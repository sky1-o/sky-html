# GEMU® Surface — 站点框架

与 https://www.hauscore.ph/ 视觉风格与页面结构对齐的响应式静态站点框架。
纯 HTML + CSS + 原生 JS，**零构建、零依赖**，可直接部署到任意静态托管平台。

---

## 一、目录结构

```
sky的网站/
├── index.html              # 唯一页面（单页结构），所有区块在此编辑  ← 唯一要改的源文件
├── assets/
│   ├── css/style.css        # 全部样式：设计令牌 → 组件 → 区块 → 断点
│   ├── js/main.js           # 交互：粘性页头/抽屉菜单/滚动揭示/FAQ/轮播
│   └── images/*.webp        # 18 张真实素材（WebP，共约 1.1 MB）
├── robots.txt               # 爬虫规则：放行搜索引擎 + 全部主流 AI 抓取器
├── sitemap.xml              # 站点地图（lastmod 由同步脚本自动更新）
├── llms.txt                 # 给 AI 引擎的「品牌事实清单」（GEO）
├── tools/
│   ├── sync_dist.py         # ★ 改完源文件后跑这个同步到 dist/ 并自检
│   └── gen_placeholders.py  # 占位图生成脚本（历史遗留，已不需要）
├── dist/                    # 部署根目录（发布用；由 sync_dist.py 生成，别手改）
├── SEO-GEO-分析报告.html     # SEO & GEO 审计报告（当前 v2）
├── DEPLOY.md                # 部署上线分步指南  ← 部署看这个
└── README.md                # 本文件
```

**改完网站如何发布（三步）**：

```bash
python tools/sync_dist.py --bump     # 1. 同步到 dist/，并把 sitemap 的 lastmod 改成今天
#                                    #    脚本会自动报告：副本是否一致 / 图片路径是否失效 / dist 有无残留
# 2. 在 WorkBuddy 里重新发布（或把 dist/ 上传到你的主机）
```

> `dist/` 是部署根目录，`robots.txt` / `sitemap.xml` / `llms.txt` 必须位于它的根层。
> 不要手工往 `dist/` 复制文件——容易漏、容易旧，统一走 `sync_dist.py`。

---

## 二、页面区块（自上而下，与参考站一致）

| # | 区块 | id | 说明 |
|---|------|----|------|
| 1 | Header 页头 | `#header` | 透明 → 滚动后转为白底毛玻璃；桌面导航 + 移动汉堡 |
| 2 | Hero 首屏 | — | 全屏大图 + `Surface to Design.` + 双 CTA + 4 项数据 |
| 3 | 品牌宣言 | `#about` | 左右分栏：大标题 + 三段正文 |
| 4 | 四大系列 | `#series` | 4 张竖版卡片：Ceiling / Cladding / Screening / Flooring |
| 5 | 能力优势 | — | 4 列图标 + 文案（防潮防蚁 / 15 年质保 / 隐藏卡扣 / 工程供货） |
| 6 | 材料对比 | `#materials` | WPC / SPC / PVC / Profiles 四卡 + 参数表；下方另有 3 个产品预留位 |
| 7 | 应用场景 | `#applications` | 6 图宫格画廊 |
| 8 | 流程 | `#process` | 深色区块，4 步（Specify → Sample → Confirm → Deliver） |
| 9 | 客户证言 | — | 自动轮播 + 指示点，悬停暂停 |
| 10 | FAQ | `#faq` | 手风琴，单开模式，**6 条问答，与 JSON-LD FAQPage 必须同步维护** |
| 11 | CTA 横幅 | `#contact` | 全宽深底 + 双按钮 |
| 12 | Footer 页脚 | — | 4 列 + 版权条（法务三项目前为占位，待建真实页面） |

---

## 三、响应式策略

**移动优先（min-width 递增）**，三档断点：

| 断点 | 目标设备 | 主要变化 |
|------|----------|----------|
| `< 640px` | 手机 | 单列；汉堡菜单；导航隐藏 |
| `≥ 640px` | 平板竖屏 | 系列 2 列；优势 2 列；页脚 2 列；数据条 4 列 |
| `≥ 900px` | 平板横屏 / 小桌面 | **显示桌面导航、隐藏汉堡**；系列 4 列；画廊 3 列；开启 12 栅格 |
| `≥ 1280px` | 大桌面 | 内容封顶 1440px，间距拉到最大 |

关键技术点：
- **流体排版**：`clamp()` 让字号/间距随视口连续缩放，断点只负责"列数"切换。
- **CSS Grid + 12 栅格**：`.grid` + `.col-3/4/6/8`，移动端全部 `span 12`。
- **100svh**：首屏高度用 `svh` 而非 `vh`，避免移动端浏览器地址栏跳动。
- **aspect-ratio**：所有图片容器锁定宽高比，杜绝布局抖动（CLS）。
- **无横向滚动**：`overflow-x: hidden` + `minmax(0, 1fr)` 防止 Grid 子项撑破容器。

