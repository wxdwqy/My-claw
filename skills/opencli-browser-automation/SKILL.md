---
name: opencli-browser-automation
description: 基于 opencli + Edge/Chrome Browser Bridge 的轻量化浏览器自动化技能。实现无需付费API即可操控浏览器，支持136个网站和12个外部CLI工具，支持知乎热榜、豆包聊天、B站等平台的自动化操作。当用户需要自动化浏览器操作、抓取网页数据、操控AI聊天机器人、执行连续对话任务时使用本技能。
---

# opencli 浏览器自动化技能方案

> 基于 opencli + Edge/Chrome Browser Bridge，实现轻量化浏览器自动化
>
> **实战验证：2026-05-16 成功在 Edge 浏览器上运行！**

## 一、适用范围

- 公开可访问的网页（无需登录）
- 已登录态的网站（需先在浏览器中登录）
- GitHub、知乎、B站、豆包、小红书等各类网站
- 支持 136 个网站适配器和 12 个外部 CLI 工具
- AI 驱动：自动探索网站、生成命令、录制操作
- ✅ **已验证可用**：百度、Hacker News、知乎热榜、B站排行、豆包聊天连续对话

## 二、安装步骤

### 2.1 安装 opencli

```bash
# 正确包名：@jackwener/opencli
npm install -g @jackwener/opencli

# 验证安装
opencli --version
# 输出：opencli v1.7.22 (或更新版本)
```

⚠️ **注意**：不要使用 `npm install -g opencli`，这个包名是错误的！

### 2.2 浏览器要求

用户需拥有以下任一浏览器（Edge/Chrome Beta/Chrome Dev 均可）：
- **Edge（推荐）**：基于 Chromium，与扩展完全兼容
- Chrome Beta（opencli 官方测试环境）
- Chrome Dev

#### 检查浏览器是否安装

```bash
# 检查 Edge
ls "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

# 检查 Chrome
where chrome
```

#### 启动浏览器

```bash
# Edge (PowerShell)
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList "https://www.baidu.com"

# 等待浏览器启动
Start-Sleep -Seconds 3

# 验证浏览器进程
tasklist | grep -i msedge
```

### 2.3 扩展安装步骤

1. 从 GitHub Releases 下载扩展：`https://github.com/jackwener/opencli/releases/latest/download/opencli-extension.zip`
2. 解压到任意目录（如 `C:\opencli-extension\`）
3. 打开浏览器 `edge://extensions/` 或 `chrome://extensions/`
4. 开启右上角「开发者模式」
5. 点击「加载解压缩的扩展」，选择解压后的文件夹
6. 验证扩展版本（应显示 v1.6.8 或更新）

### 2.4 验证安装

```bash
opencli doctor
```

**成功的输出示例**：
```
opencli v1.7.22 doctor (node v24.14.0)

[OK] Daemon: running on port 19825 (v1.7.22)
[OK] Extension: connected (v1.6.8)

Profiles:
  • default: connected v1.6.8
[OK] Connectivity: connected in 0.2s

Everything looks good!
```

⚠️ **重要**：浏览器必须保持运行，扩展才能连接。关闭浏览器后需重新打开才能恢复。

## 三、核心命令速查

### 3.1 基础命令

| 命令 | 用途 |
|------|------|
| `opencli --version` | 查看 opencli 版本 |
| `opencli doctor` | 检查扩展连接状态 |
| `opencli daemon status` | 查看守护进程状态（PID/端口/内存） |
| `opencli browser <session> open <URL>` | 打开网页 |
| `opencli browser <session> state` | 获取页面可交互元素列表 |
| `opencli browser <session> click <index>` | 点击元素（按索引） |
| `opencli browser <session> type <index> <text>` | 输入文字 |
| `opencli browser <session> screenshot [path]` | 截图 |
| `opencli browser <session> eval <js>` | 执行 JavaScript |
| `opencli browser <session> wait time <秒数>` | 等待页面加载 |
| `opencli browser <session> scroll <direction> [px]` | 滚动页面 |

