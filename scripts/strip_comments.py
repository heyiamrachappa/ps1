#!/usr/bin/env python3
"""Strip comments from project source files and write results to .stripped/ directory.

Handles Python files using the tokenize module for safety. Uses regex for
JS/HTML/CSS which is heuristic-based and may not cover all edge cases.
"""
import os
import re
from pathlib import Path
from io import BytesIO
import tokenize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".stripped"
SKIP_DIRS = {".venv", "venv", "node_modules", ".git", "zerograde_audio_id.egg-info"}
EXTS = {"py", "js", "html", "css"}


def strip_py(src: str) -> str:
    try:
        tokens = []
        g = tokenize.tokenize(BytesIO(src.encode("utf-8")).readline)
        for tok in g:
            if tok.type == tokenize.COMMENT:
                continue
            if tok.type == tokenize.ENCODING:
                continue
            tokens.append((tok.type, tok.string))
        res = tokenize.untokenize(tokens)
        if isinstance(res, bytes):
            res = res.decode("utf-8")
        return res
    except Exception:
        return src


def strip_js_css(src: str) -> str:
    # remove /* ... */
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    # remove //... to end of line
    src = re.sub(r"//.*?$", "", src, flags=re.M)
    return src


def strip_html(src: str) -> str:
    # remove <!-- ... -->
    return re.sub(r"<!--.*?-->", "", src, flags=re.S)


def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def process_file(path: Path, rel: Path):
    ext = path.suffix.lstrip('.').lower()
    text = path.read_text(encoding='utf-8')
    if ext == 'py':
        out = strip_py(text)
    elif ext in ('js', 'css'):
        out = strip_js_css(text)
    elif ext == 'html':
        out = strip_html(text)
    else:
        out = text
    dst = OUT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding='utf-8')
    print(f"wrote {dst}")


def main():
    OUT.mkdir(exist_ok=True)
    for root, dirs, files in os.walk(ROOT):
        rootp = Path(root)
        if should_skip(rootp):
            dirs[:] = []
            continue
        for f in files:
            p = rootp / f
            rel = p.relative_to(ROOT)
            if p.suffix.lstrip('.').lower() in EXTS:
                process_file(p, rel)


if __name__ == '__main__':
    main()
