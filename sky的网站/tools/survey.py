# -*- coding: utf-8 -*-
"""快速统计各文件夹图片的尺寸/比例分布，决定裁切策略。"""
import os, random, json
from pathlib import Path
from PIL import Image

ROOT = Path("F:/护墙板")
FOLDERS = [
    "PVC护墙板/PVC平板墙板", "PVC护墙板/PVC木纹墙板", "PVC护墙板/PVC格栅墙板",
    "PVC护墙板/PVC立体墙板", "PVC护墙板/PVC长城板", "PVC护墙板/大理石纹墙板",
    "SPC石塑护墙板/02_SPC产品细节图", "SPC石塑护墙板/03_SPC大理石纹",
    "SPC石塑护墙板/04_SPC木纹", "SPC石塑护墙板/05_SPC石纹",
    "SPC石塑护墙板/06_SPC水泥工业纹", "SPC石塑护墙板/07_SPC格栅长城Fluted",
    "SPC石塑护墙板/08_SPC_3D立体纹", "SPC石塑护墙板/09_SPC纯色",
    "SPC石塑护墙板/10_SPC客厅", "SPC石塑护墙板/11_SPC卧室",
    "SPC石塑护墙板/12_SPC浴室淋浴房", "SPC石塑护墙板/13_SPC厨房",
    "SPC石塑护墙板/14_SPC酒店", "SPC石塑护墙板/15_SPC办公室商业",
    "SPC石塑护墙板/16_SPC安装施工", "SPC石塑护墙板/17_SPC产品结构",
    "SPC石塑护墙板/18_SPC工厂生产", "SPC石塑护墙板/19_SPC包装装柜",
    "SPC石塑护墙板/20_SPC颜色样板",
]

EXTS = {".jpg", ".jpeg", ".png", ".webp"}
random.seed(42)

print(f"{'文件夹':<34}{'样本':>5}{'宽中位数':>9}{'高中位数':>9}{'比例中位数':>10}  比例分布")
print("-" * 96)

for rel in FOLDERS:
    d = ROOT / rel
    if not d.is_dir():
        print(f"{rel:<34}  [缺失]")
        continue
    files = [p for p in d.iterdir() if p.suffix.lower() in EXTS]
    if not files:
        continue
    sample = random.sample(files, min(60, len(files)))
    ws, hs, ars = [], [], []
    for p in sample:
        try:
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            continue
        ws.append(w); hs.append(h); ars.append(round(w / h, 2))
    if not ws:
        continue
    ws.sort(); hs.sort(); ars.sort()
    mw, mh, ma = ws[len(ws)//2], hs[len(hs)//2], ars[len(ars)//2]
    land = sum(1 for a in ars if a > 1.15)
    sqr  = sum(1 for a in ars if 0.85 <= a <= 1.15)
    port = sum(1 for a in ars if a < 0.85)
    n = len(ars)
    print(f"{rel.split('/')[-1]:<34}{n:>5}{mw:>9}{mh:>9}{ma:>10}  横{land*100//n}% 方{sqr*100//n}% 竖{port*100//n}%")