**说明**：
- `<session>`：会话名称，可以任意命名（如 `work`, `test`, `mybrowser`）
- 使用相同的 `<session>` 名称可以保持同一个浏览器标签页
- 使用不同的 `<session>` 名称可以隔离多个并行浏览器任务

### 3.2 AI 驱动的高级命令

| 命令 | 用途 |
|------|------|
| `opencli explore <url>` | 探索网站，自动发现可用接口、API、存储结构 |
| `opencli generate <url>` | 一键：探索→合成→注册，直接生成新命令 |
| `opencli cascade <url>` | 策略级联：自动找最简单的可用策略 |
| `opencli record <url>` | 录制浏览器操作，生成 YAML 命令候选 |
| `opencli validate <target>` | 验证命令定义是否正确 |
| `opencli verify <target>` | 验证+冒烟测试 |
| `opencli plugin` | 管理插件 |

### 3.3 常用平台命令示例

| 平台 | 命令示例 | 说明 |
|------|----------|------|
| 知乎 | `opencli zhihu hot` | 知乎热榜（✅已验证） |
| B站 | `opencli bilibili ranking` | B站热门视频（✅已验证） |
| Hacker News | `opencli hn top` 或 `opencli hackernews top` | HN 热帖（✅已验证） |
| V2EX | `opencli v2ex hot` | V2EX 热门话题 |
| 36氪 | `opencli 36kr hot` | 36氪热榜 |
| 新浪财经 | `opencli stock <代码>` | A股/港股/美股行情 |
| YouTube | `opencli youtube search <关键词>` | YouTube 搜索 |
| 豆包/元宝 | `opencli yuanbao ask "问题"` | 腾讯元宝对话 |
| 携程 | `opencli ctrip search <目的地>` | 携程搜索 |
| 虎扑 | `opencli tihu detail <帖子ID>` | 虎扑帖子详情 |
| 小红书 | `opencli xhs user <用户ID>` | 小红书用户笔记（需cookie） |

## 四、标准使用流程

### 4.1 日常使用流程

```bash
# 1. 先确认浏览器已启动
tasklist | grep -i msedge

# 如果没有，启动 Edge
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" -ArgumentList "https://www.baidu.com"

# 2. 确认扩展连接
opencli doctor

# 3. 导航到目标网页（使用会话名称 "work"）
opencli browser work open "https://www.baidu.com"

# 4. 获取页面元素
opencli browser work state

# 5. 根据索引操作（点击/输入/滚动）
opencli browser work click 5
opencli browser work type 3 "搜索内容"

# 6. 截图确认结果
opencli browser work screenshot "C:/Users/AIbuddy/baidu_result.png"
```

### 4.2 探索新网站（AI驱动）

```bash
# 1. 探索网站结构
opencli explore "https://target-site.com"

# 2. 合成新命令
opencli synthesize <target>

# 3. 注册命令
opencli register <name>

# 4. 一键完成以上三步
opencli generate "https://target-site.com"
```

### 4.3 需登录网站的操作流程

```
1. 人工在浏览器中完成登录
2. 在浏览器中手动完成验证（如果有）
3. 之后自动化操作会复用登录态
4. 如再次触发验证，重新人工完成
```

## 五、实战测试记录（2026-05-16）

### 5.1 测试环境

