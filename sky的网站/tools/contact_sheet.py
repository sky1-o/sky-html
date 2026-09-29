# -*- coding: utf-8 -*-
"""
从图库采样生成带编号的拼图（contact sheet），供人工目检选图。
用法: python tools/contact_sheet.py
输出: tools/sheets/sheet-*.jpg
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path("F:/护墙板")
OUT = Path(__file__).resolve().parent / "sheets"
OUT.mkdir(exist_ok=True)
EXTS = {".jpg", ".jpeg", ".png", ".webp"}
random.seed(7)

THUMB = 190       # 单格边长
COLS, ROWS = 6, 4
PAD = 6
LABEL_H = 18

# (sheet 名, [(短代号, 文件夹相对路径), ...], 每个文件夹取几张)
GROUPS = [
    ("A-纹理产品", [
        ("FLU", "SPC石塑护墙板/07_SPC格栅长城Fluted"),
        ("WOD", "SPC石塑护墙板/04_SPC木纹"),
        ("MAR", "SPC石塑护墙板/03_SPC大理石纹"),
        ("STO", "SPC石塑护墙板/05_SPC石纹"),
        ("CEM", "SPC石塑护墙板/06_SPC水泥工业纹"),
        ("3D",  "SPC石塑护墙板/08_SPC_3D立体纹"),
        ("DET", "SPC石塑护墙板/02_SPC产品细节图"),
        ("STR", "SPC石塑护墙板/17_SPC产品结构"),
        ("COL", "SPC石塑护墙板/20_SPC颜色样板"),
        ("PVCf", "PVC护墙板/PVC平板墙板"),
        ("PVCw", "PVC护墙板/PVC木纹墙板"),
        ("PVCg", "PVC护墙板/PVC格栅墙板"),
        ("PVC3", "PVC护墙板/PVC立体墙板"),
        ("PVCc", "PVC护墙板/PVC长城板"),
        ("PVCm", "PVC护墙板/大理石纹墙板"),
    ], 4),

    ("B-场景空间", [
        ("LIV", "SPC石塑护墙板/10_SPC客厅"),
        ("BED", "SPC石塑护墙板/11_SPC卧室"),
        ("BAT", "SPC石塑护墙板/12_SPC浴室淋浴房"),
        ("KIT", "SPC石塑护墙板/13_SPC厨房"),
        ("HOT", "SPC石塑护墙板/14_SPC酒店"),
        ("OFF", "SPC石塑护墙板/15_SPC办公室商业"),
    ], 4),

    ("C-工厂实拍", [
        ("INS", "SPC石塑护墙板/16_SPC安装施工"),
        ("FAC", "SPC石塑护墙板/18_SPC工厂生产"),
        ("PKG", "SPC石塑护墙板/19_SPC包装装柜"),
    ], 6),
]


def list_files(d: Path):
    return sorted([p for p in d.iterdir() if p.suffix.lower() in EXTS])


def spread(files, n):
    """均匀取样，兼顾头部（通常是精选）"""
    if len(files) <= n:
        return files
    head = files[:2]
    rest = files[2:]
    k = max(0, n - len(head))
    step = max(1, len(rest) // k) if k else 1
    return head + rest[::step][:k]


def trim_white(im, tol=18):
    """裁掉接近纯白的边缘（产品白底图常见）"""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    def row_white(y):
        return all(px[x, y] > 255 - tol for x in range(0, w, max(1, w // 80)))
    def col_white(x):
        return all(px[x, y] > 255 - tol for y in range(0, h, max(1, h // 80)))
    top = 0
    while top < h // 3 and row_white(top): top += 1
    bot = h - 1
    while bot > 2 * h // 3 and row_white(bot): bot -= 1
    left = 0
    while left < w // 3 and col_white(left): left += 1
    right = w - 1
    while right > 2 * w // 3 and col_white(right): right -= 1
    if right - left > 40 and bot - top > 40:
        return im.crop((left, top, right + 1, bot + 1))
    return im


def build_sheet(name, sources, per_folder):
    cells = []
    for code, rel in sources:
        d = ROOT / rel
        if not d.is_dir():
            continue
        files = spread(list_files(d), per_folder)
        for i, p in enumerate(files):
            cells.append((f"{code}{i:02d}", p))
    # 截断到 COLS*ROWS
    cells = cells[: COLS * ROWS]
    W = COLS * (THUMB + PAD) + PAD
    H = ROWS * (THUMB + LABEL_H + PAD) + PAD + 26
    sheet = Image.new("RGB", (W, H), "#FFFFFF")
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        title_font = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font = title_font = ImageFont.load_default()
    dr.text((PAD + 2, 5), f"{name}  —  {len(cells)} 张候选", fill="#111111", font=title_font)

    for idx, (label, p) in enumerate(cells):
        r, c = divmod(idx, COLS)
        x = PAD + c * (THUMB + PAD)
        y = 26 + PAD + r * (THUMB + LABEL_H + PAD)
        try:
            im = Image.open(p)
            im.draft("RGB", (THUMB * 2, THUMB * 2))
            im = ImageOps.exif_transpose(im).convert("RGB")
            # 长边缩到 THUMB，再居中裁方
            im = ImageOps.contain(im, (THUMB, THUMB))
            im = ImageOps.fit(im, (THUMB, THUMB), Image.LANCZOS)
            sheet.paste(im, (x, y))
        except Exception as e:
            dr.rectangle([x, y, x + THUMB, y + THUMB], fill="#EEEEEE")
            dr.text((x + 4, y + 4), "ERR", fill="#CC0000", font=font)
        dr.rectangle([x, y, x + THUMB, y + LABEL_H], fill="#111111")
        dr.text((x + 4, y + 2), label, fill="#FFFFFF", font=font)
    out = OUT / f"sheet-{name.split('-')[0]}.jpg"
    sheet.save(out, quality=88)
    print(f"{out}  ({len(cells)} 格, {W}x{H})")


if __name__ == "__main__":
    for g in GROUPS:
        build_sheet(*g)
