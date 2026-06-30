# 夜航船之书内容

这个文件是网站的内容源。页面会读取这里的站点信息和工具目录；字段名尽量不要改，字段值可以直接改。写新产品时，先补这个文件，再补对应截图或下载文件。

## 新产品资料清单

新产品加入夜航船之书时，建议至少提供这些资料：

1. 基本信息：产品名、短名、slug、当前状态、平台、是否开源、下载链接或预告状态。
2. 一句话定位：用一句话说明它解决什么具体问题，不写宣传口号。
3. 三条主要能力：用户点开前就能判断它是否有用。
4. 三个使用场景：说明什么时候会打开它。
5. 真实素材：应用截图、录屏、图标、下载文件、仓库地址；没有素材就写清楚“素材待补”，不要造假。
6. 边界说明：隐私、联网、密钥、数据保存位置、当前限制。
7. 维护信息：当前版本、发布日期、更新日志、下一步计划。

内容原则：

- 优先展示事实，不展示炫技过程。
- 优先让用户找到下载和源码，不让用户先读长叙事。
- 可以有调性，但调性服务于判断，不替代信息。
- 不使用虚构指标、虚拟 Prompt 或为了“像 AI 产品”而添加的装饰文案。

## 站点信息

- name: 夜航船之书
- version: 0.0.4
- githubHref: https://github.com/xuelinf/nightsailing
- edition: 庚午夏 · 去繁校
- headline: 一册个人 AI 工具目录。
- description: 收录我已经发布、正在打磨和计划开发的小工具。每个条目都尽量说清楚：它解决什么问题、能不能下载、是否开源、后续素材在哪里补。
- primaryCta: 查看工具
- secondaryCta: 维护约定

## 工具目录

### AI航行日记

- slug: ai-sailing-log
- shortName: 航行日记
- status: available
- statusLabel: 可下载
- openSourceLabel: 已开源
- category: 本机用量
- platform: macOS
- stage: 已发布
- visual: ai-sailing-log
- downloadHref: /downloads/AI航行日记-0.1.0.dmg
- sourceHref: https://github.com/xuelinf/vibe-token-usage
- summary: macOS 菜单栏里的 AI token 用量查看工具。
- detail: 它读取本机 Codex 与 Claude Code 的使用记录，帮助你查看今日用量、额度窗口和近期使用节奏。定位是轻量、私有、可复盘，而不是复杂的数据看板。
- privacy: 默认只读取本机日志，不上传数据。
- releaseNote: 首个已发布工具，当前可下载并查看源码。
- highlights:
  - Codex 与 Claude Code 用量聚合
  - 今日 token 与额度窗口
  - 近期使用热力图
- useCases:
  - 检查当日额度
  - 复盘近期使用峰谷
  - 观察自己的 AI 工作节奏
- materials:
  - 真实截图待补
  - 使用演示待补
  - 更新日志待补

### 问玄

- slug: wenxuan
- shortName: 问玄
- status: available
- statusLabel: 可下载
- openSourceLabel: 暂未开源
- category: 桌面托盘
- platform: macOS
- stage: 已发布
- visual: wenxuan
- downloadHref: /downloads/问玄.dmg
- sourceHref:
- summary: 起卦、排盘与 AI 参断的 macOS 托盘工具。
- detail: 问玄把提问、铜钱起卦、六爻排盘和模型解读整理成一个可重复的桌面流程。它保留传统结构，也把卦盘数据交给模型做辅助解释。
- privacy: AI 解卦通过本地代理读取模型密钥，前端不暴露 API key。
- releaseNote: 第二个已发布工具，目前提供 DMG 下载，源码暂不公开。
- highlights:
  - 铜钱起卦交互
  - 六爻结构化排盘
  - AI 解卦入口
- useCases:
  - 记录一次具体提问
  - 生成结构化卦盘
  - 调用模型生成参断
- materials:
  - 卦盘截图待补
  - 起卦过程视频待补
  - 解读示例待补

### 端口占用管理器

- slug: port-keeper
- shortName: 端口管理
- status: planned
- statusLabel: 计划中
- openSourceLabel: 预留舱位
- category: 本地开发
- platform: macOS / 本地开发
- stage: 预研中
- visual: port-keeper
- downloadHref:
- sourceHref:
- summary: 快速查看端口被谁占用，并辅助处理本机开发冲突。
- detail: 它面向本地开发场景：当端口被占用时，直接看到进程、路径、来源和可执行操作。目标不是替代终端，而是把高频排障压缩成一次确认。
- privacy: 计划做成本机工具，不上传端口或进程数据。
- releaseNote: 原型稳定后补下载入口、进程树截图和安全释放演示。
- highlights:
  - 端口占用查看
  - 进程定位
  - 快速释放端口
- useCases:
  - 定位冲突端口
  - 查看进程来源
  - 安全释放占用
- materials:
  - 端口列表截图待补
  - 进程树演示待补
  - 安全操作说明待补

### AI 语音输入

- slug: ai-voice-input
- shortName: 语音输入
- status: planned
- statusLabel: 计划中
- openSourceLabel: 免费开源
- category: 输入工具
- platform: 桌面输入工具
- stage: 设计中
- visual: ai-voice-input
- downloadHref:
- sourceHref:
- summary: 可接入多家 ASR 模型的免费开源桌面语音输入工具。
- detail: 它会尽量保持自由、轻量、可替换模型：不绑定单一厂商，用户可以接入自己信任的 ASR 服务，也可以把语音输入流程留在自己可控的环境里。
- privacy: 计划支持用户自配模型与密钥，避免把语音输入锁进单一服务。
- releaseNote: 设计稳定后补录音浮窗、模型切换和转写演示。
- highlights:
  - 多家 ASR 模型接入
  - 免费开源
  - 可自配置密钥
- useCases:
  - 快速转写
  - 切换 ASR 模型
  - 配置自己的隐私边界
- materials:
  - 录音浮窗待补
  - 模型配置待补
  - 转写演示待补
