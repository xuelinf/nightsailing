# 飞书助手 (feishu-assistant)

> 作者：**凯寓 (KAIYU)**

让 Claude Code 帮你操作飞书：发消息、读知识库、写文档，一句话搞定。

---

## 安装前准备

在开始之前，需要确认你的电脑装好了两样东西：**Python** 和 **Claude Code**。

如果你已经确定电脑装了 Python 3.8 以上版本和 Claude Code，可以直接跳到下面的「安装步骤」。

---

### 准备 1：检查你的电脑是否已安装 Python

Python 是一个运行工具，飞书助手需要它来工作。我们需要先确认你的电脑有没有装它。

#### Windows 用户

1. 按下键盘上的 `Win + R`（Win 是键盘左下角那个 Windows 徽标键），会弹出一个「运行」小窗口
2. 在里面输入 `cmd`，然后按回车键
3. 会打开一个**黑色背景的窗口**，这就是「命令提示符」（也叫命令行、终端）
4. 在黑色窗口里输入下面这行字，然后按回车：
   ```
   python3 --version
   ```
5. 如果显示类似 `Python 3.12.0` 这样的版本号，说明已经装好了，可以继续
6. 如果显示"不是内部或外部命令"之类的错误，说明还没装，按下面的步骤安装

**没装 Python？按这个步骤安装：**

1. 打开浏览器，访问 https://www.python.org/downloads/
2. 点击黄色的「Download Python 3.x.x」大按钮
3. 下载完成后，双击安装文件
4. **重要：安装界面最下方有一个勾选框 "Add Python to PATH"，一定要勾上！**
5. 然后点击 "Install Now"，等待安装完成
6. 安装完后，**关闭之前打开的命令提示符，重新打开一个**（Win+R → cmd → 回车）
7. 再次输入 `python3 --version` 确认安装成功

#### macOS 用户

1. 按下 `Command + 空格键`，会弹出一个搜索框（Spotlight）
2. 输入 `Terminal`（或输入"终端"），按回车
3. 会打开一个白色（或黑色）背景的窗口，这就是「终端」
4. 在终端里输入下面这行字，然后按回车：
   ```
   python3 --version
   ```
5. 如果显示版本号，说明已经装好了
6. 如果提示未找到命令，按下面的步骤安装

**没装 Python？两种安装方式（任选其一）：**

方式一（推荐）：在终端里输入以下命令，按回车，然后按提示操作：
```
xcode-select --install
```

方式二：打开浏览器，访问 https://www.python.org/downloads/ ，下载安装包，双击安装。

---

### 准备 2：安装 Claude Code

如果你还没安装 Claude Code，请按官方教程安装：https://docs.anthropic.com/en/docs/claude-code

---

### 命令行小技巧

如果你不熟悉命令行（那个黑色/白色背景的窗口），这里是一些基本操作：

**在命令行里粘贴文字：**

| 操作 | Windows 命令提示符 | Windows PowerShell | macOS 终端 |
|------|-------------------|-------------------|-----------|
| 粘贴 | 在窗口里**右键单击** | `Ctrl + V` | `Command + V` |
| 复制 | 选中文字后按**回车** | 选中文字后 `Ctrl + C` | `Command + C` |

**常用操作：**
- 按`上方向键`可以找回之前输入过的命令
- 输错了按 `Ctrl + C` 可以取消当前操作
- 输入命令后一定要按**回车键**才会执行

---

## 安装步骤

### 第 1 步：下载飞书助手

把 `feishu-assistant` 文件夹放到 Claude Code 的 skills 目录下：

