# -*- coding: utf-8 -*-
"""
WPC 材料卡图片：从站内 series-wood.webp（胡桃木格栅实拍）做差异化裁切
（放大取纹理细节区 + 水平镜像，与上方系列卡视觉区分）
用法: <venv-python> tools/make_wpc_img.py
"""
from pathlib import Path
from PIL import Image, ImageOps

SITE = Path(__file__).resolve().parent.parent
SRC = SITE / "assets" / "images" / "series-wood.webp"
OUT = SITE / "assets" / "images" / "material-wpc.webp"

im = Image.open(SRC).convert("RGB")
w, h = im.size  # 1000x1000

# 66% 放大裁切，偏向右侧木纹结疤区（细节更丰富）
box = 660
x0, y0 = 250, 140
crop = im.crop((x0, y0, min(x0 + box, w), min(y0 + box, h)))
crop = ImageOps.mirror(crop)                       # 镜像，避免与系列卡雷同
crop = crop.resize((800, 800), Image.LANCZOS)      # 卡片标称 800x800
crop.save(OUT, "WEBP", quality=82, method=6)
print(f"{OUT}  {crop.size[0]}x{crop.size[1]}  {OUT.stat().st_size/1024:.1f} KB")
