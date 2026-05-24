from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "assets" / "results"
BREEDS_DIR = ROOT / "assets" / "breeds"


BREEDS = {
    "poodle": {"fur": "#d8c0a7", "fur2": "#f0dcc6", "ear": "floppy", "tail": "pom", "size": "medium"},
    "chinese-rural-dog": {"fur": "#b9793f", "fur2": "#f0d39e", "ear": "point", "tail": "curl", "size": "medium"},
    "golden-retriever": {"fur": "#d69a3d", "fur2": "#f3d08b", "ear": "floppy", "tail": "long", "size": "large"},
    "labrador-retriever": {"fur": "#c8964d", "fur2": "#f0c779", "ear": "floppy", "tail": "long", "size": "large"},
    "corgi": {"fur": "#c76c2d", "fur2": "#fff0d4", "ear": "point", "tail": "short", "size": "short"},
    "shiba-inu": {"fur": "#c76128", "fur2": "#ffe4bc", "ear": "point", "tail": "curl", "size": "medium"},
    "border-collie": {"fur": "#2d2b2d", "fur2": "#f7f1e8", "ear": "semi", "tail": "long", "size": "medium"},
    "french-bulldog": {"fur": "#68615b", "fur2": "#e8d3bd", "ear": "bat", "tail": "short", "size": "small"},
    "samoyed": {"fur": "#f7f4e9", "fur2": "#fffdf5", "ear": "point", "tail": "curl", "size": "large"},
    "siberian-husky": {"fur": "#7b7f86", "fur2": "#f5f7f4", "ear": "point", "tail": "brush", "size": "large"},
    "bichon-frise": {"fur": "#fbf4e5", "fur2": "#fffdf5", "ear": "round", "tail": "pom", "size": "small"},
    "miniature-schnauzer": {"fur": "#85827d", "fur2": "#d9d3c7", "ear": "fold", "tail": "short", "size": "small"},
    "pug": {"fur": "#d3a978", "fur2": "#3e332f", "ear": "fold", "tail": "curl", "size": "small"},
    "chihuahua": {"fur": "#c98a55", "fur2": "#f5cf9b", "ear": "bat", "tail": "thin", "size": "tiny"},
    "yorkshire-terrier": {"fur": "#8b6a43", "fur2": "#d4ad6b", "ear": "point", "tail": "short", "size": "tiny"},
    "alaskan-malamute": {"fur": "#4d5259", "fur2": "#f2eee4", "ear": "point", "tail": "brush", "size": "large"},
    "pomeranian": {"fur": "#dc8d35", "fur2": "#ffd79b", "ear": "point", "tail": "pom", "size": "tiny"},
    "german-shepherd": {"fur": "#6f452a", "fur2": "#1e1f22", "ear": "point", "tail": "long", "size": "large"},
    "kunming-dog": {"fur": "#8e6a45", "fur2": "#332821", "ear": "point", "tail": "long", "size": "large"},
    "shih-tzu": {"fur": "#d8c2a2", "fur2": "#fff3da", "ear": "floppy", "tail": "curl", "size": "small"},
    "shetland-sheepdog": {"fur": "#b56b32", "fur2": "#fff0cf", "ear": "semi", "tail": "brush", "size": "medium"},
    "maltese": {"fur": "#f5f1e7", "fur2": "#fffefa", "ear": "floppy", "tail": "pom", "size": "tiny"},
    "standard-poodle": {"fur": "#b99573", "fur2": "#ead2b7", "ear": "floppy", "tail": "pom", "size": "large"},
    "australian-shepherd": {"fur": "#7e6f62", "fur2": "#e8d8bf", "ear": "semi", "tail": "short", "size": "medium"},
    "chow-chow": {"fur": "#b86d35", "fur2": "#dfa568", "ear": "round", "tail": "curl", "size": "large"},
    "native-chow-chow": {"fur": "#8d5d31", "fur2": "#cf9455", "ear": "round", "tail": "curl", "size": "large"},
}


SIZE_SCALE = {
    "tiny": 0.72,
    "small": 0.82,
    "short": 0.84,
    "medium": 0.94,
    "large": 1.04,
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def polygon_points(cx: float, cy: float, rx: float, ry: float, count: int, phase: float) -> list[tuple[float, float]]:
    return [
        (cx + math.cos(phase + i * math.tau / count) * rx, cy + math.sin(phase + i * math.tau / count) * ry)
        for i in range(count)
    ]


def draw_faceted_ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], base: tuple[int, int, int], accent: tuple[int, int, int], seed: int) -> None:
    rng = random.Random(seed)
    x1, y1, x2, y2 = box
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    rx = (x2 - x1) / 2
    ry = (y2 - y1) / 2
    points = polygon_points(cx, cy, rx, ry, 18, -0.2)
    draw.polygon(points, fill=base)
    for _ in range(34):
        a = rng.random() * math.tau
        b = a + rng.uniform(0.35, 0.95)
        p1 = (cx, cy)
        p2 = (cx + math.cos(a) * rx * rng.uniform(0.55, 1.0), cy + math.sin(a) * ry * rng.uniform(0.55, 1.0))
        p3 = (cx + math.cos(b) * rx * rng.uniform(0.55, 1.0), cy + math.sin(b) * ry * rng.uniform(0.55, 1.0))
        shade = mix(base, accent, rng.uniform(0.14, 0.46))
        draw.polygon([p1, p2, p3], fill=shade)


