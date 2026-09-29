#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把源站文件同步到 dist/ 部署目录（dist/ 才是线上发布根目录）。

用法：
    python tools/sync_dist.py           # 仅同步
    python tools/sync_dist.py --bump    # 同步，并把 sitemap.xml 的 lastmod 更新为今天

为什么需要它：
    dist/ 是部署根目录（EdgeOne Pages / OSS 都以它为根），此前靠手工复制，
    极易出现「源文件改了、线上还是旧版」或「漏拷 robots.txt / llms.txt」的问题。
    本脚本把同步变成一条命令，并在结束时做一次一致性自检。

同步范围：
    index.html, assets/**, robots.txt, sitemap.xml, llms.txt
    → dist/                                   （部署根）
    → dist/.edgeone/assets/                   （EdgeOne 构建缓存目录）

不触碰：
    dist/.edgeone/.edgeone-assets-config.json（平台配置）
    dist/.env                                 （平台注入的环境文件）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import filecmp
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
EDGEONE_INDEX_DIR = DIST / ".edgeone" / "assets"

SINGLE_FILES = ["index.html", "robots.txt", "sitemap.xml", "llms.txt"]
DIRS = ["assets"]


def bump_sitemap_lastmod() -> None:
    """把根目录 sitemap.xml 的 lastmod 改成今天（源与目标始终一致）。"""
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        return
    today = _dt.date.today().isoformat()
    text = sm.read_text(encoding="utf-8")
    new = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{today}</lastmod>", text)
    if new != text:
        sm.write_text(new, encoding="utf-8")
        print(f"[bump] sitemap.xml lastmod -> {today}")


def copy_file(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and filecmp.cmp(src, dst, shallow=False):
        return "same"
    shutil.copy2(src, dst)
    return "updated" if dst.exists() else "new"


def copy_tree(src_dir: Path, dst_dir: Path) -> tuple[int, int]:
    """返回 (写入/更新文件数, 未变化文件数)。"""
    changed = same = 0
    for src in sorted(src_dir.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(src_dir)
        r = copy_file(src, dst_dir / rel)
        if r == "same":
            same += 1
        else:
            changed += 1
    return changed, same


def targets() -> list[Path]:
    out = [DIST]
    if EDGEONE_INDEX_DIR.exists():
        out.append(EDGEONE_INDEX_DIR)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bump", action="store_true", help="把 sitemap.xml 的 lastmod 更新为今天")
    args = ap.parse_args()

    if not ROOT.joinpath("index.html").exists():
        print(f"[x] 找不到源文件：{ROOT / 'index.html'}")
        return 1

    if args.bump:
        bump_sitemap_lastmod()

    total_changed = total_same = 0
    for dest in targets():
        changed = same = 0
        for name in SINGLE_FILES:
            src = ROOT / name
            if not src.exists():
                print(f"[!] 源文件缺失，跳过：{name}")
                continue
            r = copy_file(src, dest / name)
            changed += r != "same"
            same += r == "same"
        for d in DIRS:
            src_dir = ROOT / d
            if src_dir.is_dir():
                c, s = copy_tree(src_dir, dest / d)
                changed += c
                same += s
        total_changed += changed
        total_same += same
        print(f"[ok] {dest.relative_to(ROOT)} -> 更新 {changed} 个文件，未变化 {same} 个")

    print(f"\n完成：共更新 {total_changed} 个，未变化 {total_same} 个。")

    # ---- 自检 1：dist/index.html 是否与源一致 ----
    a, b = ROOT / "index.html", DIST / "index.html"
    if a.exists() and b.exists():
        print("[check] dist/index.html 与源一致" if filecmp.cmp(a, b, shallow=False)
              else "[check][x] dist/index.html 与源不一致！")

    # ---- 自检 2：index.html 里引用的本地图片是否都存在 ----
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    refs = {
        m.split("?")[0]
        for m in re.findall(r'(?:src|href)="([^"]+)"', html)
        if not m.startswith(("http", "#", "mailto:", "tel:", "data:"))
    }
    missing = sorted(r for r in refs if not (ROOT / r).exists())
    print(f"[check] 本地资源引用 {len(refs)} 个，缺失 {len(missing)} 个"
          + (f"：{missing}" if missing else " ✅"))

    # ---- 自检 3：dist/assets 里是否有源目录已不存在的残留文件 ----
    stale = []
    for d in DIRS:
        src_dir, dst_dir = ROOT / d, DIST / d
        if src_dir.is_dir() and dst_dir.is_dir():
            for f in dst_dir.rglob("*"):
                if f.is_file() and not (src_dir / f.relative_to(dst_dir)).exists():
                    stale.append(str(f.relative_to(DIST)))
    print(f"[check] dist 残留文件 {len(stale)} 个" + (f"：{stale}" if stale else " ✅"))

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
