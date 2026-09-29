# -*- coding: utf-8 -*-
"""
为 About 区块（4:3，1000x750）筛选候选图：
- 来源：10_SPC客厅 + 11_SPC卧室（空间应用场景，契合 "Surfaces that shape how a space feels"）
- 硬条件：横图、宽>=1200、宽高比 1.2~1.5（接近4:3，裁切损失小）
- 排除已被 hero/cta/app 槽位占用的文件
输出 tools/sheets/about-candidates.jpg 拼图供目检
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path("F:/护墙板/SPC石塑护墙板")
OUT = Path(__file__).resolve().parent / "sheets" / "about-candidates.jpg"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}
USED = {"SPC-LIVING-000469.jpg", "SPC-LIVING-000200.jpg", "SPC-LIVING-000229.png",
        "SPC-BEDROOM-000436.jpg"}

FOLDERS = [ROOT / "10_SPC客厅", ROOT / "11_SPC卧室"]

cands = []
for d in FOLDERS:
    tag = "LIV" if "客厅" in d.name else "BED"
    for p in sorted(d.iterdir()):
        if p.suffix.lower() not in EXTS or p.name in USED:
            continue
        try:
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            continue
        if w < 1200 or not (1.2 <= w / h <= 1.5):
            continue
        cands.append((tag, p, w, h))

print(f"候选 {len(cands)} 张")
cands = cands[:24]

THUMB, COLS = 300, 4
ROWS = (len(cands) + COLS - 1) // COLS
PAD, LABEL = 8, 26
sheet = Image.new("RGB", (COLS * (THUMB + PAD) + PAD, ROWS * (THUMB + LABEL + PAD) + PAD), "white")
draw = ImageDraw.Draw(sheet)

for i, (tag, p, w, h) in enumerate(cands):
    try:
        with Image.open(p) as im:
            im = im.convert("RGB")
            im.thumbnail((THUMB, THUMB))
        cx, cy = PAD + (i % COLS) * (THUMB + PAD), PAD + (i // COLS) * (THUMB + LABEL + PAD)
        sheet.paste(im, (cx + (THUMB - im.width) // 2, cy + (THUMB - im.height) // 2))
        draw.text((cx, cy + THUMB + 4), f"#{i:02d} {tag} {p.name[:28]} {w}x{h}", fill="black")
    except Exception as e:
        print("skip", p.name, e)

sheet.save(OUT, quality=82)
print("saved:", OUT, sheet.size)
for i, (tag, p, w, h) in enumerate(cands):
    print(f"#{i:02d} {tag} {p}")
