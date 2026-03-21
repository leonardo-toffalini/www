from pathlib import Path
import argparse

from markdownify import markdownify as html_to_markdown


def convert_directory(input_dir: Path, output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    for html_path in sorted(input_dir.glob("*.html")):
        html_content = html_path.read_text(encoding="utf-8")
        markdown_content = html_to_markdown(html_content, heading_style="ATX")

        output_path = output_dir / f"{html_path.stem}.md"
        output_path.write_text(markdown_content, encoding="utf-8")
        converted += 1

    return converted


def main():
    input_dir = "results"
    output_dir = "results_md"
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    converted_count = convert_directory(input_dir, output_dir)
    print(f"Converted {converted_count} file(s) into {output_dir}")


if __name__ == "__main__":
    main()
