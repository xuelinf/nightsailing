# wechat-desktop

## 目录说明

Windows 微信桌面自动化技能（开发中）。

## 技术方案

基于 OCR 和桌面自动化技术实现微信消息的读取和发送。

**核心技术栈：**
- RapidOCR - 快速 OCR 识别
- pyautogui - 鼠标键盘控制
- mss - 快速截图
- pygetwindow - 窗口管理
- pyperclip - 剪贴板操作

## 计划功能

- `ocr.py` - OCR 工具
- `wechat_utils.py` - 微信窗口管理
- `wechat_read.py` - 读取聊天内容
- `wechat_send.py` - 发送消息
- `wechat_monitor.py` - 后台监控

## 开发状态

当前处于调研阶段，详见 `01_Active_Projects/Windows微信自动回复Skill可行性调研.md`。

## 参考

基于 macOS wechat-desktop skill 的方法论移植到 Windows 平台。
