# How to run
1. Run `uv sync` to download the project requirements.
2. Run `uv run scrapy crawl jozsef_attila` to scrape the poems of József Attila.
3. Run `uv run convert_results_to_md.py` to convert the html files to markdown, because its more readable and LLMs enjoy md more than html.
4. Run `uv run md_to_jsonl.py` to create a single `.jsonl` file that can be uploaded to huggingface.