def draw_ear(draw: ImageDraw.ImageDraw, x: int, y: int, side: int, kind: str, scale: float, fur: tuple[int, int, int], accent: tuple[int, int, int]) -> None:
    if kind in {"point", "bat"}:
        width = 78 * scale * (1.35 if kind == "bat" else 1)
        height = 112 * scale * (1.15 if kind == "bat" else 1)
        pts = [(x, y), (x + side * width, y - height), (x + side * width * 0.52, y + height * 0.16)]
        draw.polygon(pts, fill=fur)
        inner = [(x + side * width * 0.22, y - height * 0.06), (x + side * width * 0.75, y - height * 0.72), (x + side * width * 0.46, y + height * 0.03)]
        draw.polygon(inner, fill=mix(fur, accent, 0.38))
    elif kind in {"floppy", "fold"}:
        pts = [(x, y), (x + side * 92 * scale, y + 14 * scale), (x + side * 68 * scale, y + 142 * scale), (x + side * 12 * scale, y + 118 * scale)]
        draw.polygon(pts, fill=fur)
        draw.polygon([(x, y + 24 * scale), (x + side * 58 * scale, y + 42 * scale), (x + side * 42 * scale, y + 108 * scale)], fill=mix(fur, accent, 0.28))
    elif kind == "semi":
        pts = [(x, y), (x + side * 70 * scale, y - 76 * scale), (x + side * 88 * scale, y + 38 * scale), (x + side * 22 * scale, y + 82 * scale)]
        draw.polygon(pts, fill=fur)
    else:
        x2 = x + side * 88 * scale
        draw.ellipse((min(x - 54 * scale, x2), y - 30 * scale, max(x - 54 * scale, x2), y + 92 * scale), fill=fur)


def draw_tail(draw: ImageDraw.ImageDraw, cx: int, cy: int, kind: str, scale: float, fur: tuple[int, int, int], accent: tuple[int, int, int]) -> None:
    if kind in {"curl", "pom"}:
        w = 118 * scale
        box = (cx + 135 * scale, cy - 118 * scale, cx + 135 * scale + w, cy - 118 * scale + w)
        draw.arc(box, 10, 330, fill=fur, width=max(14, int(32 * scale)))
        if kind == "pom":
            draw.ellipse((cx + 204 * scale, cy - 128 * scale, cx + 285 * scale, cy - 46 * scale), fill=accent)
    elif kind == "brush":
        pts = [(cx + 138 * scale, cy - 35 * scale), (cx + 306 * scale, cy - 132 * scale), (cx + 240 * scale, cy - 8 * scale)]
        draw.polygon(pts, fill=fur)
    elif kind == "long":
        draw.line((cx + 136 * scale, cy - 18 * scale, cx + 288 * scale, cy - 92 * scale), fill=fur, width=max(18, int(34 * scale)))
    elif kind == "thin":
        draw.arc((cx + 130 * scale, cy - 98 * scale, cx + 270 * scale, cy + 28 * scale), 205, 330, fill=fur, width=max(8, int(14 * scale)))