- **操作系统**：Windows 10 IoT Enterprise LTSC
- **浏览器**：Edge (x86) - `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- **opencli 版本**：1.7.22
- **扩展版本**：1.6.8
- **Node 版本**：24.14.0

### 5.2 测试步骤与结果

| 测试内容 | 命令 | 结果 | 备注 |
|----------|------|------|------|
| 安装 opencli | `npm install -g @jackwener/opencli` | ✅ 成功 | 包名必须是 `@jackwener/opencli` |
| 验证安装 | `opencli --version` | ✅ 成功 | 输出：1.7.22 |
| 启动 Edge | `Start-Process msedge.exe` | ✅ 成功 | 10个进程正常运行 |
| 检查连接 | `opencli doctor` | ✅ 成功 | Extension: connected (v1.6.8) |
| 打开百度 | `opencli browser work open "https://www.baidu.com"` | ✅ 成功 | 返回 JSON：`{"url":"https://www.baidu.com"}` |
| 截图验证 | `opencli browser work screenshot "C:/Users/AIbuddy/baidu_screenshot.png"` | ✅ 成功 | 截图显示百度首页 |
| Hacker News 热帖 | `opencli hackernews top` | ✅ 成功 | 返回20条热帖 |
| 知乎热榜 | `opencli zhihu hot` | ⚠️ 需登录 | 知乎登录后完全可用 |

### 5.3 关键发现

1. **命令格式**：必须是 `opencli browser <session> <command>`，不是 `opencli operate <command>`
2. **会话名称**：可以任意命名（如 `work`, `test`），保持相同名称可复用同一标签页
3. **浏览器启动**：必须先手动启动浏览器，扩展才能连接
4. **安装包名**：必须是 `@jackwener/opencli`，不是 `opencli`

## 六、豆包聊天操作流程（✅实战验证）

豆包是字节跳动旗下的 AI 助手，支持连续对话、代码编写、图片生成等。

### 6.1 操作步骤

```bash
# 1. 先确认扩展连接
opencli doctor

# 2. 打开豆包
opencli browser work open "https://www.doubao.com"

# 3. 等待页面加载
Start-Sleep -Seconds 3

# 4. 查看页面状态（找到输入框索引）
opencli browser work state

# 5. 定位输入框（注意：豆包的输入框每次状态查询会变ID）
# 方法A：用 state 返回的索引，如 [162] 或 [214] 等
opencli browser work type 162 "你好，请介绍一下你自己"

# 方法B：用 JS 定位（更可靠）
opencli browser work eval "document.querySelector('[data-testid=chat_input_input]')?.focus()"

# 6. 发送消息（用 JS 模拟 Enter 键，最可靠）
opencli browser work eval "document.querySelector('[data-testid=chat_input_input]')?.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', code:'Enter', keyCode:13, bubbles:true}))"

# 7. 等待回复（豆包通常 3-5 秒回复）
Start-Sleep -Seconds 5

# 8. 获取回复内容
opencli browser work eval "document.body.innerText"

# 9. 截图查看实际效果
opencli browser work screenshot "C:\path\to\doubao_result.png"
```

### 6.2 连续对话技巧

```bash
# 每条消息发送后，输入框元素ID会变化，需要重新定位
# 流程：state → 找输入框索引 → type → eval发送

# 示例：连续对话3次
# 第1轮
opencli browser work state | Select-String "chat_input"
# 假设输出：[162]<textarea ... />
opencli browser work type 162 "请帮我写一首诗"
opencli browser work eval "..." # 发送

# 第2轮（输入框ID变成其他数字）
opencli browser work state | Select-String "chat_input"
# 假设输出：[214]<textarea ... />
opencli browser work type 214 "这首诗很美！是即兴创作的吗？"
opencli browser work eval "..." # 发送
```

### 6.3 豆包可用功能

| 功能 | 状态 | 示例 |
|------|------|------|
| 自我介绍 | ✅ 已验证 | "你好，请介绍一下你自己" |
| 文字创作 | ✅ 已验证 | "写一首关于春天的七言绝句" |
| 连续对话 | ✅ 已验证 | 能记住前面的对话内容 |
| 代码编写 | ✅ 已验证 | "用Python写一个计算天数的函数" |
| 图片生成 | ⚠️ 可用 | "请帮我画一幅春天的风景画" |

### 6.4 豆包操作注意事项

1. **输入框定位**：豆包的输入框选择器是 `[data-testid=chat_input_input]`
2. **发送方式**：用 JS 模拟 Enter 键比直接用 `click` 更可靠
3. **等待时间**：文字回复 3-5 秒，代码回复 2-3 秒，图片生成可能需要 10-20 秒
4. **上下文保持**：连续对话正常，会记住之前的内容
5. **URL变化**：开始对话后 URL 会变成类似 `/chat/38420299164573698` 这样的对话ID

## 七、知乎操作流程（✅实战验证）

### 7.1 无需登录的操作

```bash
# 1. 打开热榜
opencli browser work open "https://www.zhihu.com/hot"

