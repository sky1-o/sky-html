#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成占位 SVG 图片（用于框架预览）。
后续用真实产品图替换 assets/images/ 下同名文件即可，HTML 无需改动。

用法: python tools/gen_placeholders.py
"""

import os
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

# (文件名, 宽度, 高度, 标签, 起始色, 结束色)
IMAGES = [
    ("hero.jpg",            1920, 1080, "HERO — Surface to Design",  "#3A3733", "#8A8175"),
    ("series-ceiling.jpg",   900, 1200, "Surface Ceiling",           "#4A4640", "#9A9086"),
    ("series-cladding.jpg",  900, 1200, "Surface Cladding",          "#3F3B35", "#877D70"),
    ("series-screening.jpg", 900, 1200, "Surface Screening",         "#454139", "#928878"),
    ("series-flooring.jpg",  900, 1200, "Surface Flooring",          "#4E4739", "#A2937C"),
    ("material-wpc.jpg",     800,  600, "WPC",                        "#5A5348", "#B2A794"),
    ("material-spc.jpg",     800,  600, "SPC",                        "#4C4A44", "#9C968A"),
    ("material-pvc.jpg",     800,  600, "PVC / PS",                   "#464239", "#8F8677"),
    ("app-1.jpg",            900,  700, "Residential",                "#4A453D", "#949089"),
    ("app-2.jpg",            900,  700, "Hospitality",                "#3E3A34", "#8B8275"),
    ("app-3.jpg",            900,  700, "Commercial",                 "#514B42", "#A79C8B"),
    ("app-4.jpg",            900,  700, "Facade",                     "#443F38", "#8F867A"),
    ("app-5.jpg",            900,  700, "Interior",                   "#4F4941", "#A09989"),
    ("app-6.jpg",            900,  700, "Outdoor",                    "#3B3833", "#867D71"),
    ("about.jpg",           1000, 1200, "About the brand",            "#494540", "#98938A"),
    ("cta.jpg",             1920,  800, "Start a project",            "#33302B", "#7E7573"),
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <pattern id="lines" width="48" height="48" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
      <line x1="0" y1="0" x2="0" y2="48" stroke="#ffffff" stroke-opacity="0.06" stroke-width="10"/>
    </pattern>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#g)"/>
  <rect width="{w}" height="{h}" fill="url(#lines)"/>
  <g fill="none" stroke="#ffffff" stroke-opacity="0.35" stroke-width="2">
    <rect x="24" y="24" width="{w2}" height="{h2}" rx="2"/>
  </g>
  <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle"
        font-family="Helvetica, Arial, sans-serif" font-size="{fs}"
        letter-spacing="{ls}" fill="#ffffff" fill-opacity="0.82">{label}</text>
  <text x="50%" y="{sy}" text-anchor="middle"
        font-family="Helvetica, Arial, sans-serif" font-size="{fs2}"
        letter-spacing="4" fill="#ffffff" fill-opacity="0.45">PLACEHOLDER · REPLACE ME</text>
</svg>
"""


def build_svg(w, h, label, c1, c2):
    fs = max(18, int(min(w, h) * 0.055))
    fs2 = max(11, int(fs * 0.4))
    return TEMPLATE.format(
        w=w, h=h, w2=w - 48, h2=h - 48,
        label=label, c1=c1, c2=c2,
        fs=fs, ls=max(2, int(fs * 0.08)),
        fs2=fs2, sy=int(h * 0.5) + int(fs * 1.2),
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, w, h, label, c1, c2 in IMAGES:
        svg = build_svg(w, h, label, c1, c2)
        # 以 .svg 实际内容写入，但保留 .jpg 目录占位名会造成类型不符，
        # 因此统一输出为同名 .svg 文件
        out = OUT_DIR / (os.path.splitext(name)[0] + ".svg")
        out.write_text(svg, encoding="utf-8")
        print("generated:", out.name)
    print(f"\nDone. {len(IMAGES)} placeholder SVGs -> {OUT_DIR}")


if __name__ == "__main__":
    main()
