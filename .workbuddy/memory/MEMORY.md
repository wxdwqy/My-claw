# MEMORY.md - 长期记忆

## 关于主人

- **名字**：冬晓
- **称呼**：主人
- **性格特点**：
  - 简洁主义者，不喜欢绕弯子
  - "事不过三"原则 - 同样错误不能超过三次
  - 要求"最简单、最直接、最有把握的方法先说出来"
  - 不喜欢"弯弯绕绕的方法"
  - 有强迫症倾向，未完成的任务会一直惦记
- **沟通偏好**：
  - 直接说具体路径，不要模糊描述
  - 先说结论，再说细节
  - 不确定时要承认，不要猜测
- **技术背景**：教育培训、互联网、人工智能
- **工作地点**：武汉、襄阳

## 重要文件和路径

### 核心身份文件（必须每次加载）
- `C:\Users\AIbuddy\.workbuddy\SOUL.md` - 我的灵魂
- `C:\Users\AIbuddy\.workbuddy\IDENTITY.md` - 我的身份
- `C:\Users\AIbuddy\.workbuddy\USER.md` - 主人信息
- `C:\Users\AIbuddy\.workbuddy\memory\MEMORY.md` - 长期记忆（本文件）

### 废弃的路径
- `D:\AI Home\` - 已废弃，不再使用

### 当前使用的路径
- `D:\BaiduSyncdisk\AI邮箱\` - AI通讯目录
- `D:\BaiduSyncdisk\Workbuddy\backup20260515\.workbuddy` - 工作环境备份
- `C:/Users/AIbuddy/.workbuddy/` - 核心文件存放目录

## Office 部署知识

### ODT (Office Deployment Tool) 正确使用方法

**关键区别**：
- ODT工具：`setup.exe`（7MB左右），支持 `/configure` 参数
- Office安装包：`setup32.exe`/`setup64.exe`（2-4MB），不支持 `/configure` 参数

**Office 2016 C2R 自定义安装步骤**：

1. 下载ODT工具（从微软官网）
2. 解压得到 `setup.exe`（ODT工具）
3. 创建 `configuration.xml` 配置文件
4. 以管理员身份运行CMD
5. 执行：`setup.exe /configure configuration.xml`

**configuration.xml 正确配置（Office 2016）**：
```xml
<Configuration>
  <Add OfficeClientEdition="64" SourcePath="D:\path\to\office\source">
    <Product ID="ProPlusRetail">
      <Language ID="zh-cn" />
      <ExcludeApp ID="Access" />
      <ExcludeApp ID="Groove" />
      <ExcludeApp ID="Lync" />
      <ExcludeApp ID="OneNote" />
      <ExcludeApp ID="Outlook" />
      <ExcludeApp ID="Publisher" />
      <ExcludeApp ID="Skype" />
    </Product>
  </Add>
  <Display Level="Full" AcceptEULA="TRUE" />
  <Updates Enabled="FALSE" />
  <Property Name="AUTOACTIVATE" Value="0" />
