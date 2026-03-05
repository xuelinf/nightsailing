---
name: Skills 结构说明与创建规范
description: 定义 Claude Code Skills 的概念、目录结构、SKILL.md 写作规范、frontmatter 字段说明及最佳实践，作为创建高质量 Skills 的标准参考。
created: 2026-03-04
last_modified: 2026-03-04
author: 夜航船
---

# Skills 结构说明与创建规范

## 一、什么是 Skill

Skill 是 Claude Code 的能力扩展单元。通过创建一个包含 `SKILL.md` 的目录，即可教会 Claude 新的技能。Claude 会在相关场景自动调用，也可以通过 `/skill-name` 手动触发。

Skill 遵循 [Agent Skills](https://agentskills.io) 开放标准。

## 二、Skill 的存放位置

| 作用域 | 路径 | 生效范围 |
|:---|:---|:---|
| 企业级 | 通过 managed settings 部署 | 组织内所有用户 |
| 个人级 | `~/.claude/skills/<skill-name>/SKILL.md` | 你的所有项目 |
| 项目级 | `.claude/skills/<skill-name>/SKILL.md` | 仅当前项目 |
| 插件级 | `<plugin>/skills/<skill-name>/SKILL.md` | 启用了该插件的项目 |

优先级：企业级 > 个人级 > 项目级。插件级使用 `plugin-name:skill-name` 命名空间，不会冲突。

## 三、Skill 的目录结构

每个 Skill 是一个独立目录，`SKILL.md` 为入口文件（必需），其他文件为可选的辅助资源：

```
my-skill/
├── SKILL.md           # 主指令文件（必需）
├── template.md        # 供 Claude 填充的模板
├── examples/
│   └── sample.md      # 示例输出，展示期望格式
└── scripts/
    └── validate.sh    # Claude 可执行的脚本
```

> 建议：`SKILL.md` 控制在 500 行以内，详细参考资料放到独立文件，并在 SKILL.md 中引用。

## 四、SKILL.md 的写作规范

### 4.1 基本结构

SKILL.md 由两部分组成：

1. **YAML Frontmatter**（`---` 包裹）：配置 Skill 的元数据与行为
2. **Markdown 正文**：Claude 执行该 Skill 时遵循的具体指令

### 4.2 Frontmatter 字段说明

```yaml
---
name: my-skill                    # Skill 名称，也是 /slash-command 的名称
description: 这个 Skill 做什么      # 描述，Claude 据此判断何时自动加载
argument-hint: "[issue-number]"   # 自动补全时的参数提示
disable-model-invocation: false   # true = 仅用户可手动触发
user-invocable: true              # false = 从 / 菜单隐藏，仅 Claude 自动调用
allowed-tools: Read, Grep, Glob   # 激活时 Claude 可免授权使用的工具
model: sonnet                     # 激活时使用的模型
context: fork                     # fork = 在隔离的子 agent 中运行
agent: Explore                    # context: fork 时使用的子 agent 类型
---
```

所有字段均为可选。**强烈建议填写 `description`**，这是 Claude 自动识别和调用 Skill 的关键。

### 4.3 字段详细说明

| 字段 | 是否必需 | 说明 |
|:---|:---|:---|
| `name` | 否 | 显示名称。省略则使用目录名。仅允许小写字母、数字、连字符，最长 64 字符 |
| `description` | 建议填写 | 描述 Skill 的功能和使用场景。Claude 据此决定是否自动加载 |
| `argument-hint` | 否 | 参数提示，如 `[filename] [format]` |
| `disable-model-invocation` | 否 | `true` 时 Claude 不会自动触发，仅用户可通过 `/name` 手动调用 |
| `user-invocable` | 否 | `false` 时从 `/` 菜单隐藏，作为背景知识仅供 Claude 自动使用 |
| `allowed-tools` | 否 | Skill 激活时 Claude 可免确认使用的工具列表 |
| `model` | 否 | 指定运行时使用的模型 |
| `context` | 否 | 设为 `fork` 时在独立子 agent 上下文中运行 |
| `agent` | 否 | `context: fork` 时使用的子 agent 类型（`Explore`、`Plan`、`general-purpose` 或自定义） |

## 五、两种核心内容类型

### 5.1 参考型内容（Reference）

提供知识、约定、规范，Claude 在对话中自然融入使用。适合内联运行。

```yaml
---
name: api-conventions
description: 本项目的 API 设计规范
---

编写 API 端点时：
- 使用 RESTful 命名规范
- 返回统一的错误格式
- 包含请求参数校验
```

### 5.2 任务型内容（Task）

提供分步骤的操作指令，通常由用户手动触发。建议设置 `disable-model-invocation: true`。

```yaml
---
name: deploy
description: 部署应用到生产环境
context: fork
disable-model-invocation: true
---

部署应用：
1. 运行测试套件
2. 构建应用
3. 推送到部署目标
4. 验证部署成功
```

## 六、调用控制矩阵

| 配置 | 用户可调用 | Claude 可调用 | 上下文加载时机 |
|:---|:---|:---|:---|
| 默认 | 是 | 是 | 描述始终在上下文中，完整内容在调用时加载 |
| `disable-model-invocation: true` | 是 | 否 | 描述不在上下文中，用户调用时加载 |
| `user-invocable: false` | 否 | 是 | 描述始终在上下文中，调用时加载 |

## 七、高级特性

### 7.1 参数替换

| 变量 | 说明 |
|:---|:---|
| `$ARGUMENTS` | 调用时传入的全部参数 |
| `$ARGUMENTS[N]` / `$N` | 按位置访问参数（0 起始） |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |

示例：

```yaml
---
name: fix-issue
description: 修复 GitHub Issue
disable-model-invocation: true
---

修复 GitHub issue $ARGUMENTS，遵循我们的编码规范。
1. 读取 issue 描述
2. 理解需求
3. 实现修复
4. 编写测试
5. 创建 commit
```

执行 `/fix-issue 123` 时，`$ARGUMENTS` 被替换为 `123`。

### 7.2 动态上下文注入

使用 `` !`command` `` 语法在 Skill 内容发送给 Claude 之前执行 shell 命令，输出替换占位符：

```yaml
---
name: pr-summary
description: 总结 PR 变更
context: fork
agent: Explore
---

## PR 上下文
- PR diff: !`gh pr diff`
- PR 评论: !`gh pr view --comments`
- 变更文件: !`gh pr diff --name-only`

## 任务
总结这个 PR 的变更...
```

### 7.3 子 Agent 执行

设置 `context: fork` 让 Skill 在隔离环境中运行，不会访问当前对话历史：

```yaml
---
name: deep-research
description: 深入研究某个主题
context: fork
agent: Explore
---

深入研究 $ARGUMENTS：
1. 用 Glob 和 Grep 查找相关文件
2. 阅读并分析代码
3. 总结发现，附上具体文件引用
```

### 7.4 辅助文件引用

在 SKILL.md 中引用辅助文件，让 Claude 知道何时加载：

```markdown
## 额外资源
- 完整 API 文档见 [reference.md](reference.md)
- 使用示例见 [examples.md](examples.md)
```

### 7.5 可视化输出

Skill 可以捆绑脚本生成 HTML 等可视化输出，Claude 负责编排，脚本负责生成。

## 八、创建高质量 Skill 的最佳实践

### 8.1 写好 description

- **包含用户会自然使用的关键词**，这是 Claude 自动匹配的依据
- 明确说明"做什么"和"什么时候用"
- 如果触发太频繁，让 description 更具体；如果不触发，检查关键词覆盖

### 8.2 选择合适的调用模式

- 有副作用的操作（部署、发消息）→ `disable-model-invocation: true`
- 背景知识（不需要用户主动调用）→ `user-invocable: false`
- 通用知识和常规任务 → 使用默认值

### 8.3 控制工具权限

- 只读任务用 `allowed-tools: Read, Grep, Glob` 限制权限
- 需要执行命令时明确声明，如 `allowed-tools: Bash(python *)`

### 8.4 保持 SKILL.md 精简

- 主文件控制在 500 行以内
- 详细参考资料、API 文档等放到独立文件
- 通过链接引用辅助文件

### 8.5 合理使用子 Agent

- `context: fork` 适合独立任务，不适合纯指导性内容
- 纯知识型 Skill 不要用 `context: fork`（子 agent 没有对话上下文，无法有效应用指导）

### 8.6 创建 Skill 的完整流程

1. **明确目标**：这个 Skill 解决什么问题？谁来触发？
2. **创建目录**：`mkdir -p ~/.claude/skills/<skill-name>`
3. **编写 SKILL.md**：填写 frontmatter + 指令正文
4. **添加辅助文件**（可选）：模板、示例、脚本等
5. **测试**：用自然语言触发或 `/skill-name` 手动测试
6. **迭代优化**：根据实际效果调整 description 和指令内容

## 九、常见问题排查

| 问题 | 排查方法 |
|:---|:---|
| Skill 不触发 | 检查 description 关键词；用 `What skills are available?` 确认可见性；尝试 `/skill-name` 直接调用 |
| Skill 触发太频繁 | 让 description 更具体；添加 `disable-model-invocation: true` |
| Claude 看不到所有 Skill | Skill 描述超出上下文预算（动态 2%，fallback 16000 字符）；运行 `/context` 检查；设置 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量 |