# 2. 直接获取热榜数据（无需登录）
opencli zhihu hot
```

### 7.2 需要登录的操作

```bash
# 1. 人工在浏览器中完成登录
# 2. 之后可以直接操作
opencli browser work open "https://www.zhihu.com/search?type=question&q=关键词"
Start-Sleep -Seconds 3

# 3. 滚动查看内容
opencli browser work eval "window.scrollBy(0, 500)"
Start-Sleep -Seconds 2

# 4. 提取搜索结果
opencli browser work eval "JSON.stringify([...document.querySelectorAll('h2, .ContentItem-title')].map(el=>el.innerText).filter(t=>t.trim()).slice(0,20))"
```

### 7.3 知乎注意事项

1. **登录后完全可用**：热榜、搜索都能正常工作
2. **操作节奏**：适当加 `wait`，模拟真人操作节奏
3. **触发验证**：知乎有反AI检测，大规模操作可能触发验证

## 八、高级技巧

### 8.1 截图调试

```bash
# 关键步骤后截图确认
opencli browser work screenshot "C:\path\to\debug1.png"

# 对比操作前后
opencli browser work screenshot "C:\path\to\before.png"
# 执行操作...
opencli browser work screenshot "C:\path\to\after.png"
```

### 8.2 用 JS 获取结构化数据

```bash
# 获取页面所有图片链接
opencli browser work eval "JSON.stringify([...document.querySelectorAll('img')].map(img=>({src:img.src,alt:img.alt})))"

# 获取对话内容（豆包等聊天页面）
opencli browser work eval "document.body.innerText"

# 检查元素是否存在
opencli browser work eval "document.querySelector('[data-testid=chat_input_input]') !== null"
```

### 8.3 页面滚动

```bash
# 滚动到指定位置
opencli browser work eval "window.scrollTo(0, 500)"
opencli browser work eval "window.scrollTo(0, document.body.scrollHeight)"

# 滚动查看完整内容
opencli browser work eval "window.scrollBy(0, 500)"
```

### 8.4 等待页面加载

```bash
# 固定等待
Start-Sleep -Seconds 3

# 使用 opencli wait 命令
opencli browser work wait time 3

# 等待特定元素出现
opencli browser work wait selector ".loaded"