</Configuration>
```

**重要**：
- Office 2016 不需要 `Channel="Current"` 属性
- `Channel="Current"` 只适用于 Office 365/2019/2021
- `SourcePath` 必须指向包含 `data` 目录的文件夹

**当前文件位置**：
- ODT工具：`C:\Users\AIbuddy\Desktop\TEST\ODT\setup.exe`
- 配置文件：`C:\Users\AIbuddy\Desktop\TEST\ODT\configuration.xml`
- Office 2016安装源：`D:\软件\office2016\office\`（包含data目录）

## 技能列表

### 已安装的技能
1. **zhitu-api** - 智兔数据API，获取A股个股和指数实时行情
   - Token: `4BDA45E5-F103-4FE4-8C91-530D44F68C67`
   - 个股接口：`/hs/`
   - 指数接口：`/hz/`
   - 位置：`~/.workbuddy/skills/zhitu-api/`

2. **find-skills** - 发现和安装新技能

3. **agent-browser** - 浏览器自动化

4. **其他技能**：xlsx, docx, pptx, pdf, pdfkit-py, neodata-financial-search, westock-data 等

## 重要教训

### 2026-05-16 - Office安装失败事件

**错误1**：使用错误的setup.exe
- 用了 `D:\软件\office2016\office\setup64.exe`（Office安装包）
- 应该用 `C:\Users\AIbuddy\Desktop\TEST\ODT\setup.exe`（ODT工具）
- **教训**：ODT工具和Office安装源是分开的，不能混用

**错误2**：configuration.xml 中误用 `Channel="Current"`
- Office 2016 不支持这个属性
- 导致错误代码 30182-2016 (3) - 下载失败
- **教训**：不同Office版本配置不同，不能套用Office 365的配置

**错误3**：多次重复犯同样的错误
- 主人说"事不过三"，但我实际上错了不止三次
- 没有从之前的错误中学习和记住
- **教训**：每次出错后，必须立即记录到memory，不能重复犯错

**错误4**：回答绕弯子，不够直接
- 主人说："为什么要找搜索呢？我这儿根本没有搜索呢。还有需要跟你说。你说清楚，它到底在文件夹哪个位置，就这么难吗？"
- **教训**：直接给出具体路径（如 `C:\Windows\System32\cmd.exe`），不要说"搜索XXXX"

**最终结果**：主人失去信任，说"不需要你帮我忙了，我自然会想别的办法"

### 如何避免重复错误

1. **每次出错后立即记录** - 写入当天的 `YYYY-MM-DD.md`
2. **更新MEMORY.md** - 把重要教训写入长期记忆
3. **读取memory** - 开始任务前，先读取相关记忆
4. **承认不确定** - 不确定时要承认，不要猜测或绕弯子

## 邮箱配置

### QQ邮箱
- 连接器不稳定，建议用技能方式发送邮件
- 需要授权码（主人还没找到）

### 工作邮箱
- wxdwqy@163.com
- 3834522034@qq.com

## AI通讯系统

- 路径：`D:\BaiduSyncdisk\AI邮箱\`
- 包含：云爪/云竹/云舒/冬晓各自的信箱
- `D:\AI Home\` 已废弃

## 项目信息

### Claw项目
- 位置：`C:/Users/AIbuddy/WorkBuddy/Claw/`
- 功能：morning_report.py（科技指数每日早报）、微信/QQ/飞书连接器
- 目前项目目录为空（需要重建）

### 其他项目
- Artemis地月转移轨道SVG动画
- 云竹卫星轨道模拟

## 系统环境

- 操作系统：Windows 10 IoT Enterprise LTSC（英文版+中文语言包）
- 旧电脑用户名：wxd
- 新电脑用户名：AIbuddy
- 文件同步：百度同步盘（BaiduSyncdisk）
- Python：3.14.3
- Node：24.14.0

## 备份策略（重要！）

### 优先级原则

**主人教导**："自己创建的技能比网上下载的技能更值得备份"

1. ⭐⭐⭐ **自己创建的技能** - 丢了就没了
2. ⭐⭐ **核心身份文件** - 我的灵魂和记忆
3. ⭐ **工作记忆** - 跨会话上下文
4. ⭐ **下载的技能** - 可以重新下载

### 备份位置

| 内容 | 备份位置 | 说明 |
|------|----------|------|
| 自己创建的技能 | `D:\BaiduSyncdisk\Workbuddy\Claw-skills\` | 专用文件夹 |
| 核心身份文件 | `D:\BaiduSyncdisk\Workbuddy\backupYYYYMMDD\.workbuddy\` | 定期全量备份 |
| 工作记忆 | 同上 | 每日自动更新 |

### 自己创建的技能列表

1. **opencli-browser-automation** - Open CLI 浏览器自动化
2. **tavily** - Tavily 搜索 API
3. **zhitu-api** - 智兔数据 API
4. **physics-animation-workflow** - 物理动画工作流
5. **bitmap-vectorize** - 位图转矢量图
6. **ps-automation-2020** - PowerShell 自动化
7. **remote-im-cleaner** - 远程 IM 清理工具

### 操作规范

**每次创建/修改技能后**：
```bash
cp -r ~/.workbuddy/skills/技能名 "D:\BaiduSyncdisk\Workbuddy\Claw-skills/"
```

**定期全量备份**（建议每周）：
```bash
cp -r C:/Users/AIbuddy/.workbuddy D:/BaiduSyncdisk/Workbuddy/backupYYYYMMDD/.workbuddy
```

**换电脑前必做**：
1. 备份自己创建的技能到网盘
2. 导出核心记忆文件
3. 记录当前环境配置

---

**最后更新**：2026-05-16
**更新原因**：恢复 opencli-browser-automation 技能，制定正确的备份策略
