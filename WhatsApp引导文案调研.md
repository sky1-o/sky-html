# GEMU WhatsApp 引导文案调研报告

> 调研依据：《GEMU护墙板精准客户画像_5个核心维度》+ 实测 5+4 个网站（2026-09-10，真实 Chrome 逐站扫描 DOM）
> 画像关键输入：客户 = 菲律宾建材进口商/经销商/Fit-out承包商；成交沟通 = **WhatsApp + Email**；新客户路径 = 目录 → 花色 → 样品 → 报价 → 试单 → 整柜；核心痛点 = 中国供应商**回复慢、报价慢**

---

## 一、目标客户最常访问的 Top 5 网站分析

| # | 网站 | 定位 | 页面结构 | 内容呈现方式 |
|---|------|------|----------|--------------|
| 1 | **Wilcon Depot**<br>wilcon.com.ph | 全菲最大建材连锁，"Dream It. Plan It. Build It."，服务零售+承包商 | 首页轮播（Inspiration / App / Shop Online / News）→ 自有品牌墙 → **全国分店网络**（按 NCR/Luzon/Visayas/Mindanao 分区列出 90+ 分店） | 不卖价格卖"网络+便利"：分店列表是最核心内容；独立商城 shop.wilcon.com.ph 承接线上 |
| 2 | **Matimco**<br>matimco.com | 60 年本地木材大厂（1964 起家），"A Legacy of Innovation" | 品牌故事时间轴（1964→2025 每十年一节点）→ 使命/愿景/价值观 → 子品牌（Matwood/Gudwood/Nuwood）→ House of Wood 展厅 | **用历史与信任资产说话**：ISO 认证、可持续叙事、大师工艺；几乎不谈价格，谈传承 |
| 3 | **GRM Biowood**<br>grmbiowood.com.ph | 高端工程认证型，Biowood 独家分销 | Hero + GreenTag™ 认证区 → 16 类产品网格（每卡带 **Get a Quote**）→ 8 条 Why-Choose 卖点 → **案例库**（Starbucks/Ayala）→ 博客 → 联系块（含客户类型筛选表单） | **认证+案例双引擎**：认证徽章置顶，案例按项目呈现；每个产品卡都有报价按钮；博客持续产 SEO 内容 |
| 4 | **Greenwood Philippines**<br>greenwoodphilippines.com | 仓储直营低价，"The #1 Supplier" | HOME → PRODUCTS → **PROJECTS → INFLUENCERS** → ABOUT → Contact & Warehouse Locations | 全菲多分店+KOL 测评（INFLUENCERS 栏目是菲国特色）→ 用"无中间商"叙事打价格敏感型买家 |
| 5 | **Philippine Steelcare**<br>steelcaretrading.com | 建材垂直电商，明码标价 | 电商首页：产品卡（₱275–1100/片）→ Most Popular 排行 → DELIVERY/PRODUCTION/SUPPORT 三承诺 → 按品类分区 | **价格+规格全部公开**：每卡带价格区间、颜色变体、Quick view/Compare；这是它吃搜索流量的原因 |

**共性洞察**：5 站全部把"线下网络/信任资产"放最重位置；只有 Steelcare 把价格摆上台面；**没有一家认真做在线询盘转化**——这就是 GEMU 的空档。

---

## 二、WhatsApp 链接检查结果（逐站原文摘录）

### 结论先行：**5 个本地站没有一个挂 WhatsApp 按钮**

| 网站 | WhatsApp | 实际聊天入口（DOM 原文摘录） |
|------|----------|------------------------------|
| Wilcon | ❌ 无 | 页脚社交图标：`Viber` → `https://bit.ly/WilconDepotPHViber`（Viber 社群运营，无按钮文案） |
| Matimco | ❌ 无 | 全站无任何聊天入口，仅表单和线下展厅 |
| GRM Biowood | ❌ 无 | `(+63) 917 305 9445`、`(02) 8362 0080`、`info@grmbiowood.com.ph`；营业时间 "Monday to Thursday - 8AM to 7PM"；每产品卡 `Get a Quote` |
| Greenwood | ❌ 无 | 仅导航 CONTACT 页；无 wa.me/viber 链接 |
| Steelcare | ❌ 无 WhatsApp，但有**等效物** | 联系页：`Phone: +63 917 168 8749` + `viber://chat?number=+639171688749`（点击直接拉起 Viber 聊天，号码即按钮） |

**为什么本地站不用 WhatsApp？** 菲律宾本地生态是 **Viber + Messenger + 电话**。但你的买家是**进口商/经销商**——他们和中国供应商的成交沟通就是 WhatsApp（你自己的画像数据也证实了这一点）。所以：本地同行没做 ≠ 不该做，而是**这块阵地完全空着**。

### 补充样本：真正在用 WhatsApp 引导的同行（原文摘录）

