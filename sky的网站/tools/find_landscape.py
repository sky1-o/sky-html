# -*- coding: utf-8 -*-
"""
在场景文件夹中筛选「横版、高清、曝光正常、偏暖」的图片，
生成候选拼图供人工挑选 Hero / CTA 等大图。
"""
import sys
from pathlib import Path
from PIL import Image, ImageStat, ImageFilter, ImageOps, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contact_sheet import ROOT, list_files, OUT

FOLDERS = [
    "SPC石塑护墙板/10_SPC客厅", "SPC石塑护墙板/11_SPC卧室",
    "SPC石塑护墙板/13_SPC厨房", "SPC石塑护墙板/14_SPC酒店",
    "SPC石塑护墙板/15_SPC办公室商业", "SPC石塑护墙板/12_SPC浴室淋浴房",
]
TAG = {"10_SPC客厅": "LIV", "11_SPC卧室": "BED", "13_SPC厨房": "KIT",
       "14_SPC酒店": "HOT", "15_SPC办公室商业": "OFF", "12_SPC浴室淋浴房": "BAT"}

MIN_W, MIN_AR = 1100, 1.30
N_PER = 6          # 每个文件夹取前 6 名
THUMB, COLS = 190, 6


def quality(im):
    g = im.convert("L")
    stat = ImageStat.Stat(g)
    bright = stat.mean[0]
    sharp = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).stddev[0]
    rgb = ImageStat.Stat(im)
    warmth = rgb.mean[0] - rgb.mean[2]     # R-B，越大越暖
    return bright, sharp, warmth


def main():
    cand = []
    for rel in FOLDERS:
        d = ROOT / rel
        tag = TAG.get(rel.split("/")[-1], rel[:3])
        n = 0
        for p in list_files(d):
            if n >= 400:      # 每个文件夹最多扫 400 张，控制耗时
                break
            try:
                im = Image.open(p)
                w, h = im.size
                if w < MIN_W or w / h < MIN_AR:
                    continue
                im.draft("RGB", (480, 480))
                im = ImageOps.exif_transpose(im).convert("RGB")
                b, s, wa = quality(im)
            except Exception:
                continue
            n += 1
            if not (75 <= b <= 190):      # 过滤过暗/过曝
                continue
            score = s * 1.0 + wa * 0.6 + min(w, 2000) / 40.0
            cand.append((score, tag, p, w, h, round(b), round(s), round(wa)))
    cand.sort(reverse=True)

    picked, seen = [], set()
    for c in cand:
        if c[1] not in seen or sum(1 for x in picked if x[1] == c[1]) < N_PER:
            picked.append(c)
        if len(picked) >= COLS * 4:
            break
    # 每个文件夹最多 N_PER 张
    from collections import Counter
    cnt = Counter()
    final = []
    for c in picked:
        if cnt[c[1]] < N_PER:
            final.append(c); cnt[c[1]] += 1

    TH = THUMB
    PAD, LAB = 6, 20
    rows = (len(final) + COLS - 1) // COLS
    W = COLS * (TH + PAD) + PAD
    H = rows * (TH + LAB + PAD) + PAD + 26
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        tf = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font = tf = ImageFont.load_default()
    dr.text((PAD + 2, 5), f"横版大图候选 — {len(final)} 张", fill="#111111", font=tf)

    for i, (score, tag, p, w, h, b, s, wa) in enumerate(final):
        r, c = divmod(i, COLS)
        x = PAD + c * (TH + PAD)
        y = 26 + PAD + r * (TH + LAB + PAD)
        try:
            im = Image.open(p)
            im.draft("RGB", (TH * 2, TH * 2))
            im = ImageOps.exif_transpose(im).convert("RGB")
            im = ImageOps.fit(im, (TH, TH), Image.LANCZOS)
            sheet.paste(im, (x, y))
        except Exception:
            dr.rectangle([x, y, x + TH, y + TH], fill="#EEEEEE")
        dr.rectangle([x, y, x + TH, y + LAB], fill="#111111")
        dr.text((x + 4, y + 2), f"{tag}{i:02d} {w}x{h}", fill="#FFFFFF", font=font)
        print(f"{tag}{i:02d}  {p.name[:40]:42s} {w}x{h}  亮度{b} 锐度{s} 暖度{wa}")

    out = OUT / "sheet-F-landscape.jpg"
    sheet.save(out, quality=88)
    print("\n->", out)


if __name__ == "__main__":
    main()
