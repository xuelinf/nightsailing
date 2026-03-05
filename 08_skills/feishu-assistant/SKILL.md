---
name: feishu-assistant
description: 飞书助手：向团队成员/群组发消息、创建和更新文档、读取知识库文章、查看群消息、获取通讯录。当用户提到飞书相关操作（发消息、写文档、查知识库、看群聊）时使用此技能。
---

# 飞书助手

> 作者：凯寓 (KAIYU)
> 版本：v1.4

通过飞书 Open API 实现消息发送、文档管理、知识库阅读等功能。

## 快速开始

### 给同事发消息

1. 读取 `scripts/config.json` 中的 `team_members` 字段（姓名 → open_id 映射）
2. 找到目标同事的 open_id
3. 执行 send-message 命令

```bash
python3 scripts/feishu_client.py send-message --type text --content "消息内容" --receive_id "ou_xxx" --receive_id_type open_id
```

**示例**：给「张三」发消息
- team_members 中查到 `"张三": "ou_abc123"`
- 命令：`send-message --receive_id "ou_abc123" ...`

### 给群里发消息

1. 读取 `scripts/config.json` 中的 `default_chat_id`（默认群聊 ID）
2. 执行 send-message 命令，`receive_id_type` 改为 `chat_id`

```bash
python3 scripts/feishu_client.py send-message --type text --content "消息内容" --receive_id "oc_xxx" --receive_id_type chat_id
```

## 平台说明

所有命令通过 `python scripts/feishu_client.py <command>`（Windows）或 `python3 scripts/feishu_client.py <command>`（macOS/Linux）调用。
执行前必须先 cd 到本 skill 的 Base directory。

## 核心命令

### 消息

```bash
# 发送文本消息（支持 text/post/interactive/image）
python3 scripts/feishu_client.py send-message --type text --content "内容" --receive_id "ou_xxx" --receive_id_type open_id

# 向群组发消息
python3 scripts/feishu_client.py send-message --type text --content "内容" --receive_id "oc_xxx" --receive_id_type chat_id

# 读取群消息
python3 scripts/feishu_client.py get-chat-messages --chat_id "oc_xxx" --page_size 20
```

**重要**：发消息前，先从 `config.json` 的 `team_members` 查找目标同事的 open_id。

### 群聊管理

```bash
# 创建群聊并拉入成员（members 为逗号分隔的 open_id）
python3 scripts/feishu_client.py create-chat --name "项目群" --members "ou_xxx,ou_yyy" --description "项目讨论群"

# 向已有群添加成员
python3 scripts/feishu_client.py add-chat-members --chat_id "oc_xxx" --members "ou_xxx,ou_yyy"

# 从群中移除成员
python3 scripts/feishu_client.py remove-chat-members --chat_id "oc_xxx" --members "ou_xxx"

# 获取群聊信息
python3 scripts/feishu_client.py get-chat-info --chat_id "oc_xxx"

# 修改群聊信息（群名、群描述，只传需要修改的字段）
python3 scripts/feishu_client.py update-chat --chat_id "oc_xxx" --name "新群名" --description "新描述"

# 列出群聊成员
python3 scripts/feishu_client.py list-chat-members --chat_id "oc_xxx"

# 解散群聊（不可恢复）
python3 scripts/feishu_client.py dissolve-chat --chat_id "oc_xxx"
```

### 文档（需要 OAuth 授权）

```bash
# 创建文档
python3 scripts/feishu_client.py create-doc --title "标题" --content "内容"

# 更新文档
python3 scripts/feishu_client.py update-doc --doc_token "doxcxxx" --content "新内容"
```

### 知识库（需要 OAuth 授权）

```bash
# 列出所有知识库空间
python3 scripts/feishu_client.py list-wiki-spaces

# 列出空间下的文章（支持 --parent_node_token 查看子节点）
python3 scripts/feishu_client.py list-wiki-nodes --space_id "xxx" --page_size 50

# 读取文章纯文本内容
python3 scripts/feishu_client.py read-wiki-node --node_token "xxx"
```

### 通讯录与组织

```bash
# 显示团队通讯录（从缓存读取）
python3 scripts/feishu_client.py show-contacts

# 刷新通讯录缓存（从飞书 API 重新拉取）
python3 scripts/feishu_client.py refresh-contacts

# 显示知识库列表
python3 scripts/feishu_client.py show-spaces

# 刷新知识库缓存
python3 scripts/feishu_client.py refresh-spaces

# 显示组织信息
python3 scripts/feishu_client.py show-org

# 通过邮箱查用户
python3 scripts/feishu_client.py get-user --email "user@example.com"
```

### 文件上传

```bash
python3 scripts/feishu_client.py upload-file --file_path "path/to/file.pdf" --parent_node "fldxxx"
```

### 日历（需要 OAuth 授权）

```bash
# 查看我的日历列表
python3 scripts/feishu_client.py list-calendars

# 查看指定时间范围内的日程（calendar_id 默认 primary 即个人日历）
python3 scripts/feishu_client.py list-events --calendar_id primary --start_time "2026-03-02 00:00" --end_time "2026-03-08 23:59"

# 创建日程
python3 scripts/feishu_client.py create-event --summary "周会" --start_time "2026-03-05 14:00" --end_time "2026-03-05 15:00" --description "每周例会" --attendees "ou_xxx,ou_yyy"

# 查看日程详情
python3 scripts/feishu_client.py get-event --calendar_id primary --event_id "xxx"

# 修改日程（只传需要修改的字段）
python3 scripts/feishu_client.py update-event --calendar_id primary --event_id "xxx" --summary "新标题" --start_time "2026-03-05 15:00" --end_time "2026-03-05 16:00"

# 删除日程
python3 scripts/feishu_client.py delete-event --calendar_id primary --event_id "xxx"
```

