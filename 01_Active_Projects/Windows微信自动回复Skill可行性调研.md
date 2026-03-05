---
name: Windows 微信自动回复 Skill 可行性调研
description: 基于 macOS wechat-desktop skill 的方法论，调研在 Windows 平台实现类似功能的技术方案和可行性评估
created: 2026-03-05
last_modified: 2026-03-05
author: 夜航船
---

# Windows 微信自动回复 Skill 可行性调研

## 一、macOS 方案核心技术栈分析

### 1.1 技术架构

**核心理念：触觉反馈**
- 不截全屏传 AI（慢、贵）
- 用 macOS 原生 OCR 当"触觉"
- 鼠标移到哪 → OCR 哪 → Agent 知道手在哪、摸到什么

### 1.2 技术栈拆解

| 功能模块 | macOS 技术 | 实现方式 | 性能 |
|---------|-----------|---------|------|
| **OCR** | Vision Framework | PyObjC 调用原生 API | 快速模式 ~240ms<br>精确模式 ~870ms |
| **鼠标控制** | cliclick | CLI 工具 | < 10ms |
| **键盘输入** | osascript + cliclick | AppleScript + CLI | < 50ms |
| **截图** | screencapture | 系统命令 | < 50ms |
| **窗口管理** | osascript | AppleScript | < 50ms |
| **剪贴板** | pbcopy/pbpaste | 系统命令 | < 10ms |

### 1.3 核心方法论

**操作流程（标准）：**
```
1. 全屏 OCR 找目标 → 获取坐标
2. 移动鼠标 + 局部 OCR 确认 → 触觉反馈
3. 点击操作
4. 局部 OCR 验证结果 → 确认成功
```

**微信操控关键参数：**
- `SIDEBAR=310`：侧边栏宽度（图标60 + 列表250）
- `TITLE_H=50`：标题栏高度
- `INPUT_H=110`：输入框+工具栏高度
- 聊天区域 = 窗口 - 侧边栏 - 标题栏 - 输入框

**监控机制：**
- 后台轮询截图 + OCR
- 内容 hash 对比检测变化
- 关键词触发（@MYCC）
- 冷却机制防重复触发

---

## 二、Windows 平台技术方案调研

### 2.1 OCR 技术方案对比

| 方案 | 优势 | 劣势 | 性能 | 中文支持 |
|------|------|------|------|---------|
| **Windows.Media.Ocr** | 系统原生，免费，轻量 | 需要 UWP API，Python 调用复杂 | 快 (~300ms) | ✓ 优秀 |
| **Tesseract OCR** | 开源，成熟，跨平台 | 精度一般，需要训练 | 中等 (~500ms) | ✓ 可用 |
| **PaddleOCR** | 精度高，中文优秀 | 依赖重（深度学习），体积大 | 慢 (~1-2s) | ✓✓ 极佳 |
| **EasyOCR** | 精度高，易用 | 依赖重，体积大 | 慢 (~1-2s) | ✓✓ 极佳 |
| **RapidOCR** | 轻量，速度快，中文好 | 相对较新 | 快 (~200-400ms) | ✓✓ 优秀 |

**推荐方案：RapidOCR**
- 轻量级（~50MB）
- 速度接近原生（200-400ms）
- 中文识别优秀
- 纯 Python，易集成

**备选方案：Windows.Media.Ocr**
- 系统原生，零依赖
- 通过 `winrt` 包调用
- 速度最快

### 2.2 桌面自动化技术方案

| 功能 | 推荐方案 | 备选方案 | 说明 |
|------|---------|---------|------|
| **鼠标控制** | pyautogui | pynput, win32api | pyautogui 最简单，跨平台 |
| **键盘输入** | pyautogui | pynput, win32api | 支持中文输入 |
| **截图** | mss | pyautogui, PIL | mss 最快（~30ms） |
| **窗口管理** | pygetwindow | win32gui | pygetwindow 更简洁 |
| **剪贴板** | pyperclip | win32clipboard | pyperclip 跨平台 |

**技术栈选型：**
```python
# 核心依赖
rapidocr-onnxruntime  # OCR
pyautogui             # 鼠标+键盘
mss                   # 快速截图
pygetwindow           # 窗口管理
pyperclip             # 剪贴板
```

### 2.3 Windows 微信桌面版特性

**窗口结构：**
- 进程名：`WeChat.exe`
- 窗口标题：`微信` 或联系人名称
- 界面布局与 macOS 版本类似（侧边栏 + 聊天区 + 输入框）

**可操作性：**
- ✓ 可通过 win32gui 获取窗口句柄
- ✓ 可截图指定窗口区域
- ✓ 可模拟鼠标点击
- ✓ 可模拟键盘输入（包括中文）
- ✓ 可读写剪贴板

**潜在问题：**
- Windows 微信可能有多个窗口（主窗口、聊天窗口）
- 需要识别当前活动的聊天窗口
- DPI 缩放可能影响坐标计算

---

## 三、可行性评估

### 3.1 技术可行性：✓ 高度可行

| 功能模块 | macOS 实现 | Windows 对应方案 | 可行性 |
|---------|-----------|----------------|--------|
| OCR | Vision Framework | RapidOCR | ✓✓ 可行 |
| 鼠标控制 | cliclick | pyautogui | ✓✓ 可行 |
| 键盘输入 | osascript | pyautogui | ✓✓ 可行 |
| 截图 | screencapture | mss | ✓✓ 可行 |
| 窗口管理 | osascript | pygetwindow | ✓✓ 可行 |
| 剪贴板 | pbcopy | pyperclip | ✓✓ 可行 |