def draw_breed_dog(base: Image.Image, breed_key: str, result_key: str) -> Image.Image:
    spec = BREEDS[breed_key]
    fur = hex_to_rgb(spec["fur"])
    accent = hex_to_rgb(spec["fur2"])
    scale = SIZE_SCALE[spec["size"]]
    w, h = base.size
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx = int(w * 0.51)
    cy = int(h * 0.61)
    body_w = int(w * 0.46 * scale)
    body_h = int(h * 0.34 * scale * (0.82 if spec["size"] == "short" else 1))
    head_r = int(w * 0.17 * scale)

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse((cx - body_w // 2, cy + body_h // 4, cx + body_w // 2, cy + body_h // 2 + 52), fill=(37, 30, 42, 46))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    overlay.alpha_composite(shadow)
    draw = ImageDraw.Draw(overlay)

    outline = (255, 250, 238, 238)
    body_box = (cx - body_w // 2 - 12, cy - body_h // 2 - 8, cx + body_w // 2 + 12, cy + body_h // 2 + 12)
    draw.ellipse(body_box, fill=outline)
    draw_tail(draw, cx, cy, spec["tail"], scale, fur + (255,), accent + (255,))

    body_box = (cx - body_w // 2, cy - body_h // 2, cx + body_w // 2, cy + body_h // 2)
    draw_faceted_ellipse(draw, body_box, fur + (255,), accent + (255,), hash((breed_key, result_key, "body")) & 0xFFFF)

    head_cx = int(cx - body_w * 0.22)
    head_cy = int(cy - body_h * 0.42)
    draw_ear(draw, head_cx - int(head_r * 0.55), head_cy - int(head_r * 0.24), -1, spec["ear"], scale, fur + (255,), accent + (255,))
    draw_ear(draw, head_cx + int(head_r * 0.55), head_cy - int(head_r * 0.24), 1, spec["ear"], scale, fur + (255,), accent + (255,))
    draw.ellipse((head_cx - head_r - 10, head_cy - head_r - 10, head_cx + head_r + 10, head_cy + head_r + 10), fill=outline)
    draw_faceted_ellipse(draw, (head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r), fur + (255,), accent + (255,), hash((breed_key, result_key, "head")) & 0xFFFF)

    if breed_key in {"border-collie", "siberian-husky", "alaskan-malamute", "german-shepherd", "kunming-dog"}:
        draw.polygon(
            [(head_cx - head_r * 0.82, head_cy - head_r * 0.55), (head_cx, head_cy - head_r * 0.1), (head_cx + head_r * 0.82, head_cy - head_r * 0.55), (head_cx + head_r * 0.38, head_cy - head_r * 0.94), (head_cx - head_r * 0.38, head_cy - head_r * 0.94)],
            fill=accent + (250,),
        )
    if breed_key in {"pug", "french-bulldog"}:
        draw.ellipse((head_cx - head_r * 0.48, head_cy - head_r * 0.08, head_cx + head_r * 0.48, head_cy + head_r * 0.55), fill=accent + (255,))
    else:
        draw.ellipse((head_cx - head_r * 0.44, head_cy + head_r * 0.02, head_cx + head_r * 0.46, head_cy + head_r * 0.58), fill=mix(accent, (255, 255, 255), 0.16) + (255,))

    eye_y = head_cy - int(head_r * 0.22)
    for dx in (-0.36, 0.36):
        ex = int(head_cx + head_r * dx)
        draw.ellipse((ex - 13, eye_y - 13, ex + 13, eye_y + 13), fill=(38, 31, 31, 255))
        draw.ellipse((ex - 5, eye_y - 6, ex, eye_y - 1), fill=(255, 255, 255, 230))
    nose_w = int(head_r * (0.24 if spec["size"] in {"tiny", "small"} else 0.3))
    nose_y = int(head_cy + head_r * 0.16)
    draw.rounded_rectangle((head_cx - nose_w, nose_y - 12, head_cx + nose_w, nose_y + 18), radius=12, fill=(34, 28, 26, 255))
    draw.arc((head_cx - 46, nose_y + 8, head_cx, nose_y + 54), 15, 82, fill=(72, 49, 43, 240), width=5)
    draw.arc((head_cx, nose_y + 8, head_cx + 46, nose_y + 54), 98, 166, fill=(72, 49, 43, 240), width=5)

    leg_y = cy + body_h // 2 - 16
    for dx in (-0.28, 0.22):
        lx = int(cx + body_w * dx)
        draw.rounded_rectangle((lx - 38 * scale, leg_y - 30 * scale, lx + 38 * scale, leg_y + 78 * scale), radius=int(28 * scale), fill=outline)
        draw.rounded_rectangle((lx - 28 * scale, leg_y - 22 * scale, lx + 28 * scale, leg_y + 62 * scale), radius=int(22 * scale), fill=accent + (255,))

    if breed_key in {"bichon-frise", "poodle", "standard-poodle", "maltese", "pomeranian", "chow-chow", "native-chow-chow"}:
        for angle in range(0, 360, 28):
            px = head_cx + math.cos(math.radians(angle)) * head_r * 0.72
            py = head_cy + math.sin(math.radians(angle)) * head_r * 0.72
            draw.ellipse((px - 24 * scale, py - 24 * scale, px + 24 * scale, py + 24 * scale), fill=mix(fur, accent, 0.28) + (180,))

    composed = base.convert("RGBA")
    composed.alpha_composite(overlay)
    return composed.convert("RGB")


def main() -> None:
    result_files = sorted(RESULTS_DIR.glob("*.jpg"))
    BREEDS_DIR.mkdir(parents=True, exist_ok=True)
    for breed_key in BREEDS:
        out_dir = BREEDS_DIR / breed_key
        out_dir.mkdir(parents=True, exist_ok=True)
        for src in result_files:
            base = Image.open(src).convert("RGB")
            generated = draw_breed_dog(base, breed_key, src.stem)
            generated.save(out_dir / src.name, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"generated {len(BREEDS) * len(result_files)} breed result images")


if __name__ == "__main__":
    main()