---

## 四、本地预览

```bash
# 方式一：Python（已内置）
python -m http.server 8080

# 方式二：Node
npx serve .

# 方式三：VS Code 插件 Live Server，右键 index.html → Open with Live Server
```

浏览器打开 http://localhost:8080

> 注意：不要直接双击 `index.html` 用 `file://` 打开，虽然本框架也能跑，但可以避免后续加 fetch/模块化时的跨域限制。

---

## 五、换成你自己的内容

### 1. 替换 / 新增图片（最常见）
两种做法：

**A. 换掉现有图** —— 按**同名**放进 `assets/images/` 覆盖即可，HTML 不用改。当前素材清单：

```
assets/images/
├── hero.webp              1920×1080  首屏大图
├── logo.webp              36×36      页头 / 页脚 logo
├── favicon.svg / .png                站点图标
├── about.webp             1000×750   品牌宣言配图
├── series-fluted.webp     1000×1000  四大系列（1:1）
├── series-wood.webp
├── series-marble.webp
├── series-3d.webp
├── material-wpc.webp      800×800    核心材料卡
├── material-spc.webp
├── material-pvc.webp
├── material-finish.webp
├── app-residential.webp   900×675    应用场景画廊（4:3，共 6 张）
├── app-hospitality.webp / app-commercial.webp / app-wet.webp / app-kitchen.webp / app-bedroom.webp
└── cta.webp               1600×900   底部 CTA 背景
```

**B. 新增产品图到「Product showcase」预留位** —— 见 `index.html` 里 Materials 区下方那段说明注释，
把 `<div class="media media--slot">…</div>` 整块换成 `<div class="media"><img src="…"></div>` 即可，
注释里给的是可直接复制、不会破图的写法。

> 无论 A 还是 B：换完图**务必跑一次 `python tools/sync_dist.py`**，
> 脚本会把 `index.html` 里所有图片引用逐个对照磁盘校验，任何一个文件名打错都会当场报出来，
> 避免"线上破图但本地看不出来"。同时**保留 `width`/`height` 属性**（防 CLS）。
> 新增/更换素材后建议顺便更新 `sitemap.xml` 的 `lastmod`（`--bump` 参数会代劳）。

### 2. 改品牌色
打开 `assets/css/style.css`，只改开头 `:root` 里的几个变量，全站生效：

```css
--c-accent:    #B08D57;   /* 点缀色（黄铜） */
--c-ink:       #14171A;   /* 主文字 / 深色底 */
--c-paper:     #FFFFFF;   /* 主背景 */
--c-line:      #E4E1DA;   /* 分隔线 */
```

### 3. 改字体
默认 Inter（Google Fonts）+ 系统回退。若目标用户在国内访问慢，删掉 `index.html` 里那三行 `fonts.googleapis` 引用即可，会自动回退到系统字体栈。

### 4. 改文案
全部在 `index.html` 里，按上表 `id` 定位区块直接改。

### 5. 上线前必改清单
- [x] `<title>` → `WPC & SPC Wall Panels for the Philippines | GEMU® Surface`（关键词前置）
- [x] `<meta name="description">` / `keywords` / `robots` → 已配置
- [x] canonical → https://www.fsgemu.cn/
- [x] Open Graph + Twitter Card 全套（含图片宽高比 1920×1080、og:locale=en_PH）
- [x] 企业邮箱 sky@fsgemu.cn；电话全站统一 +86 130 7630 0041（NAP 一致）
- [x] favicon → assets/images/favicon.svg + .png（含 apple-touch-icon）
- [x] 结构化数据 JSON-LD → Organization + WebSite + WebPage + FAQPage
- [x] `robots.txt` / `sitemap.xml` / `llms.txt` → 根目录与 `dist/` 双份齐备
- [ ] **Organization 的 `sameAs`** → 拿到社媒 / Google 商家 / 目录链接后补上（GEO 最大加分项）
- [ ] **GA4 + Google Search Console + Bing Webmaster** → 开通后接入代码并提交 sitemap
- [ ] **页脚 Privacy / Terms / Warranty** → 目前是占位，需真实页面
- [ ] 页脚年份已自动，但公司名请确认

> 完整审计与待办分层见 **[SEO-GEO-分析报告.html](./SEO-GEO-分析报告.html)**（当前 v2）。

---

## 六、部署

见 **[DEPLOY.md](./DEPLOY.md)** —— 含 Vercel / Netlify / Cloudflare Pages / GitHub Pages / 自有 VPS 五种方案的分步指令，以及上线检查清单与回滚步骤。