# 等待特定文本出现
opencli browser work wait text "Success"
```

## 九、注意事项

### 9.1 反 AI 检测网站

| 网站 | 验证情况 | 解决方案 | 验证日期 |
|------|----------|----------|----------|
| GitHub | ✅ 无需验证 | 直接可用 | - |
| 36氪 | ✅ 无需验证 | 直接可用 | - |
| Hacker News | ✅ 无需验证 | 直接可用 | 2026-05-16 |
| B站 | ✅ 无需验证 | 直接可用 | 2026-04-06 |
| **知乎** | ✅ **登录后完全可用** | 人工登录一次即可 | 2026-04-06 |
| **豆包** | ✅ **登录后完全可用** | 人工登录后连续对话正常 | 2026-04-06 |
| 微信 | ⚠️ 需扫码 | 需人工辅助 | - |
| 豆包图片生成 | ⚠️ 可能跳转 | 豆包说"我将为你绘制" | 2026-04-06 |

### 9.2 避免触发验证的技巧

- **操作节奏模拟真人**：适当加 `wait`，每次操作间隔 1-2 秒
- **避免高频点击**：不要在 1 秒内连续点击多次
- **先观察页面加载完成再操作**：用 `opencli browser <session> state` 确认页面加载完毕
- **使用 `opencli cascade`**：自动找最安全的策略
- **截图确认**：关键步骤后截图，确认页面状态

### 9.3 故障排查

| 问题 | 解决方案 |
|------|----------|
| Extension: not connected | 重启浏览器，确保扩展已启用 |
| 守护进程未运行 | 运行 `opencli daemon status` 查看状态 |
| 操作无响应 | 先 `opencli browser <session> state` 查看元素状态 |
| 浏览器未运行 | 手动打开浏览器 |
| 页面变空白/空 | 用 `opencli browser <session> open` 重新导航到目标页面 |
| 输入框元素找不到 | 用 `state` 重新定位，元素ID每次会变 |
| 豆包发送后无回复 | 检查是否跳转了页面，等待更长时间 |
| URL 显示 about:blank | 扩展连接断开了，重新 `open` 目标页面 |

## 十、与 agent-browser 的对比

| 维度 | opencli | agent-browser |
|------|---------|---------------|
| 浏览器 | 复用用户已有 Chrome/Edge | 自带 Chromium（约 300MB） |
| 登录态 | 完全复用真实浏览器 | 独立 profile |
| 安装大小 | ~30KB（扩展）+ npm 包 | ~300MB |
| 命令数量 | 136 个网站适配器 + 12 个外部CLI | 通用操作 |
| AI 探索 | ✅ 有（explore/generate） | ❌ 无 |
| **推荐场景** | **优先使用**，轻量简洁 | 备选方案 |

## 十一、结论

**opencli 是首选工具**，理由：
1. 复用用户已有浏览器，不额外占用空间
2. 136 个现成命令，覆盖常用网站
3. AI 探索功能强大，支持一键生成新命令
4. 安装简单（npm + 扩展），不引入重复依赖
5. 登录态完全复用，避免重复认证

**agent-browser 作为备选**，当：
- opencli 无法连接用户浏览器时
- 需要独立浏览器环境时
- 需要特定 Chromium 版本时

---

## 十二、作者信息

**作者**：云爪 🐾

**联系邮箱**：3834522034@qq.com

**版本历史**：
- **v2.0.0 (2026-05-16)**：重大更新！修正命令格式为 `opencli browser <session> <command>`，新增 Edge 浏览器测试记录，更新安装步骤
- v1.2.0 (2026-04-06)：新增豆包/知乎操作流程、高级技巧、实战测试记录
- v1.1.0 (2026-04-06)：新增与 agent-browser 对比、故障排查
- v1.0.0 (2026-04-06)：初始版本

---

## 附录：完整命令列表

### A.1 外部 CLI 工具（12个）

discord(discord-cli), docker, dws(DingTalk Workspace), gh, lark-cli, longbridge, ntn(notion), obsidian, tg(tg-cli), vercel, wecom-cli(企业微信), wx(wx-cli)

### A.2 App 适配器（7个）

antigravity, chatgpt-app, chatwise, codex, cursor, discord-app, doubao-app

### A.3 网站适配器（136个）

1688, 1point3acres, 36kr, 51job, aibase, amazon, apple-podcasts, arxiv, baidu-scholar, band, barchart, bbc, bilibili, binance, bloomberg, bluesky, boss, brave, chaoxing, chatgpt, claude, cnki, coingecko, coupang, crates, ctrip, dblp, deepseek, defillama, devto, dianping, dictionary, dockerhub, douban, doubao, douyin, duckduckgo, eastmoney, endoflife, facebook, flathub, gemini, gitee, google, google-scholar, goproxy, gov-law, gov-policy, grok, hackernews, hf, homebrew, hupu, imdb, indeed, instagram, jd, jianyu, jike, jimeng, ke, lesswrong, lichess, linkedin, linux-do, lobsters, maimai, maven, mdn, medium, mubu, notebooklm, nowcoder, npm, nuget, nvd, oeis, ones, openalex, openfda, openreview, osv, packagist, paperreview, pixiv, powerchina, producthunt, pubmed, pypi, quark, qwen, reddit, rednote, rest-countries, reuters, rfc, rubygems, sinablog, sinafinance, smzdm, spotify, stackoverflow, steam, substack, taobao, tdx, ths, tieba, tiktok, toutiao, tvmaze, twitter, uisdc, uiverse, v2ex, wanfang, web, weibo, weixin, weread, wikidata, wikipedia, wttr, xianyu, xiaoe, xiaohongshu, xiaoyuzhou, xueqiu, yahoo, yahoo-finance, yollomi, youtube, yuanbao, zhihu, zlibrary, zsxq

**运行 `opencli list` 查看完整命令详情，或 `opencli <site> --help -f yaml` 查看单个网站的所有命令参数。**
