---
name: "tavily"
description: "Tavily search API for AI agents. Provides clean, relevant web search results. Requires API key."
---

# Tavily Search Skill

Tavily 是为 AI 智能体设计的搜索 API，返回干净、相关的网络搜索结果。

## 配置

**API Key 存储在 Key.md 中**，位置：`C:\Users\AIbuddy\.workbuddy\Key.md`

脚本会自动从以下位置读取 API key（按优先级）：
1. 环境变量：`TAVILY_API_KEY`
2. Key.md 文件中的配置

**首次使用**：
- 确保 `C:\Users\AIbuddy\.workbuddy\Key.md` 中包含 Tavily API Key
- 或者设置环境变量：`export TAVILY_API_KEY="your-key-here"`

## 使用方法

### 基础搜索
```bash
uv run {baseDir}/scripts/tavily_search.py "your search query"
```

### 高级选项
```bash
# 搜索并包含答案（AI生成摘要）
uv run {baseDir}/scripts/tavily_search.py "query" --include-answer

# 搜索并包含图片结果
uv run {baseDir}/scripts/tavily_search.py "query" --include-images

# 限制结果数量（默认5）
uv run {baseDir}/scripts/tavily_search.py "query" --max-results 10

# 搜索特定域名
uv run {baseDir}/scripts/tavily_search.py "query" --include-domains "wikipedia.org,github.com"
```

## API 端点

- **搜索**: `https://api.tavily.com/search`
- **文档**: https://docs.tavily.com

## 返回格式

```json
{
  "query": "search query",
  "results": [
    {
      "title": "Page Title",
      "url": "https://...",
      "content": "Relevant content snippet...",
      "score": 0.95
    }
  ],
  "answer": "AI-generated answer (if requested)"
}
```

## 示例

```bash
# 搜索 Office 2016 自定义安装方法
uv run {baseDir}/scripts/tavily_search.py "Office 2016 ODT custom installation exclude apps"

# 搜索最新AI新闻（带答案）
uv run {baseDir}/scripts/tavily_search.py "latest AI news 2026" --include-answer
```

## 注意事项

- API 有使用限额，请合理使用
- 搜索结果默认返回英文，可指定搜索语言
- 适合需要高质量、结构化搜索结果的场景
- **API key 不要硬编码在脚本中**，请从 Key.md 或环境变量读取

---

**作者**: 云爪 🐾
**版本**: v1.1.0 (2026-05-16) - 移除硬编码的 API key，改为从 Key.md 读取
**联系邮箱**: 3834522034@qq.com
