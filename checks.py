"""Run with python checks.py; no third-party packages required."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
SECTIONS = ["遇到的問題", "可以怎麼做", "實際例子", "行動清單", "下一步"]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.ids = []
        self.links = []
        self.headings = []
        self.title = ""
        self.capture = None
        self.text = []
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag in ("h2", "title"):
            self.capture = tag
            self.text = []

    def handle_data(self, data):
        if self.capture:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == self.capture:
            text = "".join(self.text).strip()
            if tag == "h2":
                self.headings.append(text)
            else:
                self.title = text
            self.capture = None


def check():
    pages = {path.resolve(): Page(path) for path in ROOT.rglob("*.html")}
    assert (ROOT / "index.html") in pages, "Missing index.html"
    titles = set()
    link_count = 0
    for path, page in pages.items():
        name = path.relative_to(ROOT)
        assert page.title and page.title not in titles, f"{name}: missing or duplicate title"
        titles.add(page.title)
        assert sum(tag == "h1" for tag, _ in page.tags) == 1, f"{name}: needs exactly one h1"
        assert any(tag == "html" and attrs.get("lang") == "zh-Hant" for tag, attrs in page.tags), f"{name}: needs zh-Hant language"
        assert any(tag == "meta" and attrs.get("name") == "viewport" for tag, attrs in page.tags), f"{name}: missing viewport"
        assert sum(tag == "main" and attrs.get("id") == "main" for tag, attrs in page.tags) == 1, f"{name}: missing main landmark"
        assert "#main" in page.links, f"{name}: missing skip link"
        assert len(page.ids) == len(set(page.ids)), f"{name}: duplicate IDs"
        assert any(tag == "link" and attrs.get("rel") == "stylesheet" and (path.parent / attrs.get("href", "")).resolve() == ROOT / "styles.css" for tag, attrs in page.tags), f"{name}: missing shared CSS"
        if path.parent.name == "guides":
            assert page.headings == SECTIONS, f"{name}: wrong article sections: {page.headings}"
            assert "../index.html" in page.links, f"{name}: missing home link"
        for link in page.links:
            url = urlsplit(link)
            assert url.scheme in ("", "https", "http", "mailto"), f"{name}: unsupported link {link}"
            if url.scheme or url.netloc:
                continue
            assert not url.path.startswith("/"), f"{name}: use relative URLs: {link}"
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert target.is_relative_to(ROOT), f"{name}: link escapes project: {link}"
            assert target.is_file(), f"{name}: broken link {link}"
            if url.fragment and target in pages:
                assert unquote(url.fragment) in pages[target].ids, f"{name}: missing anchor {link}"
            link_count += 1
    home = pages[ROOT / "index.html"]
    for path in pages:
        if path.parent.name == "guides":
            assert path.relative_to(ROOT).as_posix() in home.links, f"Home is missing {path.name}"
    print(f"PASS: {len(pages)} pages, {link_count} local links; structure, sections, titles and anchors checked.")


if __name__ == "__main__":
    check()
