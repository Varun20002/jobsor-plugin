#!/usr/bin/env python3
"""JOBSOR one-page resume PDF. Plain Python 3, nothing to install.

Usage: python3 resume_pdf.py resume.json out.pdf
Exit 0: written on one page (prints "ok pages=1 size=<font size>").
Exit 3: does not fit on one page even at the smallest size (prints "too long by <N> lines"); drop the least relevant line and retry.
Exit 2: bad input.

resume.json:
{
  "name": "Asha Rao",
  "contact": [{"text": "+91 98xxxxxx"}, {"text": "asha@x.com", "url": "mailto:asha@x.com"}, {"text": "GitHub", "url": "https://github.com/x"}],
  "sections": [
    {"heading": "Experience", "entries": [
      {"title": "Product Intern", "right": "Jan 2026 - Jun 2026", "sub": "Acme", "sub_right": "Bengaluru",
       "link": {"text": "Demo", "url": "https://..."}, "text": "optional plain paragraph",
       "bullets": ["Built the onboarding checklist; activation went from **31% to 44%**"]}
    ]}
  ]
}
**text** is bold. Characters outside Windows-1252 are replaced (the rupee sign becomes "Rs.").
"""
import json
import sys

W_REG = "278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584,350,556,350,222,556,333,1000,556,556,333,1000,667,333,1000,350,611,350,350,222,222,333,333,350,556,1000,333,1000,500,333,944,350,500,667,278,333,556,556,556,556,260,556,333,737,370,556,584,333,737,333,400,584,333,333,333,556,537,278,333,333,365,556,834,834,834,611,667,667,667,667,667,667,1000,722,667,667,667,667,278,278,278,278,722,722,778,778,778,778,778,584,778,722,722,722,722,667,667,611,556,556,556,556,556,556,889,500,556,556,556,556,278,278,278,278,556,556,556,556,556,556,556,584,611,556,556,556,556,500,556,500"
W_BOLD = "278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584,350,556,350,278,556,500,1000,556,556,333,1000,667,333,1000,350,611,350,350,278,278,500,500,350,556,1000,333,1000,556,333,944,350,500,667,278,333,556,556,556,556,280,556,333,737,370,556,584,333,737,333,400,584,333,333,333,611,556,278,333,333,365,556,834,834,834,611,722,722,722,722,722,722,1000,722,667,667,667,667,278,278,278,278,722,722,778,778,778,778,778,584,778,722,722,722,722,667,667,611,556,556,556,556,556,556,889,556,556,556,556,556,278,278,278,278,611,611,611,611,611,611,611,584,611,611,611,611,611,556,611,556"
W_ITAL = "278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584,350,556,350,222,556,333,1000,556,556,333,1000,667,333,1000,350,611,350,350,222,222,333,333,350,556,1000,333,1000,500,333,944,350,500,667,278,333,556,556,556,556,260,556,333,737,370,556,584,333,737,333,400,584,333,333,333,556,537,278,333,333,365,556,834,834,834,611,667,667,667,667,667,667,1000,722,667,667,667,667,278,278,278,278,722,722,778,778,778,778,778,584,778,722,722,722,722,667,667,611,556,556,556,556,556,556,889,500,556,556,556,556,278,278,278,278,556,556,556,556,556,556,556,584,611,556,556,556,556,500,556,500"
WIDTHS = {f: [int(x) for x in s.split(",")] for f, s in (("R", W_REG), ("B", W_BOLD), ("I", W_ITAL))}
FONT_NAME = {"R": "Helvetica", "B": "Helvetica-Bold", "I": "Helvetica-Oblique"}
PAGE_W, PAGE_H = 595.28, 841.89  # A4
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 40.0, 36.0, 36.0
SIZES = [10.5, 10.0, 9.5, 9.0]
SWAP = {"₹": "Rs. ", "−": "-", "‐": "-", "‑": "-", " ": " ", "→": "->", "≤": "<=", "≥": ">="}


def clean(text):
    text = "".join(SWAP.get(c, c) for c in str(text))
    out = []
    for c in text:
        try:
            c.encode("cp1252")
            out.append(c)
        except UnicodeEncodeError:
            out.append("?")
    return "".join(out)


def width(text, font, size):
    w = WIDTHS[font]
    total = 0
    for b in text.encode("cp1252"):
        total += w[b - 32] if b >= 32 else 0
    return total * size / 1000.0


def pdf_str(text):
    raw = text.encode("cp1252")
    return "(" + raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)").decode("latin-1") + ")"


def runs(text):
    """Split "a **b** c" into [(word, font)] tokens, keeping the spaces as separate tokens."""
    parts = clean(text).split("**")
    tokens = []
    for i, part in enumerate(parts):
        font = "B" if i % 2 else "R"
        word = ""
        for c in part:
            if c == " ":
                if word:
                    tokens.append((word, font))
                    word = ""
                tokens.append((" ", font))
            else:
                word += c
        if word:
            tokens.append((word, font))
    return tokens


def wrap(text, size, max_w):
    lines, line, line_w = [], [], 0.0
    for tok, font in runs(text):
        tw = width(tok, font, size)
        if tok == " ":
            if line:
                line.append((tok, font))
                line_w += tw
            continue
        if line and line_w + tw > max_w:
            while line and line[-1][0] == " ":
                line_w -= width(" ", line[-1][1], size)
                line.pop()
            lines.append(line)
            line, line_w = [], 0.0
        line.append((tok, font))
        line_w += tw
    while line and line[-1][0] == " ":
        line.pop()
    if line:
        lines.append(line)
    return lines