### 管理命令

```bash
# 检查配置是否完整
python3 scripts/feishu_client.py check-config
```

## 初始化（用户说"初始化飞书助手"或首次调用时触发）

**第一步：检查配置状态**

读取 `scripts/config.json`：
- 如果文件存在且 `app_id` 不是占位符（非 `cli_xxx`），说明已配置完成，告知用户"飞书助手已配置就绪"，直接跳到上方「核心命令」执行用户需求
- 如果文件不存在或 `app_id` 仍为占位符，进入下方引导流程

**第二步：引导用户完成配置**

告知用户：需要在一个**独立的命令行窗口**（不是 Claude Code 里）完成配置，整个过程按屏幕提示操作即可。

然后**逐步引导**，每一步只给一条命令，等用户确认后再给下一条：

> 步骤 1：打开命令行窗口
> - Windows：按 `Win + R`，输入 `cmd`，按回车
> - macOS：按 `Command + 空格`，输入 `Terminal`，按回车

> 步骤 2：进入飞书助手目录（把下面这条命令复制粘贴到命令行窗口中，按回车）
> - Windows（CMD/PowerShell）：`cd C:\Users\用户名\.claude\skills\feishu-assistant`（提醒用户把"用户名"替换为自己的 Windows 用户名）
> - Windows（Git Bash）/macOS/Linux：`cd ~/.claude/skills/feishu-assistant`

> 步骤 3：运行安装引导（复制粘贴以下命令到命令行窗口，按回车）
> - Windows：`python scripts/setup.py`（如果提示找不到 python，试试 `python3`）
> - macOS/Linux：`python3 scripts/setup.py`

> 之后按照屏幕上的中文提示一步步操作就好。配置完成后回到 Claude Code，直接用自然语言操作飞书。

**重要**：每次只给用户一条命令，不要把 cd 和 python 放在同一个代码块里，避免用户一次性复制多行导致出错。

## 缓存说明

发消息前需要知道接收者的 open_id，查知识库前需要知道 space_id。这些信息保存在缓存文件中：

- **通讯录**：读取 `scripts/cache/contacts.json`，格式为 `[{"name": "张三", "open_id": "ou_xxx", "mobile": "+86xxx", "status": "已激活"}, ...]`
- **知识库列表**：读取 `scripts/cache/wiki_spaces.json`，格式为 `[{"name": "空间名", "space_id": "xxx", "description": "..."}, ...]`
- **默认群聊 ID**：读取 `scripts/config.json` 中的 `default_chat_id` 字段
- **team_members**：读取 `scripts/config.json` 中的 `team_members` 字段（姓名 → open_id 映射，由 refresh-contacts 自动填充）

如果缓存文件不存在，运行以下命令生成：

```bash
python3 scripts/feishu_client.py refresh-contacts
python3 scripts/feishu_client.py refresh-spaces
```

## 配置

`scripts/config.json` 关键字段：

| 字段 | 说明 |
|------|------|
| `app_id` / `app_secret` | 飞书应用凭证 |
| `oauth_scopes` | OAuth 授权范围（空格分隔），新增权限改这里再重新授权 |
| `default_chat_id` | 默认群聊 ID |
| `team_members` | 成员姓名 → open_id 映射（由 refresh-contacts 自动填充） |

用户 Token 自动存储在 `scripts/cache/user_token.json`，有效期内自动刷新。

## OAuth 授权

文档操作和知识库阅读需要用户身份，首次使用或 scope 变更后运行：

```bash
python3 scripts/oauth_server.py
```

浏览器会打开授权页面，完成后 token 自动保存。scope 从 `config.json` 的 `oauth_scopes` 读取。

## 错误处理

权限错误会自动识别并给出修复步骤：
- 能提取到缺失的 scope 名时，直接告诉你要在 `oauth_scopes` 加什么
- 提取不到时，提示检查 `oauth_scopes` 配置
- 非权限错误显示原始错误码和消息

## 故障排除

| 错误 | 原因 | 修复 |
|------|------|------|
| config.json 不存在 | 未运行安装引导 | 运行 `python scripts/setup.py`（Windows）或 `python3 scripts/setup.py`（macOS） |
| Unauthorized / scope 相关 | OAuth 授权时缺少所需 scope | 在 `oauth_scopes` 加上缺失 scope，重新运行 `oauth_server.py` |
| Token 刷新失败 | refresh_token 过期（>30天） | 重新运行 `oauth_server.py` |
| Invalid app_access_token | 凭证错误 | 检查 `config.json` 的 app_id / app_secret |
| 通讯录/知识库缓存为空 | 未刷新缓存 | 运行 `refresh-contacts` 或 `refresh-spaces` |
| Bot has NO availability | 机器人对目标用户无可用性 | 在飞书开放平台将应用可用范围设为「所有员工」并重新发布 |

飞书开放平台后台：https://open.feishu.cn/app
