"""
MDfy - Batch PDF to Markdown converter
Uses Microsoft MarkItDown for conversion.

Usage:
    python mdfy.py <input_folder> [output_folder]

    input_folder  : folder containing PDF files to convert
    output_folder : (optional) destination for .md files; defaults to input_folder
"""

import argparse
import hashlib
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("ERROR: 'markitdown' is not installed. Run:  pip install markitdown")
    sys.exit(1)


def file_hash(path: Path) -> str:
    """Return SHA-256 hex digest of a file (for duplicate detection)."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_unique_pdfs(input_folder: Path) -> list[Path]:
    """
    Walk input_folder recursively, collect all PDFs and deduplicate by content hash.
    When duplicates are found, the first file encountered (alphabetical order) is kept.
    Case-insensitive extension matching (.pdf / .PDF).
    """
    seen: dict[str, Path] = {}
    skipped = 0

    all_pdfs = sorted(
        p for p in input_folder.rglob("*") if p.suffix.lower() == ".pdf"
    )

    for pdf in all_pdfs:
        digest = file_hash(pdf)
        if digest in seen:
            skipped += 1
            print(f"  [SKIP duplicate] {pdf}  (same content as {seen[digest]})")
        else:
            seen[digest] = pdf

    if skipped:
        print(f"\n  {skipped} duplicate(s) ignored.\n")

    return list(seen.values())


def md_output_path(pdf_path: Path, input_folder: Path, output_folder: Path) -> Path:
    """
    Derive output .md path, preserving sub-folder structure relative to input_folder.
    This avoids silent overwrites when two PDFs share the same stem in different subfolders.
    """
    relative = pdf_path.relative_to(input_folder)
    return (output_folder / relative).with_suffix(".md")


def already_converted(pdf_path: Path, input_folder: Path, output_folder: Path) -> bool:
    """Return True if a .md output already exists for this PDF."""
    return md_output_path(pdf_path, input_folder, output_folder).exists()


def convert(
    pdf_path: Path, input_folder: Path, output_folder: Path, converter: MarkItDown
) -> None:
    """Convert a single PDF to Markdown using MarkItDown."""
    md_path = md_output_path(pdf_path, input_folder, output_folder)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    result = converter.convert(str(pdf_path))
    text = result.text_content or ""
    md_path.write_text(text, encoding="utf-8")
    print(f"  [OK] {pdf_path.name}  ->  {md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-convert PDFs to Markdown using MarkItDown."
    )
    parser.add_argument("input_folder", type=Path, help="Folder containing PDF files")
    parser.add_argument(
        "output_folder",
        type=Path,
        nargs="?",
        default=None,
        help="Destination folder for .md files (default: same as input_folder)",
    )
    args = parser.parse_args()

    input_folder: Path = args.input_folder.resolve()
    output_folder: Path = (args.output_folder or input_folder).resolve()

    if not input_folder.is_dir():
        print(f"ERROR: '{input_folder}' is not a valid directory.")
        sys.exit(1)

    output_folder.mkdir(parents=True, exist_ok=True)

    print(f"\nScanning: {input_folder}")
    print(f"Output  : {output_folder}\n")

    pdfs = collect_unique_pdfs(input_folder)

    if not pdfs:
        print("No PDF files found.")
        return

    converter = MarkItDown()
    converted = skipped_existing = errors = 0

    for pdf in pdfs:
        if already_converted(pdf, input_folder, output_folder):
            print(f"  [SKIP existing] {pdf.name}")
            skipped_existing += 1
            continue
        try:
            convert(pdf, input_folder, output_folder, converter)
            converted += 1
        except Exception as exc:
            print(f"  [ERROR] {pdf.name}: {exc}")
            errors += 1

    print(
        f"\nDone. Converted: {converted} | Already existed: {skipped_existing} | Errors: {errors}"
    )


if __name__ == "__main__":
    main()
