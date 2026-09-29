# -*- coding: utf-8 -*-
"""
专筛「高级感」首屏候选：暗调、极简、大理石/石纹、画面下方留白多（适合压字）。
输出大尺寸拼图 tools/sheets/sheet-premium.jpg
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat, ImageFilter

sys_root = Path("F:/护墙板/SPC石塑护墙板")
OUT = Path(__file__).resolve().parent / "sheets"

FOLDERS = ["10_SPC客厅", "11_SPC卧室", "12_SPC浴室淋浴房", "13_SPC厨房",
           "14_SPC酒店", "15_SPC办公室商业", "06_SPC水泥工业纹", "05_SPC石纹"]
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def metrics(im):
    g = im.convert("L")
    w, h = g.size
    stat = ImageStat.Stat(g)
    bright = stat.mean[0]
    sharp = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).stddev[0]
    # 下方 35% 区域的均匀度（越低越适合压字）
    bottom = g.crop((0, int(h * 0.65), w, h)).resize((160, 60))
    bs = ImageStat.Stat(bottom.filter(ImageFilter.FIND_EDGES)).stddev[0]
    rgb = ImageStat.Stat(im)
    warmth = rgb.mean[0] - rgb.mean[2]
    sat = ImageStat.Stat(im.convert("HSV")).mean[1]
    return bright, sharp, bs, warmth, sat


def main():
    cand = []
    for f in FOLDERS:
        d = sys_root / f
        if not d.is_dir():
            continue
        files = sorted([p for p in d.iterdir() if p.suffix.lower() in EXTS])
        step = max(1, len(files) // 700)
        n = 0
        for p in files[::step]:
            try:
                im = Image.open(p)
                w, h = im.size
                if w < 1400 or w / h < 1.40:
                    continue
                im.draft("RGB", (480, 480))
                im = ImageOps.exif_transpose(im).convert("RGB")
                b, s, bs, wa, sat = metrics(im)
            except Exception:
                continue
            n += 1
            if not (58 <= b <= 135):      # 暗调
                continue
            if sat > 95:                  # 过艳过滤
                continue
            score = (135 - b) * 0.6 + s * 0.9 + (60 - min(bs, 60)) * 1.4 + min(w, 3000) / 55.0
            cand.append((score, f[:3], p, w, h, round(b), round(s), round(bs)))
        print(f"{f}: 扫描 {n} 张横版")
    cand.sort(reverse=True)

    from collections import Counter
    cnt = Counter(); picked = []
    for c in cand:
        if cnt[c[1]] < 5:
            picked.append(c); cnt[c[1]] += 1
        if len(picked) >= 30:
            break

    T, COLS, PAD, LAB = 300, 5, 6, 24
    ROWS = (len(picked) + COLS - 1) // COLS
    W = COLS * (T + PAD) + PAD
    H = ROWS * (T + LAB + PAD) + PAD + 26
    sh = Image.new("RGB", (W, H), "#FFFFFF")
    dr = ImageDraw.Draw(sh)
    try:
        fo = ImageFont.truetype("arial.ttf", 14); tf = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        fo = tf = ImageFont.load_default()
    dr.text((PAD + 2, 5), f"高级感首屏候选 — {len(picked)} 张（暗调/极简/下方留白）", fill="#111111", font=tf)

    names = []
    for i, (sc, tag, p, w, h, b, s, bs) in enumerate(picked):
        r, c = divmod(i, COLS)
        x = PAD + c * (T + PAD); y = 26 + PAD + r * (T + LAB + PAD)
        im = Image.open(p); im.draft("RGB", (T * 2, T * 2))
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = ImageOps.fit(im, (T, int(T * 9 / 16)), Image.LANCZOS)
        sh.paste(im, (x, y))
        lbl = f"{tag}{i:02d}"
        names.append((lbl, str(p)))
        dr.rectangle([x, y + im.size[1], x + T, y + LAB + im.size[1]], fill="#111111")
        dr.text((x + 5, y + im.size[1] + 4), f"{lbl} {w}x{h}", fill="#FFFFFF", font=fo)
    out = OUT / "sheet-premium.jpg"
    sh.save(out, quality=90)
    (OUT / "premium_map.txt").write_text("\n".join(f"{a}={b2}" for a, b2 in names), encoding="utf-8")
    print("->", out, sh.size)


if __name__ == "__main__":
    main()
