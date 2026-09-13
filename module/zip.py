#!/usr/bin/env python3
"""
zip.py — pack folder module menjadi zip Magisk (anti-bug backslash).
Diadaptasi dari ex-zip.py Example-Build (pathlib + argparse + versi module.prop).

Cara pakai (dari folder module/):
    python zip.py                    # -> build/faacb-v<version>.zip
    python zip.py -o rilis.zip       # -> build/rilis.zip
    python zip.py --no-version       # -> build/faacb.zip
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import zipfile

# ---------------- KONFIG ----------------
APP_NAME = "faacb"

REQUIRED = [
    "module.prop",
    "customize.sh",
    "uninstall.sh",
    "service.sh",
    "META-INF/com/google/android/update-binary",
    "META-INF/com/google/android/updater-script",
    "system/bin/faacb",
    "helper/classes.dex",
    "system/app/FcbManager/FcbManager.apk",
]

EXECUTABLES = {
    "customize.sh",
    "uninstall.sh",
    "service.sh",
    "system/bin/faacb",
}

EXCLUDE_DIRS = {
    "temp", "__pycache__", ".git", ".hg", ".svn",
    "archive", "build", "manager", "obj", "dex",
}
EXCLUDE_FILES = {
    ".DS_Store", "Thumbs.db",
    "zip.py",
    ".gitignore", ".gitattributes",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".zip"}
# ----------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent


def read_version(module_dir: pathlib.Path) -> str:
    try:
        text = (module_dir / "module.prop").read_text(encoding="utf-8")
    except OSError:
        return "1.0.0"
    m = re.search(r"^version\s*=\s*(.+?)\s*$", text, re.M)
    if not m:
        return "1.0.0"
    return m.group(1).lstrip("v").strip() or "1.0.0"


def should_skip(path: pathlib.Path, module_dir: pathlib.Path) -> bool:
    rel = path.relative_to(module_dir)
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return True
    if path.is_file():
        if path.name in EXCLUDE_FILES:
            return True
        if path.name.startswith("session-"):
            return True
        if path.suffix in EXCLUDE_SUFFIXES:
            return True
    return False


def zip_info_for(path: pathlib.Path, arcname_posix: str) -> zipfile.ZipInfo:
    zi = zipfile.ZipInfo(filename=arcname_posix)
    zi.compress_type = zipfile.ZIP_DEFLATED
    if path.is_dir():
        zi.filename += "/"
        zi.external_attr = (0o755 << 16) | 0x10
    else:
        mode = 0o755 if arcname_posix in EXECUTABLES else 0o644
        zi.external_attr = mode << 16
    return zi


def build(module_dir: pathlib.Path, out_zip: pathlib.Path) -> pathlib.Path:
    if not module_dir.is_dir():
        sys.exit("Module dir tidak ketemu: %s" % module_dir)
    missing = [f for f in REQUIRED if not (module_dir / f).exists()]
    if missing:
        sys.exit("File wajib hilang: " + ", ".join(missing))
    out_zip = out_zip.resolve()
    files: list[pathlib.Path] = []
    for p in sorted(module_dir.rglob("*")):
        if p.resolve() == out_zip:
            continue
        if should_skip(p, module_dir):
            continue
        files.append(p)
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arc = path.relative_to(module_dir).as_posix()
            zi = zip_info_for(path, arc)
            if path.is_dir():
                zf.writestr(zi, "")
            else:
                zf.writestr(zi, path.read_bytes())
    with zipfile.ZipFile(out_zip) as zf:
        bad = [n for n in zf.namelist() if "\\" in n]
        if bad:
            sys.exit("ZIP cacat, ada backslash: %s" % bad[:5])
    return out_zip


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Pack module menjadi zip Magisk.")
    ap.add_argument("path", nargs="?", default=".",
                    help="Path module (default: folder script ini)")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--no-version", action="store_true")
    args = ap.parse_args(argv)
    module_dir = pathlib.Path(args.path).resolve()
    if args.path == "." and ROOT != pathlib.Path.cwd().resolve():
        module_dir = pathlib.Path.cwd().resolve()
    outdir = module_dir / "build"
    outdir.mkdir(parents=True, exist_ok=True)
    version = read_version(module_dir)
    if args.output:
        out = pathlib.Path(args.output)
        out = out if out.is_absolute() else (outdir / out.name)
    elif args.no_version:
        out = outdir / ("%s.zip" % APP_NAME)
    else:
        out = outdir / ("%s-v%s.zip" % (APP_NAME, version))
    result = build(module_dir, out)
    print("OK: %s (%.1f KB) dari %s"
          % (result.name, result.stat().st_size / 1024, module_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
