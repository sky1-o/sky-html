# -*- coding: utf-8 -*-
"""
GEMU logo 处理：
1. 去除烙进 JPEG 的浅灰棋盘格背景，恢复 alpha 透明
   （棋盘格两色约 (254,254,254)/(236,236,236)，都是低饱和度灰色；
    logo 主体为棕色/木纹，饱和度明显高于背景，用色度差做遮罩）
2. 按内容裁切 + 留边
3. 输出 assets/images/logo.webp（页头/页脚用）与 assets/images/favicon.png
4. 生成深/浅底合成检查图 tools/_logo_check.png 供人工目检
"""
from PIL import Image
import os

SRC = r"C:\Users\35266\.workbuddy\clipboard-images\clipboard-2026-09-09T11-24-05-727Z-c1004aa5.jpg"
OUT_DIR = r"C:\Users\35266\Desktop\网站\sky的网站\assets\images"
TOOL_DIR = r"C:\Users\35266\Desktop\网站\sky的网站\tools"

im = Image.open(SRC).convert("RGB")
w, h = im.size

# ---- 1. 构建alpha遮罩 ----
# chroma = max(rgb)-min(rgb)：灰背景≈0~4，logo棕色≈30~45，木纹≈25~60
# value = max(rgb)：深色像素无论如何都算前景
px = im.load()
alpha = Image.new("L", (w, h), 0)
ap = alpha.load()

LO, HI = 8.0, 22.0   # chroma 低于8视为背景，高于22视为前景，之间线性过渡
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        chroma = max(r, g, b) - min(r, g, b)
        value = max(r, g, b)
        if chroma >= HI or value <= 190:
            a = 255
        elif chroma <= LO:
            a = 0
        else:
            a = int((chroma - LO) / (HI - LO) * 255)
        ap[x, y] = a

rgba = im.convert("RGBA")
rgba.putalpha(alpha)

# ---- 2. 裁切到内容范围 + 2% 留边 ----
bbox = alpha.getbbox()
if bbox:
    pad_x = int((bbox[2] - bbox[0]) * 0.02)
    pad_y = int((bbox[3] - bbox[1]) * 0.02)
    box = (max(0, bbox[0] - pad_x), max(0, bbox[1] - pad_y),
           min(w, bbox[2] + pad_x), min(h, bbox[3] + pad_y))
    rgba = rgba.crop(box)
print("cropped size:", rgba.size)

# ---- 3. 输出 ----
# logo.webp：高 360px，页头 36px 显示留足 2x/3x 视网膜余量
lh = 360
lw = round(rgba.width * lh / rgba.height)
logo_small = rgba.resize((lw, lh), Image.LANCZOS)
logo_small.save(os.path.join(OUT_DIR, "logo.webp"), "WEBP", quality=90)
print("logo.webp:", logo_small.size)

# favicon.png：192x192，图形缩到 86% 居中，四周留呼吸空间
FS = 192
inner = int(FS * 0.86)
side = min(rgba.width, rgba.height)
sq = rgba.crop((
    (rgba.width - side) // 2, (rgba.height - side) // 2,
    (rgba.width + side) // 2, (rgba.height + side) // 2,
)).resize((inner, inner), Image.LANCZOS)
fav = Image.new("RGBA", (FS, FS), (0, 0, 0, 0))
fav.paste(sq, ((FS - inner) // 2, (FS - inner) // 2), sq)
fav.save(os.path.join(OUT_DIR, "favicon.png"), "PNG")
print("favicon.png:", fav.size)

# ---- 4. 检查图：白底/深底各一半，验证去背干净、无灰边 ----
cw, ch = 900, 500
check = Image.new("RGB", (cw, ch), "white")
check.paste(Image.new("RGB", (cw // 2, ch), (38, 34, 30)), (cw // 2, 0))
test = logo_small.resize((int(lh * 440 / lh * logo_small.width / logo_small.height), 440)) if False else logo_small.resize(
    (round(logo_small.width * 440 / logo_small.height), 440), Image.LANCZOS)
check.paste(test, (30, 30), test)
check.paste(test, (cw // 2 + 30, 30), test)
check.save(os.path.join(TOL := TOOL_DIR, "_logo_check.png"))
print("check saved")
