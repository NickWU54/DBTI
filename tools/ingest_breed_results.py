#!/usr/bin/env python3
"""Compress generated breed result images and expose completed assets to index.html."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT_DIR = ROOT / "assets" / "breed-results"

RESULT_FILES = [
    "yes-or-no.jpg",
    "502.jpg",
    "drama.jpg",
    "momo.jpg",
    "Zzzzz.jpg",
    "emo.jpg",
    "dad.jpg",
    "salty.jpg",
    "social.jpg",
    "lazy.jpg",
    "taotie.jpg",
    "404-not-found.jpg",
    "Vme50.jpg",
    "guard.jpg",
    "8080.jpg",
    "shift.jpg",
]

BREED_KEYS = [
    "poodle",
    "chinese-rural-dog",
    "golden-retriever",
    "labrador-retriever",
    "corgi",
    "shiba-inu",
    "border-collie",
    "french-bulldog",
    "samoyed",
    "siberian-husky",
    "bichon-frise",
    "miniature-schnauzer",
    "pug",
    "chihuahua",
    "yorkshire-terrier",
    "alaskan-malamute",
    "pomeranian",
    "german-shepherd",
    "kunming-dog",
    "shih-tzu",
    "shetland-sheepdog",
    "maltese",
    "standard-poodle",
    "australian-shepherd",
    "chow-chow",
    "native-chow-chow",
]

SOURCE_EXTS = [".png", ".jpg", ".jpeg", ".webp"]


def find_source(source: Path, breed: str, result_file: str) -> Path | None:
    result_stem = Path(result_file).stem
    candidates = []
    for ext in SOURCE_EXTS:
        candidates.append(source / breed / f"{result_stem}{ext}")
        candidates.append(source / f"{breed}-{result_stem}{ext}")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def save_web_jpg(source_path: Path, out_path: Path, max_px: int, max_bytes: int) -> None:
    image = Image.open(source_path)
    image = ImageOps.exif_transpose(image).convert("RGB")
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    image = image.crop((left, top, left + side, top + side))
    if side > max_px:
        image = image.resize((max_px, max_px), Image.Resampling.LANCZOS)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    for quality in (92, 88, 84, 80, 76, 72, 68):
        image.save(out_path, "JPEG", quality=quality, optimize=True, progressive=True)
        if out_path.stat().st_size <= max_bytes:
            return
    raise RuntimeError(f"{out_path} is still larger than {max_bytes} bytes")


def collect_available() -> list[str]:
    available = []
    for breed in BREED_KEYS:
        for result_file in RESULT_FILES:
            path = OUT_DIR / breed / result_file
            if path.exists():
                available.append(f"{breed}/{result_file}")
    return available


def update_index(available: list[str]) -> None:
    content = INDEX.read_text(encoding="utf-8")
    replacement = "const availableBreedResultKeys = new Set([\n"
    replacement += "".join(f'        "{key}",\n' for key in available)
    replacement += "      ]);"
    pattern = r"const availableBreedResultKeys = new Set\(\[[\s\S]*?\]\);"
    updated, count = re.subn(pattern, replacement, content, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not update availableBreedResultKeys in index.html")
    INDEX.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--max-px", default=1024, type=int)
    parser.add_argument("--max-mb", default=2.0, type=float)
    parser.add_argument("--update-index", action="store_true")
    args = parser.parse_args()

    source = args.source.resolve()
    max_bytes = int(args.max_mb * 1024 * 1024)
    imported = []
    for breed in BREED_KEYS:
        for result_file in RESULT_FILES:
            source_path = find_source(source, breed, result_file)
            if not source_path:
                continue
            out_path = OUT_DIR / breed / result_file
            save_web_jpg(source_path, out_path, args.max_px, max_bytes)
            imported.append(f"{breed}/{result_file}")

    if args.update_index:
        update_index(collect_available())

    print(f"Imported {len(imported)} image(s).")
    for key in imported:
        print(key)


if __name__ == "__main__":
    main()
