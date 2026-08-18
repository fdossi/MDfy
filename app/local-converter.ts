export const LOCAL_FORMATS = new Set(["pdf", "docx", "xlsx", "csv", "epub"]);

const clean = (value: string) => value.replace(/\r\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
const escapeCell = (value: unknown) => String(value ?? "").replace(/\|/g, "\\|").replace(/\r?\n/g, "<br>");

function tableToMarkdown(rows: unknown[][]) {
  if (!rows.length) return "";
  const width = Math.max(...rows.map(row => row.length), 1);
  const normalized = rows.map(row => Array.from({length: width}, (_, index) => escapeCell(row[index])));
  const header = normalized[0];
  return [`| ${header.join(" | ")} |`, `| ${header.map(() => "---").join(" | ")} |`, ...normalized.slice(1).map(row => `| ${row.join(" | ")} |`)].join("\n");
}

function parseCsv(text: string) {
  const rows: string[][] = [];
  let row: string[] = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (char === '"' && quoted && text[i + 1] === '"') { field += '"'; i++; }
    else if (char === '"') quoted = !quoted;
    else if (char === "," && !quoted) { row.push(field); field = ""; }
    else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && text[i + 1] === "\n") i++;
      row.push(field); if (row.some(cell => cell.length)) rows.push(row); row = []; field = "";
    } else field += char;
  }
  row.push(field); if (row.some(cell => cell.length)) rows.push(row);
  return rows;
}

async function pdfToMarkdown(file: File) {
  const pdfjs = await import("pdfjs-dist");
  pdfjs.GlobalWorkerOptions.workerSrc = new URL("pdfjs-dist/build/pdf.worker.min.mjs", import.meta.url).toString();
  const document = await pdfjs.getDocument({data: new Uint8Array(await file.arrayBuffer())}).promise;
  const pages: string[] = [];
  for (let number = 1; number <= document.numPages; number++) {
    const page = await document.getPage(number);
    const content = await page.getTextContent();
    const text = content.items.map(item => "str" in item ? item.str : "").join(" ").replace(/\s+/g, " ").trim();
    if (text) pages.push(`## Página ${number}\n\n${text}`);
  }
  const output = pages.join("\n\n");
  if (output.replace(/[^\p{L}\p{N}]/gu, "").length < 20) throw new Error("Este PDF parece digitalizado e precisa do conversor avançado com OCR.");
  return output;
}

async function workbookToMarkdown(file: File) {
  const {default: JSZip} = await import("jszip");
  const zip = await JSZip.loadAsync(await file.arrayBuffer());
  const sharedFile = zip.file("xl/sharedStrings.xml");
  const shared: string[] = [];
  if (sharedFile) {
    const doc = new DOMParser().parseFromString(await sharedFile.async("text"), "application/xml");
    doc.querySelectorAll("si").forEach(node => shared.push(Array.from(node.querySelectorAll("t")).map(value => value.textContent ?? "").join("")));
  }
  const sections: string[] = [];
  const sheets = Object.keys(zip.files).filter(name => /^xl\/worksheets\/sheet\d+\.xml$/.test(name)).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
  for (const [index,name] of sheets.entries()) {
    const doc = new DOMParser().parseFromString(await zip.files[name].async("text"), "application/xml");
    const rows: unknown[][] = [];
    doc.querySelectorAll("sheetData row").forEach(row => {
      const values: string[] = [];
      row.querySelectorAll("c").forEach(cell => {
        const reference = cell.getAttribute("r") ?? "A1";
        const column = reference.replace(/\d/g, "").split("").reduce((total,char)=>total*26+char.charCodeAt(0)-64,0)-1;
        const raw = cell.querySelector("v")?.textContent ?? cell.querySelector("is t")?.textContent ?? "";
        values[column] = cell.getAttribute("t") === "s" ? (shared[Number(raw)] ?? raw) : raw;
      });
      rows.push(values);
    });
    if (rows.length) sections.push(`# Planilha ${index+1}\n\n${tableToMarkdown(rows)}`);
  }
  return sections.join("\n\n");
}

async function epubToMarkdown(file: File) {
  const {default: JSZip} = await import("jszip");
  const zip = await JSZip.loadAsync(await file.arrayBuffer());
  const names = Object.keys(zip.files).filter(name => /\.(xhtml|html|htm)$/i.test(name) && !zip.files[name].dir).sort();
  const sections: string[] = [];
  for (const name of names) {
    const html = await zip.files[name].async("text");
    const doc = new DOMParser().parseFromString(html, "text/html");
    doc.querySelectorAll("script,style,nav").forEach(node => node.remove());
    doc.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach(node => {
      const level = Number(node.tagName.slice(1)); node.replaceWith(`${"#".repeat(level)} ${node.textContent ?? ""}\n\n`);
    });
    doc.querySelectorAll("p,li,blockquote").forEach(node => node.append("\n\n"));
    const text = clean(doc.body.textContent ?? "");
    if (text) sections.push(text);
  }
  if (!sections.length) throw new Error("Não foi possível localizar o conteúdo textual deste EPUB.");
  return sections.join("\n\n---\n\n");
}

export async function convertLocally(file: File) {
  const extension = file.name.toLowerCase().split(".").pop() ?? "";
  let markdown = "";
  if (extension === "pdf") markdown = await pdfToMarkdown(file);
  else if (extension === "docx") { const mammoth = await import("mammoth"); markdown = (await mammoth.convertToMarkdown({arrayBuffer: await file.arrayBuffer()})).value; }
  else if (extension === "xlsx") markdown = await workbookToMarkdown(file);
  else if (extension === "csv") markdown = tableToMarkdown(parseCsv(await file.text()));
  else if (extension === "epub") markdown = await epubToMarkdown(file);
  else throw new Error("Este formato requer o conversor avançado.");
  return new Blob([`${clean(markdown)}\n`], {type: "text/markdown;charset=utf-8"});
}
