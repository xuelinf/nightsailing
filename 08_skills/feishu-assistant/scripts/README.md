# feishu-assistant/scripts

## 目录说明

飞书助手的核心脚本文件。

## 文件说明

- `feishu_client.py` - 飞书 API 客户端，提供所有飞书操作命令
- `oauth_server.py` - OAuth 授权服务器，用于获取用户授权
- `setup.py` - 安装引导脚本，帮助用户完成初始配置
- `config.example.json` - 配置文件模板
- `scopes.json` - OAuth 权限范围定义

## 配置文件

实际使用时需要创建 `config.json`（从 `config.example.json` 复制），包含：
- 飞书应用凭证（app_id, app_secret）
- OAuth 授权范围
- 默认群聊 ID
- 团队成员映射

## 缓存目录

`cache/` 目录（自动生成）存放：
- `contacts.json` - 通讯录缓存
- `wiki_spaces.json` - 知识库列表缓存
- `user_token.json` - 用户授权 token
