---
name: AI Protocol - AI协作规范
description: AI写作、更新、管理文件的标准规范，确保人与AI协作的一致性与可读性。
created: 2026-03-04
last_modified: 2026-03-04
author: 夜航船
---

# AI Protocol - AI协作规范

## 1. 文档写作基本规范

所有文档统一采用以下格式：

- **文件格式**：Markdown（.md）
- **元数据**：文档开头使用 YAML frontmatter（以 `---` 包裹），存放 meta 数据
- **正文**：YAML frontmatter 之后，使用标准 Markdown 格式书写

### YAML Frontmatter 结构

每个文档必须包含以下字段：

```yaml
---
name: 文档标题
description: 一句话描述文档的核心内容与用途，满足渐进式披露原则，便于AI和人快速了解文档主旨。
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
author: 作者名
---
```

### 设计原则

- **渐进式披露**：通过 YAML frontmatter 让读者（人或AI）无需阅读全文即可快速理解文档的主要内容与用途，便于后续调用和检索。
