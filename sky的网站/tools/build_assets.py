# -*- coding: utf-8 -*-
"""
按选定清单处理图库图片 → 裁切 / 缩放 / 压缩 → 输出 WebP 到 assets/images/
用法: python tools/build_assets.py
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contact_sheet import ROOT, spread, list_files

SITE = Path(__file__).resolve().parent.parent
OUTDIR = SITE / "assets" / "images"
OUTDIR.mkdir(parents=True, exist_ok=True)

# (输出名, 来源相对目录, 精确文件名或 spread 索引, 目标宽, 目标高, 是否裁白边)
PLAN = [
    ("hero",            "SPC石塑护墙板/10_SPC客厅",  "SPC-LIVING-000469.jpg", 1920, 1080, False),
    ("cta",             "SPC石塑护墙板/10_SPC客厅",  "SPC-LIVING-000200.jpg", 1600,  900, False),
    ("about",           "SPC石塑护墙板/18_SPC工厂生产", "SPC-FACTORY-000002.jpg", 1000, 750, False),
    ("app-residential", "SPC石塑护墙板/10_SPC客厅",  "SPC-LIVING-000229.png",  900,  675, False),
    ("app-hospitality", "SPC石塑护墙板/15_SPC办公室商业", "SPC-OFFICE-000046.jpg", 900, 675, False),
    ("app-commercial",  "SPC石塑护墙板/15_SPC办公室商业", "SPC-OFFICE-000206.jpg", 900, 675, False),
    ("app-wet",         "SPC石塑护墙板/12_SPC浴室淋浴房", "SPC-BATH-000200.jpg",  900,  675, False),
    ("app-kitchen",     "SPC石塑护墙板/13_SPC厨房",  "SPC-KITCHEN-000053.jpg",  900,  675, False),
    ("app-bedroom",     "SPC石塑护墙板/11_SPC卧室",  "SPC-BEDROOM-000436.jpg",  900,  675, False),
    ("series-fluted",   "PVC护墙板/PVC格栅墙板",     2,  1000, 1000, True),
    ("series-wood",     "PVC护墙板/PVC木纹墙板",     1,  1000, 1000, True),
    ("series-marble",   "PVC护墙板/大理石纹墙板",    1,  1000, 1000, True),
    ("series-3d",       "SPC石塑护墙板/08_SPC_3D立体纹", 3, 1000, 1000, True),
    ("material-pvc",    "PVC护墙板/PVC平板墙板",     2,   800,  800, True),
    ("material-spc",    "SPC石塑护墙板/05_SPC石纹",  2,   800,  800, True),
    ("material-finish", "PVC护墙板/PVC长城板",       3,   800,  800, True),
]


def trim_white(im, tol=16):
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    sx = max(1, w // 100)
    sy = max(1, h // 100)
    thr = 255 - tol
    top = 0
    while top < h // 2 and all(px[x, top] > thr for x in range(0, w, sx)): top += 1
    bot = h - 1
    while bot > top and all(px[x, bot] > thr for x in range(0, w, sx)): bot -= 1
    left = 0
    while left < w // 2 and all(px[left, y] > thr for y in range(0, h, sy)): left += 1
    right = w - 1
    while right > left and all(px[right, y] > thr for y in range(0, h, sy)): right -= 1
    if (right - left) > w * 0.25 and (bot - top) > h * 0.25:
        return im.crop((left, top, right + 1, bot + 1))
    return im


def resolve(rel, key):
    d = ROOT / rel
    if isinstance(key, int):
        fs = spread(list_files(d), 4)
        return fs[key]
    return d / key


def process(name, path, tw, th, do_trim):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")

    src_w, src_h = im.size
    if do_trim:
        im = trim_white(im)

    # 居中裁到目标比例（若源比例差异大，向中心裁）
    target_ar = tw / th
    w, h = im.size
    ar = w / h
    if abs(ar - target_ar) > 0.01:
        if ar > target_ar:                    # 源更宽 → 裁两侧
            nw = int(h * target_ar)
            x0 = (w - nw) // 2
            im = im.crop((x0, 0, x0 + nw, h))
        else:                                 # 源更高 → 裁上下（略偏上，保主体）
            nh = int(w / target_ar)
            y0 = int((h - nh) * 0.42)
            im = im.crop((0, y0, w, y0 + nh))

    # 只缩小、不放大
    if im.size[0] > tw:
        im = im.resize((tw, th), Image.LANCZOS)
    else:
        im = ImageOps.fit(im, (max(im.size[0], 1), int(im.size[0] / target_ar)), Image.LANCZOS)

    out = OUTDIR / f"{name}.webp"
    q = 82
    im.save(out, "WEBP", quality=q, method=6)
    kb = out.stat().st_size / 1024
    print(f"{name:18s} {src_w}x{src_h} -> {im.size[0]}x{im.size[1]}  {kb:6.1f} KB  <- {path.name[:36]}")
    return out, im.size, kb


if __name__ == "__main__":
    total = 0
    for name, rel, key, tw, th, trim in PLAN:
        p = resolve(rel, key)
        if not p.exists():
            print(f"{name:18s} [找不到] {p}")
            continue
        _, _, kb = process(name, p, tw, th, trim)
        total += kb
    print(f"\n合计 {total:.0f} KB -> {OUTDIR}")