- **Windows**: `C:\Users\你的用户名\.claude\skills\feishu-assistant\`
- **macOS**: `~/.claude/skills/feishu-assistant/`

> 提示：`.claude` 是一个隐藏文件夹。Windows 下在文件管理器地址栏直接输入 `C:\Users\你的用户名\.claude\skills\` 按回车即可进入。macOS 下在 Finder 中按 `Command + Shift + .` 可以显示隐藏文件。

### 第 2 步：打开一个命令行窗口

> **注意：这里需要打开一个独立的命令行窗口，不是在 Claude Code 里面输入！**
>
> 安装配置只需要做一次。配置完成后，日常使用时在 Claude Code 里用自然语言操作飞书就行了。

打开命令行的方法（和前面检查 Python 一样）：
- **Windows**：`Win + R` → 输入 `cmd` → 按回车
- **macOS**：`Command + 空格` → 输入 `Terminal` → 按回车

### 第 3 步：进入飞书助手目录

在命令行窗口里，复制粘贴下面**一条命令**，按回车：

**Windows：**（把"你的用户名"换成你自己的）
```
cd C:\Users\你的用户名\.claude\skills\feishu-assistant
```

**macOS：**
```
cd ~/.claude/skills/feishu-assistant
```

> 提示：你也可以用「拖拽」的方式——先输入 `cd `（cd 后面有一个空格），然后把文件夹直接拖到命令行窗口里，路径会自动填上，再按回车。

看到命令行的路径变了（不报错），说明进入成功了。

### 第 4 步：运行安装引导

确认上一步成功后，再复制粘贴下面**一条命令**，按回车：

**Windows：**
```
python scripts/setup.py
```

**macOS：**
```
python3 scripts/setup.py
```

> 如果 Windows 上提示 `python` 找不到，试试 `python3 scripts/setup.py`；macOS 上反之。

安装引导会用中文一步步教你完成配置。按照屏幕上的提示操作就行。

### 第 5 步：回到 Claude Code 说"初始化飞书助手"

配置完成后，回到 **Claude Code**，输入：

```
初始化飞书助手
```

Claude 会自动检查配置状态，确认一切就绪。之后就可以直接用自然语言操作飞书了：

- "给张三发一条飞书消息，内容是明天下午开会"
- "看看知识库里有什么文章"
- "帮我创建一个飞书文档，标题是会议纪要"
- "读一下知识库里的《xxx》这篇文章"

---

## 功能列表

- 发送消息（私聊/群聊）
- 读取群组消息
- 群聊管理（创建群、拉人/踢人、改群信息）
- 创建和更新飞书文档
- 浏览和阅读知识库文章
- 查看团队通讯录
- 上传文件到飞书云文档
- 日历管理（查看/创建/修改/删除日程）

## 文件结构

```
feishu-assistant/
├── SKILL.md                    # Claude 读取的技能定义
├── README.md                   # 你正在看的这个文件
└── scripts/
    ├── setup.py                # 安装引导（运行一次即可）
    ├── feishu_client.py        # 核心 API 客户端
    ├── oauth_server.py         # OAuth 授权工具
    ├── config.example.json     # 配置文件模板
    ├── scopes.json             # 应用权限配置（批量开通用）
    ├── config.json             # 你的配置（自动生成，不要分享）
    └── cache/                  # 运行时缓存
        ├── contacts.json       # 通讯录缓存
        ├── wiki_spaces.json    # 知识库列表缓存
        └── user_token.json     # OAuth Token（自动管理）
```

## 常用维护命令

以下命令需要在命令行窗口中运行（和安装时一样）。每次运行前，先进入飞书助手目录：

**进入目录（每次都要先执行这一步）：**

Windows：
```
cd C:\Users\你的用户名\.claude\skills\feishu-assistant
```

macOS：
```
cd ~/.claude/skills/feishu-assistant
```

确认进入目录后，再复制粘贴下面需要的命令。**每次只复制一条命令**，按回车执行：

---

**检查配置是否正确：**
```
python scripts/feishu_client.py check-config
```

**刷新通讯录：**
```
python scripts/feishu_client.py refresh-contacts
```

**刷新知识库列表：**
```
python scripts/feishu_client.py refresh-spaces
```

**重新 OAuth 授权：**
```
python scripts/oauth_server.py
```

**重新运行安装引导：**
```
python scripts/setup.py
```

> macOS / Linux 上把 `python` 换成 `python3`。

## 安全提醒

- `config.json` 包含你的应用密钥，**不要分享给别人**
- `cache/user_token.json` 包含你的登录凭证，**不要分享给别人**
- 以上文件已在 `.gitignore` 中排除，不会被 git 提交

## 常见问题

**Q: `python3` 命令提示找不到？**
A: Windows 上试试用 `python` 代替 `python3`。如果还是不行，说明 Python 没装或者没加入 PATH，请回到上面的"安装前准备"重新安装 Python，记得勾选 "Add Python to PATH"。

**Q: 报错 "config.json 不存在"？**
A: 运行 `python3 scripts/setup.py` 完成初始配置。

**Q: 报错 "用户 token 不可用"？**
A: 运行 `python3 scripts/oauth_server.py` 完成 OAuth 授权。

**Q: 发消息报错 "Bot has NO availability"？**
A: 在飞书开放平台 → 你的应用 → 版本管理与发布 → 将可用范围设为「所有员工」→ 重新发布。

**Q: 通讯录是空的？**
A: 运行 `python3 scripts/feishu_client.py refresh-contacts`。如果仍为空，检查应用是否有通讯录权限。

**Q: 安装引导中途出错了怎么办？**
A: 可以随时重新运行 `python3 scripts/setup.py`，会从头开始引导。已填过的信息不会丢失。

**Q: macOS 上弹出 "xcode-select" 安装提示？**
A: 这是正常的，按提示安装即可。安装完后重新运行命令。
