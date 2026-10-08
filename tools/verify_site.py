#!/usr/bin/env python3
"""Focused local and deployed-site checks for Quran Reels Publisher."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import re
import struct
import sys
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://mahmoudblog4-png.github.io/quran-reels-publisher-site/"
TOKEN_FILE = "tiktokvjJklXigqA8jNbixNnCDhujkValANaJT.txt"
ICON_FILE = "assets/app-icon.png"
PAGES = {
    "index.html": SITE_URL,
    "privacy.html": SITE_URL + "privacy.html",
    "terms.html": SITE_URL + "terms.html",
}
TEXT_FILES = frozenset((*PAGES, "style.css"))
LEGAL_SHA256 = {
    "privacy.html": "3a6b1d0086ba6c03fcd36f84796957a4df6d6e23d8bc2117097bf37ab9361f8c",
    "terms.html": "a9125cfda526bce2f3576e0afa37832c3cb8df4edff31f6250359ffe63e6e55e",
}
TOKEN_SHA256 = "83b38625413718c6a802354139d2e8dc014c235369df22be97f9d0a50e457a13"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.references: list[str] = []
        self.legal_depth = 0
        self.legal_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        if tag == "link":
            self.links.append(attributes)
            self.references.append(attributes.get("href", ""))
        elif tag == "img":
            self.images.append(attributes)
            self.references.append(attributes.get("src", ""))
        elif tag == "a":
            self.references.append(attributes.get("href", ""))
        if tag == "div" and "legal-content" in attributes.get("class", "").split():
            self.legal_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.legal_depth:
            self.legal_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.legal_depth:
            self.legal_chunks.append(data)


def fail(message: str) -> None:
    raise ValueError(message)


def parse_page(name: str, content: bytes) -> tuple[str, SiteParser]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{name}: not valid UTF-8 ({exc})")
    parser = SiteParser()
    parser.feed(text)
    parser.close()
    return text, parser


def check_html(name: str, content: bytes, *, check_local_links: bool) -> None:
    text, parser = parse_page(name, content)
    canonicals = [item.get("href", "") for item in parser.links if "canonical" in item.get("rel", "").lower().split()]
    if canonicals != [PAGES[name]]:
        fail(f"{name}: canonical URL is {canonicals!r}; expected {PAGES[name]!r}")

    icons = [item.get("href", "") for item in parser.links if "icon" in item.get("rel", "").lower().split()]
    apple_icons = [item.get("href", "") for item in parser.links if "apple-touch-icon" in item.get("rel", "").lower().split()]
    if icons != [ICON_FILE] or apple_icons != [ICON_FILE]:
        fail(f"{name}: favicon and apple-touch-icon must both reference only {ICON_FILE}")
    brands = [item.get("src", "") for item in parser.images if "brand-icon" in item.get("class", "").split()]
    if brands != [ICON_FILE]:
        fail(f"{name}: header logo must reference only {ICON_FILE}")

    if name in LEGAL_SHA256:
        match = re.search(r'<div class="legal-content">(.*?)</div>', text, re.DOTALL)
        if not match:
            fail(f"{name}: legal body container is missing")
        legal_body = match.group(1).replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        digest = hashlib.sha256(legal_body).hexdigest()
        if digest != LEGAL_SHA256[name]:
            fail(f"{name}: legal body differs from the original baseline ({digest})")

    if check_local_links:
        for value in parser.references:
            if not value or value.startswith("#"):
                continue
            parsed = urlparse(value)
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path.startswith("/"):
                fail(f"{name}: internal link is root-relative, not project-path-safe: {value}")
            rel_path = unquote(parsed.path)
            target = (ROOT / Path(name).parent / rel_path).resolve() if rel_path else (ROOT / name).resolve()
            if not target.is_relative_to(ROOT.resolve()):
                fail(f"{name}: internal link escapes the project: {value}")
            if not target.is_file():
                fail(f"{name}: internal link target does not exist: {value}")


def check_local() -> None:
    for name in PAGES:
        check_html(name, (ROOT / name).read_bytes(), check_local_links=True)

    icon = (ROOT / ICON_FILE).read_bytes()
    if len(icon) >= 1_000_000:
        fail(f"{ICON_FILE}: PNG must be smaller than 1 MB (is {len(icon)} bytes)")
    if len(icon) < 26 or icon[:8] != PNG_SIGNATURE or icon[12:16] != b"IHDR":
        fail(f"{ICON_FILE}: invalid PNG signature or IHDR")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", icon[16:26])
    if (width, height) != (512, 512):
        fail(f"{ICON_FILE}: dimensions are {width}x{height}, expected 512x512")
    if color_type != 2:
        fail(f"{ICON_FILE}: PNG must be opaque RGB (color type 2; got {color_type})")
    if bit_depth not in (8, 16):
        fail(f"{ICON_FILE}: unsupported RGB bit depth {bit_depth}")

    token_hash = hashlib.sha256((ROOT / TOKEN_FILE).read_bytes()).hexdigest()
    if token_hash != TOKEN_SHA256:
        fail(f"{TOKEN_FILE}: verification file differs from its original byte baseline ({token_hash})")

    if not (ROOT / "style.css").is_file():
        fail("style.css: stylesheet is missing")
    print("PASS local: PNG signature, 512x512 opaque RGB, and size under 1 MB")
    print("PASS local: all pages use the same icon, project-safe links, and exact canonical URLs")
    print("PASS local: legal bodies and TikTok verification file match original baselines")


class RedirectLog(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.redirects: list[tuple[str, str]] = []

    def redirect_request(self, request, fp, code, message, headers, newurl):
        self.redirects.append((request.full_url, newurl))
        return super().redirect_request(request, fp, code, message, headers, newurl)


def fetch(url: str) -> tuple[str, int, str, bytes, list[tuple[str, str]]]:
    redirects = RedirectLog()
    opener = build_opener(redirects)
    request = Request(url, headers={"User-Agent": "QuranReelsSiteVerifier/1.0"})
    with opener.open(request, timeout=25) as response:
        return (
            response.geturl(),
            response.status,
            response.headers.get_content_type(),
            response.read(),
            redirects.redirects,
        )


def check_live() -> None:
    check_local()
    expected = {
        "index.html": (SITE_URL, "text/html"),
        "privacy.html": (urljoin(SITE_URL, "privacy.html"), "text/html"),
        "terms.html": (urljoin(SITE_URL, "terms.html"), "text/html"),
        "style.css": (urljoin(SITE_URL, "style.css"), "text/css"),
        ICON_FILE: (urljoin(SITE_URL, ICON_FILE), "image/png"),
        TOKEN_FILE: (urljoin(SITE_URL, TOKEN_FILE), "text/plain"),
    }
    errors: list[str] = []
    for path, (url, content_type) in expected.items():
        try:
            final_url, status, actual_type, body, _ = fetch(url)
        except Exception as exc:
            errors.append(f"live {path}: request failed: {exc}")
            continue
        if status != 200:
            errors.append(f"live {path}: HTTP status {status}")
        if actual_type != content_type:
            errors.append(f"live {path}: content type {actual_type!r}, expected {content_type!r}")
        if final_url != url:
            errors.append(f"live {path}: resolved to {final_url!r}, expected {url!r}")
        local_body = (ROOT / path).read_bytes()
        if path in TEXT_FILES:
            matches = body.replace(b"\r\n", b"\n") == local_body.replace(b"\r\n", b"\n")
        else:
            matches = body == local_body
        if not matches:
            errors.append(f"live {path}: deployed content differs from local file (deployment may be pending)")
        if path in PAGES:
            try:
                check_html(path, body, check_local_links=False)
            except Exception as exc:
                errors.append(f"live {path}: {exc}")

    for candidate in (
        "http://mahmoudblog4-png.github.io/quran-reels-publisher-site/",
        "http://mahmoudblog4-png.github.io/quran-reels-publisher-site",
        "https://mahmoudblog4-png.github.io/quran-reels-publisher-site",
    ):
        try:
            final_url, status, _, _, redirects = fetch(candidate)
        except Exception as exc:
            errors.append(f"live redirect {candidate}: request failed: {exc}")
            continue
        if status != 200 or final_url != SITE_URL or not redirects:
            errors.append(f"live redirect: {candidate} ended at {final_url} (HTTP {status}); expected redirect to {SITE_URL}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        fail(f"live verification found {len(errors)} issue(s); after deployment, rerun this command once")
    print("PASS live: HTTPS pages, stylesheet, PNG, and verification file return expected status/content types")
    print("PASS live: text content matches after newline normalization; PNG and verification token match exact bytes; icon references and legal bodies are preserved")
    print("PASS live: HTTP and no-trailing-slash URLs redirect to the canonical HTTPS home URL")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--local", action="store_true", help="check local site files and preservation baselines")
    modes.add_argument("--live", action="store_true", help="check deployed HTTPS site and redirect behavior")
    args = parser.parse_args()
    try:
        check_local() if args.local else check_live()
    except Exception as exc:  # Keep the verifier's failure concise and actionable.
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