### 3.2 性能对比预估

| 操作 | macOS | Windows 预估 |
|------|-------|-------------|
| 鼠标移动/点击 | < 10ms | < 20ms |
| 局部 OCR | ~250ms | ~300-400ms |
| 全屏 OCR | ~240-870ms | ~400-800ms |
| 截图 | < 50ms | ~30-50ms |
| 窗口操作 | < 50ms | ~50-100ms |

**结论：性能略低于 macOS，但完全可用**

### 3.3 核心差异点

| 差异项 | macOS | Windows | 影响 |
|-------|-------|---------|------|
| OCR API | 系统原生 | 第三方库 | 需要安装依赖 |
| 脚本语言 | Bash + Python | Python | 需要重写 shell 脚本 |
| 窗口管理 | AppleScript | win32gui | API 不同，需要适配 |
| DPI 缩放 | 统一 Retina | 可变 DPI | 需要处理 DPI 感知 |

---

## 四、实现计划

### 4.1 技术架构

```
Windows 微信自动回复 Skill
├── ocr.py              # OCR 工具（RapidOCR）
├── wechat_utils.py     # 微信窗口管理工具
├── wechat_read.py      # 读取聊天内容
├── wechat_send.py      # 发送消息
├── wechat_monitor.py   # 后台监控
└── SKILL.md            # Skill 文档
```

### 4.2 实现步骤

**Phase 1: 基础工具开发（2-3天）**
1. 实现 `ocr.py`：
   - 集成 RapidOCR
   - 支持全屏/区域/窗口截图 + OCR
   - 返回文字 + 坐标（JSON 格式）

2. 实现 `wechat_utils.py`：
   - 查找微信窗口
   - 获取窗口位置、大小
   - 激活窗口
   - 处理 DPI 缩放

**Phase 2: 核心功能开发（3-4天）**
3. 实现 `wechat_read.py`：
   - 截取聊天区域
   - OCR 识别聊天内容
   - 返回文字列表

4. 实现 `wechat_send.py`：
   - 点击输入框
   - 输入文字（剪贴板方式）
   - 发送消息
   - OCR 验证发送成功

**Phase 3: 监控与集成（2-3天）**
5. 实现 `wechat_monitor.py`：
   - 后台轮询监控
   - 内容变化检测
   - 关键词触发
   - 写入触发文件

6. 编写 `SKILL.md`：
   - 使用说明
   - API 文档
   - 安全规则

**Phase 4: 测试与优化（2-3天）**
7. 功能测试：
   - 各模块单独测试
   - 集成测试
   - 边界情况测试

8. 性能优化：
   - OCR 速度优化
   - 截图优化
   - 内存优化

### 4.3 关键技术点

**1. DPI 感知处理**
```python
import ctypes
# 设置 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(2)
```

**2. 窗口坐标获取**
```python
import pygetwindow as gw
# 查找微信窗口
windows = gw.getWindowsWithTitle('微信')
if windows:
    win = windows[0]
    x, y, w, h = win.left, win.top, win.width, win.height
```

**3. 快速截图**
```python
import mss
with mss.mss() as sct:
    monitor = {"top": y, "left": x, "width": w, "height": h}
    img = sct.grab(monitor)
```

**4. OCR 调用**
```python
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
result, elapse = ocr(img)
# result: [[bbox, text, confidence], ...]
```

**5. 中文输入**
```python
import pyperclip
import pyautogui
# 通过剪贴板输入中文
pyperclip.copy(text)
pyautogui.hotkey('ctrl', 'v')
```

### 4.4 风险与应对

| 风险 | 影响 | 应对方案 |
|------|------|---------|
| OCR 精度不足 | 识别错误 | 使用精确模式，增加验证机制 |
| 窗口焦点抢夺 | 操作失败 | 添加延迟，检测窗口状态 |
| DPI 缩放问题 | 坐标错误 | 正确处理 DPI 感知 |
| 微信更新界面 | 坐标失效 | 动态计算坐标，不硬编码 |
| 性能不足 | 响应慢 | 优化 OCR 区域，使用快速模式 |

---

## 五、总结

### 5.1 可行性结论

**✓ 高度可行**

Windows 平台完全可以实现与 macOS 版本相同的功能：
- OCR 能力：RapidOCR 可替代 Vision Framework
- 自动化能力：pyautogui + mss 可替代 cliclick + screencapture
- 性能表现：略低于 macOS，但完全满足实时交互需求

### 5.2 核心优势

1. **技术成熟**：所有依赖库都是成熟的开源项目
2. **纯 Python**：无需 shell 脚本，更易维护
3. **跨平台潜力**：pyautogui 等库支持跨平台
4. **轻量级**：总依赖 < 100MB

### 5.3 预期效果

- 读取聊天：~500ms
- 发送消息：~800ms
- 监控轮询：5s 间隔
- OCR 精度：> 95%（中文）

### 5.4 下一步行动

1. 搭建开发环境（安装依赖）
2. 实现 OCR 工具原型
3. 测试微信窗口操作
4. 逐步实现完整功能
