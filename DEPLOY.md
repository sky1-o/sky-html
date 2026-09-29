# fsgemu.cn 上线部署手册

域名：**fsgemu.cn**（阿里云注册）
站点：**纯静态**（无构建、无后端），发布目录为 `dist/`（index.html + assets/ + robots.txt + sitemap.xml）

> **为什么用香港/海外节点**：目标买家在菲律宾。国内节点必须 ICP 备案（2–4 周），且境外访问慢；
> 海外/香港节点**免备案、即开即用**，对菲律宾访客反而更快。`.cn` 域名解析到海外服务器是完全合规的。

---

## 当前状态（2026-09-10）

- ✅ 网站已通过 WorkBuddy 发布，**分享链接立即可用**（发给客户看完全没问题）：
  - `https://0e9dabc5ab334b478690cd38538eda76.app.workbuddy.link`
  - 内容更新：改完项目文件 → 同步到 `dist/` → 重新发布，链接不变。
- ⏳ fsgemu.cn 绑定：二选一（方案 A 推荐，方案 B 全程在阿里云内）。

---

## 方案 A：EdgeOne Pages（推荐 · 免费 · 免备案 · 我来部署）

腾讯云 EdgeOne Pages 国际版，全球 CDN（含亚太），自动 HTTPS，免费额度足够。

**你要做的只有 3 步（共约 10 分钟）：**

1. **安装授权**：在 WorkBuddy 里安装「EdgeOne Makers」连接器并按提示登录/授权（免费注册腾讯云国际账号即可）。
   授权后告诉我，我直接把 `dist/` 部署上去，返回一个 `xxx.edgeone.app` 的正式地址。
2. **绑定域名**：EdgeOne Pages 控制台 → 你的项目 → **Custom Domains** → 添加 `fsgemu.cn` 和 `www.fsgemu.cn`，
   接入区域选「全球可用区（不含中国内地）」。控制台会给出一个 CNAME 目标值（形如 `xxx.eo.dnse1.com`）。
3. **去阿里云加解析**（域名 → 解析设置 → 添加记录）：

   | 记录类型 | 主机记录 | 记录值 | TTL |
   |---|---|---|---|
   | CNAME | `@` | EdgeOne 给的 CNAME 值 | 10分钟 |
   | CNAME | `www` | EdgeOne 给的 CNAME 值 | 10分钟 |

   > 若控制台对根域名给出的是 A 记录而非 CNAME，按它给的值填 A 记录即可。

生效后 EdgeOne 自动签发 HTTPS 证书（通常几分钟～24 小时内）。

---

## 方案 B：阿里云 OSS 静态网站托管（香港节点 · 不用离开阿里云）

**你要做的（控制台操作约 20 分钟）：**

1. **建 Bucket**：OSS 控制台 → 创建 Bucket → 名称如 `fsgemu-web`（全局唯一）→ **地域选「中国香港」**（免备案）
   → 读写权限选「公共读」→ 其余默认。
2. **开启静态托管**：Bucket → 数据管理 → 静态页面 → 默认首页 `index.html`、404 页也可填 `index.html` → 保存。
3. **上传文件**：Bucket → 文件列表 → 把本地 `dist/` 里的 **`index.html`、`assets/` 文件夹、`robots.txt`、`sitemap.xml`**
   全部拖入上传（保持目录结构）。
4. **绑定域名**：Bucket → Bucket 配置 → 域名管理 → 添加自定义域名 `fsgemu.cn`（再添加一次 `www.fsgemu.cn`）。
5. **HTTPS 证书**：阿里云「数字证书管理服务」→ 免费证书 → 申请一张 `fsgemu.cn` 的 DV 证书（免费，几分钟签发）
   → 回到 OSS 域名管理 → 对应域名处上传/选择该证书。
6. **去阿里云解析**（和方案 A 同一入口）：

   | 记录类型 | 主机记录 | 记录值 | TTL |
   |---|---|---|---|
   | CNAME | `@` | `fsgemu-web.oss-cn-hongkong.aliyuncs.com` | 10分钟 |
   | CNAME | `www` | `fsgemu-web.oss-cn-hongkong.aliyuncs.com` | 10分钟 |

   > 把 `fsgemu-web` 换成你实际的 Bucket 名。费用：低流量下每月几元，按量计费。

---

## 方案 C（备选）：Cloudflare Pages

免费、全球 CDN，但要新注册 Cloudflare 账号并托管 DNS，步骤见旧版手册存档。
适合以后想把域名解析整体迁出阿里云时再考虑。

---

## 上线验收清单（域名解析生效后逐项检查）

- [ ] `https://www.fsgemu.cn/` 能打开，地址栏有锁标志（HTTPS）
- [ ] `http://fsgemu.cn` 能跳转到 HTTPS
- [ ] 首屏大图、四个系列图、材料三卡（WPC / SPC / Profiles）图片全部加载（F12 → Network 无 404）
- [ ] 手机宽度下汉堡菜单可开合
- [ ] WhatsApp 按钮 / 邮件按钮点击正常唤起
- [ ] 右键查看源代码：title、meta description、canonical 均为 fsgemu.cn
- [ ] Google PageSpeed：https://pagespeed.web.dev/
- [ ] OG 预览调试：https://developers.facebook.com/tools/debug/
- [ ] 把 `https://www.fsgemu.cn/` 提交 Google Search Console（免费，收录更快）

---

## 以后怎么更新网站

1. 告诉我改什么（文字 / 图片 / 产品位）→ 我改项目根目录的 `index.html` / `assets/`。
2. 同步到发布目录：
   ```bash
   cd "C:/Users/35266/Desktop/网站/sky的网站"
   cp -r index.html assets dist/        # Git Bash；或手动把这两个拖进 dist 覆盖
   ```
3. 重新发布（WorkBuddy 链接不变；EdgeOne/OSS 则重新上传 dist 内容）。

> 注意：`tools/`（选图脚本与联络表）和 `.workbuddy/`（工作记录）**不属于网站**，不要上传到 OSS/EdgeOne。
