from pathlib import Path
import argparse
import json
import re


DATE_LINE_RE = re.compile(r"\b\d{4}\b")


def parse_markdown_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)

    title = ""
    if lines and lines[0].startswith("## "):
        title = lines[0][3:].strip()
        lines = lines[1:]

    while lines and not lines[0].strip():
        lines.pop(0)

    while lines and not lines[-1].strip():
        lines.pop()

    date = ""
    if lines and DATE_LINE_RE.search(lines[-1]):
        date = lines[-1].strip()
        lines = lines[:-1]

    while lines and not lines[-1].strip():
        lines.pop()

    content = "\n".join(lines).strip()

    return {
        "title": title,
        "date": date,
        "content": content,
    }


def build_jsonl(input_dir: Path, output_file: Path) -> int:
    records = []
    for md_path in sorted(input_dir.glob("*.md")):
        records.append(parse_markdown_file(md_path))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert markdown files into JSONL records with title/date/content."
    )
    parser.add_argument(
        "--input-dir",
        default="results_md",
        help="Directory containing markdown files (default: results_md).",
    )
    parser.add_argument(
        "--output-file",
        default="results.jsonl",
        help="Output JSONL file path (default: results.jsonl).",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_file = Path(args.output_file)

    if not input_dir.exists():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    count = build_jsonl(input_dir, output_file)
    print(f"Wrote {count} record(s) to {output_file}")


if __name__ == "__main__":
    main()
