#!/usr/bin/env python3
"""Create the IMRE/MOF Dobot reference overlay for the documented PTZ pose.

The polygons are presentation annotations for the 2560x1440 reference pose
(azimuth/elevation/zoom camera units 749/573/10). They are not robot
coordinates, calibration, or reusable current-run occupancy evidence.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 2560
HEIGHT = 1440

COLORS = {
    "occupied": (239, 68, 68, 230),
    "obstructed": (249, 115, 22, 230),
    "fixed": (156, 163, 175, 230),
    "boundary": (229, 231, 235, 235),
}

REGIONS = [
    (
        "TUBE-RACK: OCCUPIED",
        "occupied",
        [(806, 748), (1014, 735), (1024, 1030), (802, 1045)],
        (800, 700),
    ),
    (
        "BIOSHAKE: OCCUPIED",
        "occupied",
        [(525, 790), (795, 775), (820, 1260), (510, 1265)],
        (500, 760),
    ),
    (
        "CENTRIFUGE-1: OCCUPIED",
        "occupied",
        [(1000, 955), (1300, 950), (1315, 1380), (984, 1380)],
        (930, 875),
    ),
    (
        "CENTRIFUGE-2: OCCUPIED",
        "occupied",
        [(1300, 940), (1655, 920), (1664, 1380), (1315, 1380)],
        (1420, 875),
    ),
    (
        "CAP-QBOT: NOT FULLY VISIBLE",
        "obstructed",
        [(1580, 500), (2075, 500), (2110, 1155), (1555, 1155)],
        (1570, 465),
    ),
    (
        "DOBOT BODY: FIXED / OCCLUDING",
        "fixed",
        [(1090, 0), (1840, 0), (1840, 370), (1525, 960), (1160, 960), (1075, 280)],
        (1160, 150),
    ),
]

OUTER_BOUNDARY = [(345, 75), (2315, 75), (2475, 1415), (278, 1415)]
TRANSFER_CORRIDOR = [(820, 265), (1685, 230), (1905, 1190), (760, 1215)]


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color: tuple[int, ...]) -> None:
    text_font = font(30)
    bbox = draw.textbbox(xy, text, font=text_font, stroke_width=1)
    pad = 10
    background = (3, 7, 18, 220)
    draw.rounded_rectangle(
        (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad),
        radius=8,
        fill=background,
        outline=color,
        width=3,
    )
    draw.text(xy, text, font=text_font, fill=color, stroke_width=1, stroke_fill=(0, 0, 0, 255))


def annotate(source: Path, output: Path) -> None:
    image = Image.open(source).convert("RGBA")
    if image.size != (WIDTH, HEIGHT):
        raise ValueError(f"Expected {WIDTH}x{HEIGHT} reference frame, got {image.width}x{image.height}")

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.line(OUTER_BOUNDARY + [OUTER_BOUNDARY[0]], fill=COLORS["boundary"], width=8, joint="curve")
    label(draw, (390, 110), "VISIBLE CELL / WORKSPACE BOUNDARY", COLORS["boundary"])

    draw.line(
        TRANSFER_CORRIDOR + [TRANSFER_CORRIDOR[0]],
        fill=COLORS["obstructed"],
        width=7,
        joint="curve",
    )

    # Draw geometry first so later region polygons cannot cover earlier labels.
    for _, state, polygon, _ in REGIONS:
        color = COLORS[state]
        draw.polygon(polygon, fill=(*color[:3], 28), outline=color, width=7)

    # Draw all labels last so every label remains readable over overlapping fixtures.
    for text, state, _, label_xy in REGIONS:
        label(draw, label_xy, text, COLORS[state])
    label(draw, (865, 285), "TRANSFER CORRIDOR: PARTLY HIDDEN", COLORS["obstructed"])

    title_font = font(34)
    title = "REFERENCE POSE ONLY — fresh image required for every validation"
    title_box = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_box[2] - title_box[0]
    draw.rounded_rectangle((1280 - title_width // 2 - 22, 18, 1280 + title_width // 2 + 22, 72), radius=10, fill=(3, 7, 18, 230))
    draw.text((1280 - title_width // 2, 25), title, font=title_font, fill=(255, 255, 255, 255))

    legend_y = 1345
    legend = [
        ("OCCUPIED", COLORS["occupied"]),
        ("NOT FULLY VISIBLE", COLORS["obstructed"]),
        ("FIXED", COLORS["fixed"]),
    ]
    x = 370
    draw.rounded_rectangle((340, 1322, 2160, 1410), radius=12, fill=(3, 7, 18, 220), outline=(75, 85, 99, 255), width=2)
    legend_font = font(28)
    for text, color in legend:
        draw.rectangle((x, legend_y, x + 35, legend_y + 28), fill=color)
        draw.text((x + 50, legend_y - 3), text, font=legend_font, fill=(245, 245, 245, 255))
        x += 480 if text != "NOT FULLY VISIBLE" else 660

    output.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(image, overlay).convert("RGB").save(output, quality=94, subsampling=0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    annotate(args.source, args.output)


if __name__ == "__main__":
    main()