| 来源 | 原文 | 亮点 |
|------|------|------|
| **sonsill.com**（中国墙板出口商） | 按钮 `Talk on WhatsApp`（首页出现 2 次）；`Request Free Samples`；`Sample SLA 48h`；`Territory pricing, OEM packaging, full marketing support`（FOR DISTRIBUTORS 专区） | 按钮文案口语化、按买家身份分专区、给出响应时限 |
| **sothinkhome.com**（对菲出口自建站） | `Tel/WhatsApp: +86 137 0339 9579 (James Wilson)`；`👉 Click below to claim your offer & get a tailored quote in 24 hours 👈`；`✅ Free Sample Kit (3 different finishes, shipped via DHL) ✅ 5% discount on first container order`；`Below are real (anonymized) screenshots from our WhatsApp and email support channels` | **真人化**（姓名+手机号）；限时钩子；24h 承诺；晒聊天截图建立信任 |
| **xhwood.com** | `Salesperson : Archer Mobile / Whatsapp: +8617753868584`；`We respond to all inquiries within 24 hours` | 把"人"推到前台 |
| **ltpvcfactory.com** | `WhatsApp: +86 17757302351`；`Sample Policy: Free samples and brochures are provided, with freight collect` | 样品政策写进话术 |
| ⚠️ **sothinkhome 的反面教材** | 其 WhatsApp 按钮链接是 `api.whatsapp.com/send/?phone=%E9%BB%98%E8%AE%A4` —— phone 参数是**未填的模板占位符（"默认"）**，按钮全是坏的 | 上线前务必真机测试 wa.me 链接 |

---

## 三、GEMU 全新 WhatsApp 引导文案（含借鉴说明）

> 适用号码：`+86 130 7630 0041` ｜ 落地链接模板：`https://wa.me/8613076300041?text=<开场白URL编码>`

### ① 首屏主按钮

**文案：`Chat on WhatsApp`**

- 借鉴 **sonsill "Talk on WhatsApp"**：动词开头 + 口语化，比 "WhatsApp Us" 更有对话感；比 "Contact us" 明确告知点过去是什么。

### ② 按钮预填开场白（买家点击后自动出现在输入框）

**文案：**
> Hi GEMU, I'm a [distributor / contractor] in the Philippines. Please send me your latest catalog and FOB price list.

- 借鉴 **画像"新客户路径"第一条 = Catalog**：开场白直接对准买家旅程第一步（索目录），买家零打字即可发出高质量询盘
- 借鉴 **sothinkhome 的身份前置**：让买家亮出身份（distributor/contractor），你方第一句就能分级跟进

### ③ CTA 区引导文案（按钮上方一句话）

**文案：**
> Message us on WhatsApp — catalog, MOQ and container pricing answered within 4 hours on working days.

- 借鉴 **sothinkhome "tailored quote in 24 hours"**：给出明确响应时限。sothinkhome 说 24h，你说 **4 小时**——这正打画像里最大的痛点"中国供应商回复慢、报价慢"，且敢写得比对手短
- 借鉴 **画像"需求点思考"清单**：catalog / MOQ / container pricing 三个词就是买家脑子里的问题原文

### ④ 样品钩子（放在 CTA 区副行或 WhatsApp 首条回复里）

**文案：**
> Free sample kit (3 finishes of your choice) — you only cover the courier.

- 借鉴 **sothinkhome "Free Sample Kit (3 different finishes, shipped via DHL)"**：把"样品"具体化成 kit+数量
- 借鉴 **ltpvcfactory "free samples, freight collect"**：运费由买家承担的表述，过滤纯薅样品的人（对应画像"低价值客户：只采购样品"）

### ⑤ 真人署名（页脚/联系块）

**文案：**
> WhatsApp: +86 130 7630 0041 (Salon — Export Sales) ｜ Mon–Sat 8:00–20:00 (GMT+8)

- 借鉴 **sothinkhome/xhwood 的真人化**：号码配姓名+职位，回复率显著高于陌生号码；营业时间借鉴 **GRM "Monday to Thursday - 8AM to 7PM"** 的明示做法（时间按你实际情况改）

### ⑥ 信任截图位（可选，后期加）

**文案：**
> Real conversations with our buyers — see how we handle inquiries, samples and shipping docs.

- 借鉴 **sothinkhome 的 WhatsApp 聊天截图信任区**：对从未交易过的菲律宾买家，截图是最便宜的信任证据（注意打码客户信息）

### ⚠️ 上线前必做

1. 真机点击测试 `wa.me/8613076300041` 链接（**sothinkhome 全站按钮坏了都没发现**——别重蹈覆辙）
2. WA 号设置：头像用 GEMU logo、状态写 "GEMU Wall Panels | Foshan, China"、隐私设置允许任何人发消息

---

*调研方法：WebFetch + 真实 Chrome（agent-browser）逐站扫描 DOM 中 wa.me/api.whatsapp/viber/tel 链接及浮窗文本；引用均为 2026-09-10 页面原文。*