class Page:
    def __init__(self):
        self.ops = []
        self.links = []

    def text(self, x, y, s, font, size):
        if s:
            self.ops.append("BT /F%s %.2f Tf %.2f %.2f Td %s Tj ET" % (font, size, x, y, pdf_str(s)))

    def line_runs(self, x, y, line, size):
        for tok, font in line:
            self.text(x, y, tok, font, size)
            x += width(tok, font, size)

    def rule(self, y):
        self.ops.append("0.6 w %.2f %.2f m %.2f %.2f l S" % (MARGIN_X, y, PAGE_W - MARGIN_X, y))

    def link(self, x, y, w, h, url):
        self.links.append((x, y - 2, x + w, y + h, url))


def layout(data, size, page):
    """Draw at this size; return the y reached (negative overflow means it did not fit)."""
    lead = size * 1.28
    max_w = PAGE_W - 2 * MARGIN_X
    y = PAGE_H - MARGIN_TOP - size * 1.8
    name = clean(data.get("name", ""))
    nsize = size + 7
    page.text((PAGE_W - width(name, "B", nsize)) / 2, y, name, "B", nsize)
    y -= lead * 1.35

    items = [(clean(c.get("text", "")), c.get("url")) for c in data.get("contact", []) if c.get("text")]
    if items:
        sep = "  |  "
        csize = size - 0.5
        total = sum(width(t, "R", csize) for t, _ in items) + width(sep, "R", csize) * (len(items) - 1)
        x = max(MARGIN_X, (PAGE_W - total) / 2)
        for i, (t, url) in enumerate(items):
            if i:
                page.text(x, y, sep, "R", csize)
                x += width(sep, "R", csize)
            page.text(x, y, t, "R", csize)
            tw = width(t, "R", csize)
            if url:
                page.link(x, y, tw, csize, url)
            x += tw
        y -= lead * 0.6

    for section in data.get("sections", []):
        entries = section.get("entries", [])
        if not entries:
            continue
        y -= lead * 0.75
        page.text(MARGIN_X, y, clean(section.get("heading", "")), "B", size + 1)
        y -= 3.5
        page.rule(y)
        y -= lead * 0.95
        for e in entries:
            title, right = clean(e.get("title", "")), clean(e.get("right", ""))
            if title or right:
                page.text(MARGIN_X, y, title, "B", size)
                x_after = MARGIN_X + width(title, "B", size)
                link = e.get("link")
                if link and link.get("url"):
                    lt = clean(link.get("text") or "Link")
                    lx = x_after + width("  ", "R", size)
                    page.text(lx, y, lt, "R", size - 0.5)
                    page.link(lx, y, width(lt, "R", size - 0.5), size, link["url"])
                if right:
                    page.text(PAGE_W - MARGIN_X - width(right, "R", size), y, right, "R", size)
                y -= lead
            sub, sub_right = clean(e.get("sub", "")), clean(e.get("sub_right", ""))
            if sub or sub_right:
                page.text(MARGIN_X, y, sub, "I", size)
                if sub_right:
                    page.text(PAGE_W - MARGIN_X - width(sub_right, "I", size), y, sub_right, "I", size)
                y -= lead
            if e.get("text"):
                for ln in wrap(e["text"], size, max_w):
                    page.line_runs(MARGIN_X, y, ln, size)
                    y -= lead
            indent = 11.0
            for b in e.get("bullets", []):
                for i, ln in enumerate(wrap(b, size, max_w - indent)):
                    if i == 0:
                        page.text(MARGIN_X + 2, y, "\u2022", "R", size)
                    page.line_runs(MARGIN_X + indent, y, ln, size)
                    y -= lead
            y -= lead * 0.3
    return y


def build(page):
    objs = []
    font_ids = {}
    for key in ("R", "B", "I"):
        objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding /WinAnsiEncoding >>" % FONT_NAME[key])
        font_ids[key] = len(objs)
    stream = "\n".join(page.ops).encode("latin-1")
    objs.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
    content_id = len(objs)
    annot_ids = []
    for (x1, y1, x2, y2, url) in page.links:
        u = clean(url).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        objs.append("<< /Type /Annot /Subtype /Link /Rect [%.2f %.2f %.2f %.2f] /Border [0 0 0] /A << /S /URI /URI (%s) >> >>" % (x1, y1, x2, y2, u))
        annot_ids.append(len(objs))
    pages_id = len(objs) + 2
    fonts = " ".join("/F%s %d 0 R" % (k, v) for k, v in font_ids.items())
    annots = (" /Annots [%s]" % " ".join("%d 0 R" % a for a in annot_ids)) if annot_ids else ""
    objs.append("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << %s >> >> /Contents %d 0 R%s >>"
                % (pages_id, PAGE_W, PAGE_H, fonts, content_id, annots))
    page_id = len(objs)
    objs.append("<< /Type /Pages /Kids [%d 0 R] /Count 1 >>" % page_id)
    objs.append("<< /Type /Catalog /Pages %d 0 R >>" % pages_id)
    catalog_id = len(objs)
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        body = o if isinstance(o, bytes) else o.encode("latin-1")
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, catalog_id, xref)
    return bytes(out)


def main():
    if len(sys.argv) != 3:
        print("usage: resume_pdf.py resume.json out.pdf")
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as err:
        print("bad input: %s" % err)
        return 2
    for size in SIZES:
        page = Page()
        y = layout(data, size, page)
        if y >= MARGIN_BOTTOM:
            with open(sys.argv[2], "wb") as f:
                f.write(build(page))
            print("ok pages=1 size=%s" % size)
            return 0
    lines = int((MARGIN_BOTTOM - y) / (SIZES[-1] * 1.28)) + 1
    print("too long by %d lines" % lines)
    return 3


if __name__ == "__main__":
    sys.exit(main())
