#!/usr/bin/env python3
"""Build a JSONL queue of breed-specific DBTI image prompts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BREEDS = [
    ("poodle", "贵宾犬 / toy poodle or teddy poodle"),
    ("chinese-rural-dog", "中华田园犬 / Chinese rural dog"),
    ("golden-retriever", "金毛寻回犬 / golden retriever"),
    ("labrador-retriever", "拉布拉多寻回犬 / Labrador retriever"),
    ("corgi", "威尔士柯基犬 / Welsh corgi"),
    ("shiba-inu", "日本柴犬 / Shiba Inu"),
    ("border-collie", "边境牧羊犬 / border collie"),
    ("french-bulldog", "法国斗牛犬 / French bulldog"),
    ("samoyed", "萨摩耶犬 / Samoyed"),
    ("siberian-husky", "西伯利亚雪橇犬 / Siberian husky"),
    ("bichon-frise", "比熊犬 / Bichon Frise"),
    ("miniature-schnauzer", "迷你雪纳瑞 / miniature schnauzer"),
    ("pug", "巴哥犬 / pug"),
    ("chihuahua", "吉娃娃犬 / Chihuahua"),
    ("yorkshire-terrier", "约克夏梗 / Yorkshire terrier"),
    ("alaskan-malamute", "阿拉斯加雪橇犬 / Alaskan malamute"),
    ("pomeranian", "博美犬 / Pomeranian"),
    ("german-shepherd", "德国牧羊犬 / German shepherd"),
    ("kunming-dog", "昆明犬 / Kunming dog"),
    ("shih-tzu", "西施犬 / Shih Tzu"),
    ("shetland-sheepdog", "喜乐蒂牧羊犬 / Shetland sheepdog"),
    ("maltese", "马尔济斯犬 / Maltese"),
    ("standard-poodle", "巨型贵宾犬 / standard poodle"),
    ("australian-shepherd", "澳大利亚牧羊犬 / Australian shepherd"),
    ("chow-chow", "松狮犬 / Chow Chow"),
    ("native-chow-chow", "本土松狮犬 / native Chinese Chow Chow"),
]

RESULT_PROMPTS = {
    "yes-or-no": "A smart {breed} wearing a doctoral cap, sitting at a tiny desk, raising one paw to choose between two large simple cards marked YES and NO. The vibe is a dog helping its human play a yes-or-no reasoning game. Important: no turtle, no soup bowl, no seafood, no literal soup imagery.",
    "502": "A {breed} happily clinging to a simplified owner silhouette or owner leg, like a removable sticker stuck on clothing. Add a small 502 glue tube prop nearby and a few clean cartoon glue-drop icons, but avoid slime, bodily fluids, melting, horror, or anything gross.",
    "drama": "A dramatic {breed} actor on a tiny stage under spotlights, holding a small trophy, one paw on chest, exaggerated teary performance expression, velvet curtain hints, no humans.",
    "momo": "A quiet {breed} half-hidden behind a sofa or curtain, wearing a cute flat pink momo-style round mask with simple dot eyes and open smile, only part of the body visible, mysterious low-presence vibe.",
    "Zzzzz": "A {breed} sleeping deeply in an oversized soft dog bed with blanket and pillow, tiny sleep bubbles, peaceful face, alarm clocks around it but ignored. Make it clearly about sleeping, not laziness.",
    "emo": "An anxious {breed} sitting by a closed door, hugging a small blanket, big worried eyes, little rain cloud icon above, a leash and slippers nearby, exaggerated but cute not sad-realistic.",
    "dad": "A stern father-like {breed} wearing square glasses and a neat cardigan or tie, holding a small checklist and pointing at a wall clock, expression serious but funny, household supervision vibe.",
    "salty": "A jealous {breed} hugging a big traditional dark vinegar jar and drinking from it with a straw, cheeks puffed, side-eye expression, tiny floating hearts crossed out around it. Make sure the dog has normal anatomy and no extra human hands.",
    "social": "An extremely outgoing {breed} bursting into a park meetup, greeting several simple background silhouettes with a huge grin, wearing a little bandana like a party host, leash trailing behind.",
    "lazy": "A {breed} completely refusing to move during a walk, belly flat on the ground like a heavy rug, leash gently stretched, tiny wheels or skateboard offered nearby but ignored, expression stubborn and lazy.",
    "taotie": "A foodie {breed} sitting proudly before a ridiculous banquet of safe-looking cartoon dog snacks, chicken pieces, biscuits, empty bowls stacked like trophies, sparkling eyes and open mouth. Funny overeating vibe, not messy or gross.",
    "404-not-found": "A {breed} dashing away off-leash at comic speed, leash end floating in foreground, little dust trail and a simple laptop-like sign in background showing a blank error page shape. Strong runaway energy, funny not scary.",
    "Vme50": "A cute small {breed} pretending to be mildly sick under a tiny blanket, holding a small notebook and pencil like it is keeping a grudge ledger, with a red-and-white fried chicken bucket nearby as a ransom-like prop.",
    "guard": "A serious {breed} working as a neighborhood security guard, wearing a tiny cap and vest, standing by a simple gate booth with a flashlight and walkie-talkie, alert expression toward a parcel silhouette.",
    "8080": "A {breed} dressed like a home renovation worker, wearing a small painter cap and tool belt, holding a small hammer in one paw and a big sledgehammer nearby, standing in front of a half-renovated living room wall with paint roller and tiles.",
    "shift": "A mischievous {breed} treating stylized cartoon poop swirls like rare collectibles in a tiny museum display, wearing a silly explorer hat and holding tongs. Make it abstract, cute, and gross-funny, not realistic or graphic.",
}

STYLE = "flat low-poly geometric character design inspired by classic MBTI 16-personality avatar posters, playful Chinese internet meme tone, pastel background, crisp shapes, polished UI asset quality"


def main() -> None:
    out = ROOT / "assets" / "breed-results" / "generation-queue.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for breed_key, breed_name in BREEDS:
            for result_key, scene in RESULT_PROMPTS.items():
                prompt = (
                    "Use case: stylized-concept\n"
                    "Asset type: DBTI dog personality result illustration\n"
                    f"Primary request: Create one square image for breed variant {breed_name}, result {result_key}.\n"
                    f"Subject and scene: {scene.format(breed=breed_name)}\n"
                    f"Style/medium: {STYLE}.\n"
                    "Composition/framing: centered dog, square 1:1, generous padding, independent single-scene illustration, no collage, no screenshot crop.\n"
                    "Constraints: redraw the dog as the target breed inside the same scene; preserve props, composition, humor, and personality read; do not paste a sticker over an old image.\n"
                    "Avoid: watermark, logos, UI chrome, photorealism, 3D render, extra limbs, distorted anatomy, unreadable text blocks."
                )
                fh.write(json.dumps({
                    "breed": breed_key,
                    "result": result_key,
                    "target": f"assets/breed-results/{breed_key}/{result_key}.jpg",
                    "prompt": prompt,
                }, ensure_ascii=False) + "\n")
    print(out)


if __name__ == "__main__":
    main()

