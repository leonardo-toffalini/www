from pathlib import Path
import re

import scrapy
from urllib.parse import urldefrag, urlparse


class JozsefAttilaSpider(scrapy.Spider):
    name = "jozsef_attila"
    allowed_domains = ["mek.oszk.hu"]
    start_urls = ["https://mek.oszk.hu/11800/11864/html/index.html"]

    def __init__(self, *args, **kwargs):
        output_dir = kwargs.pop("output_dir", "results")
        super().__init__(*args, **kwargs)
        self.seen_article_ids = set()
        self.seen_urls = set()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _filename_from_article_id(self, article_id):
        safe_id = re.sub(r"[^A-Za-z0-9._-]", "_", article_id)
        return self.output_dir / f"{safe_id}.html"

    def parse(self, response):
        normalized_current_url, _ = urldefrag(response.url)
        self.seen_urls.add(normalized_current_url)

        for article in response.css("article[id]"):
            article_id = article.attrib.get("id")
            if not article_id or article_id in self.seen_article_ids:
                continue

            self.seen_article_ids.add(article_id)
            article_html = article.get()
            output_file = self._filename_from_article_id(article_id)
            output_file.write_text(article_html, encoding="utf-8")

            yield {
                "article_id": article_id,
                "source_url": response.url,
                "file_path": str(output_file),
            }

        for href in response.css("a::attr(href)").getall():
            absolute_url = response.urljoin(href)
            normalized_url, _ = urldefrag(absolute_url)
            parsed = urlparse(normalized_url)

            if parsed.scheme not in {"http", "https"}:
                continue

            if parsed.hostname not in self.allowed_domains:
                continue

            if normalized_url in self.seen_urls:
                continue

            self.seen_urls.add(normalized_url)
            yield response.follow(normalized_url, callback=self.parse)
