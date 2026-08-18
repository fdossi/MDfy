import os, shutil, subprocess, tarfile, tempfile, zipfile
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from markitdown import MarkItDown

app=FastAPI(title="MDfy API",version="1.0.0")
origins=[x.strip() for x in os.getenv("ALLOWED_ORIGINS","*").split(",")]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_methods=["GET","POST"],allow_headers=["*"],expose_headers=["x-output-filename"])
SUPPORTED={".pdf",".docx",".epub",".mobi",".doc",".xls",".xlsx",".csv",".png",".jpg",".jpeg",".tif",".tiff",".djvu"}
ARCHIVES={".zip",".tar",".tgz"};MAX_BYTES=100*1024*1024

def safe_extract(archive:Path,target:Path):
    root=target.resolve()
    if archive.suffix.lower()==".zip":
        with zipfile.ZipFile(archive) as z:
            if any(not (target/m.filename).resolve().is_relative_to(root) for m in z.infolist()):raise ValueError("Pacote contém caminho inseguro")
            z.extractall(target)
    else:
        with tarfile.open(archive,"r:gz" if archive.suffix.lower()==".tgz" else "r:") as t:
            if any(not (target/m.name).resolve().is_relative_to(root) for m in t.getmembers()):raise ValueError("Pacote contém caminho inseguro")
            t.extractall(target,filter="data")

def convert_one(source:Path,output:Path):
    temp=None
    try:
        target=source
        if source.suffix.lower()==".djvu":
            temp=source.with_suffix(".temp.pdf");subprocess.run(["ddjvu","-format=pdf",str(source),str(temp)],check=True,timeout=180);target=temp
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(MarkItDown().convert(str(target)).text_content,encoding="utf-8")
    finally:
        if temp:temp.unlink(missing_ok=True)

@app.get("/health")
def health():return {"status":"ok"}

@app.post("/convert")
async def convert(file:UploadFile=File(...)):
    filename=Path(file.filename or "arquivo").name;suffix=Path(filename).suffix.lower()
    if suffix not in SUPPORTED|ARCHIVES:raise HTTPException(415,"Formato não compatível")
    work=Path(tempfile.mkdtemp(prefix="mdfy-"));source=work/filename;total=0
    try:
        with source.open("wb") as stream:
            while chunk:=await file.read(1024*1024):
                total+=len(chunk)
                if total>MAX_BYTES:raise HTTPException(413,"O limite é de 100 MB por arquivo")
                stream.write(chunk)
        if suffix in ARCHIVES:
            extracted=work/"extraidos";converted=work/"markdown";extracted.mkdir();safe_extract(source,extracted);count=0
            for item in extracted.rglob("*"):
                if item.is_file() and item.suffix.lower() in SUPPORTED:
                    convert_one(item,converted/item.relative_to(extracted).with_suffix(".md"));count+=1
            if not count:raise HTTPException(422,"O pacote não contém arquivos compatíveis")
            result=Path(shutil.make_archive(str(work/"markdown-convertido"),"zip",converted));name="markdown-convertido.zip";media="application/zip"
        else:
            result=work/f"{source.stem}.md";convert_one(source,result);name=result.name;media="text/markdown; charset=utf-8"
        return FileResponse(result,filename=name,media_type=media,headers={"x-output-filename":name},background=BackgroundTask(shutil.rmtree,work,ignore_errors=True))
    except HTTPException:
        shutil.rmtree(work,ignore_errors=True);raise
    except Exception as exc:
        shutil.rmtree(work,ignore_errors=True);raise HTTPException(500,f"Não foi possível converter: {exc}") from exc
