#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书助手 API 客户端
通用版本，所有个性化配置从 config.json 读取。

作者：凯寓 (KAIYU)
"""

import json
import os
import re
import sys
import time
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
import requests


# ─── 路径定义 ───────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
CACHE_DIR = SCRIPTS_DIR / "cache"
CONFIG_PATH = SCRIPTS_DIR / "config.json"
USER_TOKEN_PATH = CACHE_DIR / "user_token.json"
CONTACTS_CACHE_PATH = CACHE_DIR / "contacts.json"
SPACES_CACHE_PATH = CACHE_DIR / "wiki_spaces.json"


def ensure_utf8():
    """确保控制台能正常显示中文"""
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ─── FeishuClient 核心类 ────────────────────────────────────
class FeishuClient:
    """飞书 API 客户端"""

    PERMISSION_ERROR_CODES = {99991668, 99991672, 99991663, 99991664}

    def __init__(self, app_id: str, app_secret: str, user_token_file: Optional[str] = None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self._access_token = None
        self._token_expire_time = 0
        self.user_token_file = user_token_file
        self._user_token_data = None

    def get_access_token(self, token_type: str = "app") -> str:
        """获取 access_token（app 或 tenant）"""
        if self._access_token and time.time() < self._token_expire_time:
            return self._access_token

        if token_type == "tenant":
            url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
            token_key = "tenant_access_token"
        else:
            url = f"{self.base_url}/auth/v3/app_access_token/internal"
            token_key = "app_access_token"

        response = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        })
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取 access_token 失败: {data.get('msg')}")

        self._access_token = data[token_key]
        self._token_expire_time = time.time() + data["expire"] - 300
        return self._access_token

    def get_user_access_token(self) -> Optional[str]:
        """获取用户 access_token（自动刷新）"""
        if not self.user_token_file:
            return None

        token_path = Path(self.user_token_file)
        if not token_path.exists():
            return None

        if not self._user_token_data:
            with open(token_path, "r", encoding="utf-8") as f:
                self._user_token_data = json.load(f)

        token_time = self._user_token_data.get("_token_time", 0)
        expires_in = self._user_token_data.get("expires_in", 7200)

        if time.time() > token_time + expires_in - 300:
            self._refresh_user_token()

        return self._user_token_data.get("access_token")

    def _refresh_user_token(self):
        """刷新用户 access_token"""
        app_token = self.get_access_token("app")

        response = requests.post(
            f"{self.base_url}/authen/v1/oidc/refresh_access_token",
            json={
                "grant_type": "refresh_token",
                "refresh_token": self._user_token_data["refresh_token"],
            },
            headers={
                "Authorization": f"Bearer {app_token}",
                "Content-Type": "application/json",
            },
        )
        data = response.json()

        if data.get("code") != 0:
            # refresh_token 过期，自动重新授权
            print("\n" + "=" * 56)
            print("  用户授权已过期（超过 30 天未使用）")
            print("  正在自动启动授权流程...")
            print("=" * 56)

            oauth_script = SCRIPTS_DIR / "oauth_server.py"
            try:
                subprocess.run([sys.executable, str(oauth_script)], check=True)
                with open(self.user_token_file, "r", encoding="utf-8") as f:
                    self._user_token_data = json.load(f)
                print("\n  授权成功！继续执行...\n")
                return
            except subprocess.CalledProcessError as e:
                raise Exception(f"自动授权失败: {e}。请手动运行: {sys.executable} {oauth_script}")

        new_data = data.get("data", {})
        new_data["_token_time"] = time.time()
        self._user_token_data = new_data

        with open(self.user_token_file, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)

    def _request(self, method: str, endpoint: str, use_user_token: bool = False, **kwargs) -> Dict[str, Any]:
        """统一请求方法"""
        url = f"{self.base_url}{endpoint}"

        if use_user_token:
            token = self.get_user_access_token()
            if not token:
                raise Exception("用户 token 不可用，请先运行 setup.py 或 oauth_server.py 完成授权")
        else:
            token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.request(method, url, headers=headers, **kwargs)
        data = response.json()

        if data.get("code") != 0:
            self._raise_with_guidance(data, endpoint, use_user_token)

        return data.get("data", {})

    def _raise_with_guidance(self, data: Dict[str, Any], endpoint: str, use_user_token: bool):
        """解析 API 错误并给出修复建议"""
        code = data.get("code", 0)
        msg = data.get("msg", "")

        is_permission_error = (
            code in self.PERMISSION_ERROR_CODES
            or "Unauthorized" in msg
            or "permission" in msg.lower()
            or "scope" in msg.lower()
        )

        if is_permission_error:
            scope_match = re.search(r"[\w:]+:[\w:]+(?:readonly|read|write)", msg)
            missing_scope = scope_match.group(0) if scope_match else None

            hint_lines = [f"API 权限不足 (code={code}): {msg}", "", "修复步骤:"]

            if missing_scope:
                hint_lines.append(f"  1. 在 config.json 的 oauth_scopes 中添加: {missing_scope}")
            else:
                hint_lines.append("  1. 检查 config.json 的 oauth_scopes 是否包含该 API 所需的 scope")

            if use_user_token:
                hint_lines.append("  2. 运行 oauth_server.py 重新授权（scope 变更后必须重新授权）")
            else:
                hint_lines.append("  2. 在飞书开放平台后台确认应用已开通对应权限")

            hint_lines.append("  3. 飞书开放平台: https://open.feishu.cn/app")
            raise Exception("\n".join(hint_lines))

        raise Exception(f"API 请求失败 (code={code}): {msg}")

    # ─── 消息 ──────────────────────────────────────────────
    def send_message(self, receive_id: str, msg_type: str, content: str, receive_id_type: str = "open_id") -> Dict[str, Any]:
        """发送消息"""
        if msg_type == "text":
            content_obj = {"text": content}
        elif msg_type == "post":
            content_obj = {"zh_cn": {"title": "", "content": [[{"tag": "text", "text": content}]]}}
        else:
            content_obj = json.loads(content) if isinstance(content, str) else content

        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(content_obj),
        }
        return self._request("POST", "/im/v1/messages", json=payload, params={"receive_id_type": receive_id_type})

    def get_chat_messages(self, chat_id: str, page_size: int = 20, start_time: Optional[str] = None, page_token: Optional[str] = None) -> Dict[str, Any]:
        """获取群组消息"""
        params = {"container_id_type": "chat", "container_id": chat_id, "page_size": min(page_size, 50)}
        if start_time:
            params["start_time"] = start_time
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", "/im/v1/messages", params=params)

    # ─── 群聊 ──────────────────────────────────────────────
    def create_chat(self, name: str, member_ids: List[str], description: str = "") -> Dict[str, Any]:
        """创建群聊并拉入成员"""
        payload = {
            "name": name,
            "user_id_list": member_ids,
        }
        if description:
            payload["description"] = description
        return self._request("POST", "/im/v1/chats", json=payload, params={"user_id_type": "open_id"})

    def add_chat_members(self, chat_id: str, member_ids: List[str]) -> Dict[str, Any]:
        """向群聊添加成员"""
        return self._request("POST", f"/im/v1/chats/{chat_id}/members", json={"id_list": member_ids}, params={"member_id_type": "open_id"})

    def remove_chat_members(self, chat_id: str, member_ids: List[str]) -> Dict[str, Any]:
        """从群聊移除成员"""
        return self._request("DELETE", f"/im/v1/chats/{chat_id}/members", json={"id_list": member_ids}, params={"member_id_type": "open_id"})

    def update_chat(self, chat_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """修改群聊信息（群名、群描述等）"""
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        return self._request("PUT", f"/im/v1/chats/{chat_id}", json=payload)

    def get_chat_info(self, chat_id: str) -> Dict[str, Any]:
        """获取群聊信息"""
        return self._request("GET", f"/im/v1/chats/{chat_id}")

    def list_chat_members(self, chat_id: str, page_size: int = 50, page_token: Optional[str] = None) -> Dict[str, Any]:
        """列出群聊成员"""
        params = {"member_id_type": "open_id", "page_size": min(page_size, 50)}
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", f"/im/v1/chats/{chat_id}/members", params=params)

    def dissolve_chat(self, chat_id: str) -> Dict[str, Any]:
        """解散群聊"""
        return self._request("DELETE", f"/im/v1/chats/{chat_id}")

    # ─── 文档 ──────────────────────────────────────────────
    def create_document(self, title: str, content: str = "", folder_token: Optional[str] = None) -> Dict[str, Any]:
        """创建文档（用户身份）"""
        payload = {"title": title}
        if folder_token:
            payload["folder_token"] = folder_token
        result = self._request("POST", "/docx/v1/documents", use_user_token=True, json=payload)
        if content:
            doc_token = result["document"]["document_id"]
            self.update_document(doc_token, content)
        return result

    def update_document(self, doc_token: str, content: str) -> Dict[str, Any]:
        """更新文档（追加内容）"""
        blocks_data = self._request("GET", f"/docx/v1/documents/{doc_token}/blocks", use_user_token=True)
        items = blocks_data.get("items", [])
        if not items:
            raise Exception("文档为空，无法找到根 block")

        page_block_id = items[0].get("block_id")
        payload = {
            "children": [{
                "block_type": 2,
                "text": {"elements": [{"text_run": {"content": content}}]},
            }]
        }
        return self._request("POST", f"/docx/v1/documents/{doc_token}/blocks/{page_block_id}/children", use_user_token=True, json=payload)

    # ─── 文件上传 ──────────────────────────────────────────
    def upload_file(self, file_path: str, parent_node: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """上传文件到飞书云文档"""
        if not file_name:
            file_name = Path(file_path).name
        with open(file_path, "rb") as f:
            url = f"{self.base_url}/drive/v1/files/upload_all"
            headers = {"Authorization": f"Bearer {self.get_access_token()}"}
            response = requests.post(url, headers=headers, data={"parent_node": parent_node, "file_name": file_name}, files={"file": (file_name, f, "application/octet-stream")})
            result = response.json()
            if result.get("code") != 0:
                raise Exception(f"上传文件失败: {result.get('msg')}")
            return result.get("data", {})

    # ─── 日历 ──────────────────────────────────────────────
    def _parse_time(self, time_str: str) -> str:
        """将 'YYYY-MM-DD HH:MM' 格式转为 Unix 时间戳字符串"""
        from datetime import datetime
        return str(int(datetime.strptime(time_str, "%Y-%m-%d %H:%M").timestamp()))

    def list_calendars(self) -> Dict[str, Any]:
        """列出用户的日历列表"""
        return self._request("GET", "/calendar/v4/calendars", use_user_token=True)

    def _resolve_calendar_id(self, calendar_id: str) -> str:
        """将 'primary' 解析为用户主日历的真实 calendar_id"""
        if calendar_id != "primary":
            return calendar_id
        data = self.list_calendars()
        for cal in data.get("calendar_list", []):
            if cal.get("type") == "primary":
                return cal["calendar_id"]
        raise Exception("未找到主日历，请使用 list-calendars 查看可用日历并指定 calendar_id")

    def list_calendar_events(self, calendar_id: str = "primary", start_time: Optional[str] = None, end_time: Optional[str] = None, page_size: int = 50, page_token: Optional[str] = None) -> Dict[str, Any]:
        """列出日历事件，支持时间范围过滤"""
        calendar_id = self._resolve_calendar_id(calendar_id)
        params = {"page_size": min(page_size, 50)}
        if start_time:
            params["start_time"] = self._parse_time(start_time)
        if end_time:
            params["end_time"] = self._parse_time(end_time)
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", f"/calendar/v4/calendars/{calendar_id}/events", use_user_token=True, params=params)

    def get_calendar_event(self, calendar_id: str, event_id: str) -> Dict[str, Any]:
        """获取单个日历事件详情"""
        calendar_id = self._resolve_calendar_id(calendar_id)
        return self._request("GET", f"/calendar/v4/calendars/{calendar_id}/events/{event_id}", use_user_token=True)

    def create_calendar_event(self, summary: str, start_time: str, end_time: str, description: str = "", attendees: Optional[list] = None, calendar_id: str = "primary") -> Dict[str, Any]:
        """创建日历事件"""
        calendar_id = self._resolve_calendar_id(calendar_id)
        payload = {
            "summary": summary, "description": description,
            "start_time": {"timestamp": self._parse_time(start_time)},
            "end_time": {"timestamp": self._parse_time(end_time)},
        }
        if attendees:
            payload["attendees"] = [{"type": "user", "user_id": a} for a in attendees]
        return self._request("POST", f"/calendar/v4/calendars/{calendar_id}/events", use_user_token=True, json=payload)

    def update_calendar_event(self, calendar_id: str, event_id: str, summary: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """更新日历事件"""
        calendar_id = self._resolve_calendar_id(calendar_id)
        payload = {}
        if summary is not None:
            payload["summary"] = summary
        if description is not None:
            payload["description"] = description
        if start_time is not None:
            payload["start_time"] = {"timestamp": self._parse_time(start_time)}
        if end_time is not None:
            payload["end_time"] = {"timestamp": self._parse_time(end_time)}
        return self._request("PATCH", f"/calendar/v4/calendars/{calendar_id}/events/{event_id}", use_user_token=True, json=payload)

    def delete_calendar_event(self, calendar_id: str, event_id: str) -> Dict[str, Any]:
        """删除日历事件"""
        calendar_id = self._resolve_calendar_id(calendar_id)
        return self._request("DELETE", f"/calendar/v4/calendars/{calendar_id}/events/{event_id}", use_user_token=True)

    # ─── 通讯录 ────────────────────────────────────────────
    def get_user_info(self, email: str) -> Dict[str, Any]:
        """根据邮箱获取用户信息"""
        return self._request("POST", "/contact/v3/users/batch_get_id", params={"emails": email})

    def list_departments(self, parent_department_id: str = "0") -> Dict[str, Any]:
        """获取部门列表"""
        return self._request("GET", "/contact/v3/departments", params={"parent_department_id": parent_department_id, "fetch_child": True, "page_size": 50})

    def list_department_users(self, department_id: str) -> Dict[str, Any]:
        """获取部门成员列表"""
        return self._request("GET", "/contact/v3/users", params={"department_id": department_id, "page_size": 50})

    def get_user_by_id(self, user_id: str, user_id_type: str = "open_id") -> Dict[str, Any]:
        """根据 ID 获取用户详情"""
        return self._request("GET", f"/contact/v3/users/{user_id}", params={"user_id_type": user_id_type})

    def get_tenant_info(self) -> Dict[str, Any]:
        """获取企业信息"""
        return self._request("GET", "/tenant/v2/tenant/query")

    # ─── 知识库 ────────────────────────────────────────────
    def list_wiki_spaces(self, page_size: int = 50, page_token: Optional[str] = None) -> Dict[str, Any]:
        """列出知识库空间"""
        params = {"page_size": min(page_size, 50)}
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", "/wiki/v2/spaces", use_user_token=True, params=params)

    def list_wiki_nodes(self, space_id: str, parent_node_token: Optional[str] = None, page_size: int = 20, page_token: Optional[str] = None) -> Dict[str, Any]:
        """列出知识库节点"""
        params = {"page_size": min(page_size, 50)}
        if parent_node_token:
            params["parent_node_token"] = parent_node_token
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", f"/wiki/v2/spaces/{space_id}/nodes", use_user_token=True, params=params)

    def get_wiki_node(self, token: str) -> Dict[str, Any]:
        """获取知识库节点信息"""
        return self._request("GET", "/wiki/v2/spaces/get_node", use_user_token=True, params={"token": token})

    def read_wiki_node_content(self, node_token: str) -> Dict[str, Any]:
        """读取知识库文章纯文本"""
        node_info = self.get_wiki_node(node_token)
        node = node_info.get("node", {})
        obj_token = node.get("obj_token")
        obj_type = node.get("obj_type")
        title = node.get("title", "")

        if not obj_token:
            raise Exception(f"无法获取节点文档 token: {node_info}")

        if obj_type in ("doc", "docx"):
            content_data = self._request("GET", f"/docx/v1/documents/{obj_token}/raw_content", use_user_token=True)
            return {"title": title, "obj_type": obj_type, "obj_token": obj_token, "content": content_data.get("content", "")}
        else:
            return {"title": title, "obj_type": obj_type, "obj_token": obj_token, "content": f"[不支持直接读取的类型: {obj_type}，请在飞书中查看]"}


# ─── 配置加载 ──────────────────────────────────────────────
def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        print("错误: 未找到 config.json")
        print(f"请先运行安装引导: {sys.executable} {SCRIPTS_DIR / 'setup.py'}")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    if USER_TOKEN_PATH.exists():
        config["user_token_file"] = str(USER_TOKEN_PATH)

    return config


def create_client(config: Dict[str, Any]) -> FeishuClient:
    """根据配置创建客户端"""
    return FeishuClient(config["app_id"], config["app_secret"], config.get("user_token_file"))


# ─── 缓存刷新命令 ──────────────────────────────────────────
def cmd_refresh_contacts(client: FeishuClient):
    """刷新通讯录缓存"""
    data = client.list_department_users("0")
    items = data.get("items", [])

    contacts = []
    for u in items:
        contacts.append({
            "name": u.get("name", ""),
            "open_id": u.get("open_id", ""),
            "mobile": u.get("mobile", ""),
            "status": "已激活" if u.get("status", {}).get("is_activated") else "未激活",
        })

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONTACTS_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

    # 同步更新 config.json 的 team_members
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    config["team_members"] = {c["name"]: c["open_id"] for c in contacts if c["name"]}
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"通讯录已刷新，共 {len(contacts)} 人，保存到 {CONTACTS_CACHE_PATH}")
    for c in contacts:
        print(f"  {c['name']:12s} {c['mobile']:16s} {c['open_id']}")


def cmd_refresh_spaces(client: FeishuClient):
    """刷新知识库空间缓存"""
    all_spaces = []
    page_token = None

    while True:
        data = client.list_wiki_spaces(page_size=50, page_token=page_token)
        items = data.get("items", [])
        for s in items:
            all_spaces.append({
                "name": s.get("name", ""),
                "space_id": s.get("space_id", ""),
                "description": s.get("description", ""),
            })
        if not data.get("has_more"):
            break
        page_token = data.get("page_token")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(SPACES_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_spaces, f, indent=2, ensure_ascii=False)

    print(f"知识库空间已刷新，共 {len(all_spaces)} 个，保存到 {SPACES_CACHE_PATH}")
    for s in all_spaces:
        print(f"  {s['name']:30s} {s['space_id']}")


def cmd_show_contacts():
    """显示缓存的通讯录"""
    if not CONTACTS_CACHE_PATH.exists():
        print("通讯录缓存不存在，请先运行: refresh-contacts")
        return

    contacts = json.loads(CONTACTS_CACHE_PATH.read_text(encoding="utf-8"))
    print(f"团队通讯录（共 {len(contacts)} 人）：\n")
    print(f"  {'序号':4s} {'姓名':12s} {'手机号':16s} {'状态':8s} {'open_id'}")
    print("  " + "-" * 80)
    for i, c in enumerate(contacts, 1):
        print(f"  {i:<4d} {c['name']:12s} {c['mobile']:16s} {c['status']:8s} {c['open_id']}")


def cmd_show_spaces():
    """显示缓存的知识库列表"""
    if not SPACES_CACHE_PATH.exists():
        print("知识库缓存不存在，请先运行: refresh-spaces")
        return

    spaces = json.loads(SPACES_CACHE_PATH.read_text(encoding="utf-8"))
    print(f"知识库空间（共 {len(spaces)} 个）：\n")
    for s in spaces:
        desc = f"（{s['description']}）" if s.get("description") else ""
        print(f"  {s['name']:30s} {s['space_id']}  {desc}")


def cmd_show_org(client: FeishuClient):
    """显示组织信息"""
    data = client.get_tenant_info()
    tenant = data.get("tenant", {})
    print("组织信息：")
    print(f"  名称: {tenant.get('name', '未知')}")
    print(f"  域名: {tenant.get('domain', '未知')}")
    print(f"  显示ID: {tenant.get('display_id', '未知')}")
    print(f"  租户Key: {tenant.get('tenant_key', '未知')}")


def cmd_check_config():
    """检查配置完整性"""
    print("检查配置...\n")
    issues = []

    # config.json
    if not CONFIG_PATH.exists():
        print(f"  ❌ config.json 不存在")
        print(f"     请运行: {sys.executable} {SCRIPTS_DIR / 'setup.py'}")
        return
    print(f"  ✅ config.json 存在")

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    if not config.get("app_id") or config["app_id"] == "cli_xxx":
        issues.append("app_id 未配置")
    else:
        print(f"  ✅ app_id: {config['app_id']}")

    if not config.get("app_secret") or config["app_secret"] == "xxx":
        issues.append("app_secret 未配置")
    else:
        print(f"  ✅ app_secret: {'*' * 8}（已隐藏）")

    if config.get("default_chat_id"):
        print(f"  ✅ 默认群聊: {config['default_chat_id']}")
    else:
        print(f"  ⚠  默认群聊: 未设置（可选）")

    # token
    if USER_TOKEN_PATH.exists():
        token_data = json.loads(USER_TOKEN_PATH.read_text(encoding="utf-8"))
        token_time = token_data.get("_token_time", 0)
        refresh_expires = token_data.get("refresh_expires_in", 2592000)
        if time.time() > token_time + refresh_expires:
            issues.append("OAuth refresh_token 已过期，需要重新授权")
        else:
            remaining_days = int((token_time + refresh_expires - time.time()) / 86400)
            print(f"  ✅ OAuth 授权: 有效（还剩约 {remaining_days} 天）")
    else:
        issues.append("OAuth 授权未完成")

    # 缓存
    if CONTACTS_CACHE_PATH.exists():
        contacts = json.loads(CONTACTS_CACHE_PATH.read_text(encoding="utf-8"))
        print(f"  ✅ 通讯录缓存: {len(contacts)} 人")
    else:
        print(f"  ⚠  通讯录缓存: 不存在（运行 refresh-contacts 生成）")

    if SPACES_CACHE_PATH.exists():
        spaces = json.loads(SPACES_CACHE_PATH.read_text(encoding="utf-8"))
        print(f"  ✅ 知识库缓存: {len(spaces)} 个空间")
    else:
        print(f"  ⚠  知识库缓存: 不存在（运行 refresh-spaces 生成）")

    if issues:
        print(f"\n  ⚠ 发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"     - {issue}")
    else:
        print("\n  🎉 配置完整，一切就绪！")


# ─── CLI 入口 ──────────────────────────────────────────────
def main():
    ensure_utf8()

    parser = argparse.ArgumentParser(description="飞书助手 API 客户端")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # ── 管理命令 ──
    subparsers.add_parser("check-config", help="检查配置完整性")
    subparsers.add_parser("refresh-contacts", help="刷新通讯录缓存")
    subparsers.add_parser("refresh-spaces", help="刷新知识库空间缓存")
    subparsers.add_parser("show-contacts", help="显示通讯录")
    subparsers.add_parser("show-spaces", help="显示知识库列表")
    subparsers.add_parser("show-org", help="显示组织信息")

    # ── 发送消息 ──
    p = subparsers.add_parser("send-message", help="发送消息")
    p.add_argument("--type", required=True, choices=["text", "post", "interactive", "image"])
    p.add_argument("--content", required=True)
    p.add_argument("--receive_id", required=True)
    p.add_argument("--receive_id_type", default="open_id")

    # ── 群消息 ──
    p = subparsers.add_parser("get-chat-messages", help="获取群组消息")
    p.add_argument("--chat_id", required=True)
    p.add_argument("--page_size", type=int, default=20)
    p.add_argument("--start_time", type=str)
    p.add_argument("--page_token", type=str)

    # ── 群聊管理 ──
    p = subparsers.add_parser("create-chat", help="创建群聊")
    p.add_argument("--name", required=True, help="群聊名称")
    p.add_argument("--members", required=True, help="成员 open_id，逗号分隔")
    p.add_argument("--description", default="")

    p = subparsers.add_parser("add-chat-members", help="向群聊添加成员")
    p.add_argument("--chat_id", required=True)
    p.add_argument("--members", required=True, help="成员 open_id，逗号分隔")

    p = subparsers.add_parser("remove-chat-members", help="从群聊移除成员")
    p.add_argument("--chat_id", required=True)
    p.add_argument("--members", required=True, help="成员 open_id，逗号分隔")

    p = subparsers.add_parser("get-chat-info", help="获取群聊信息")
    p.add_argument("--chat_id", required=True)

    p = subparsers.add_parser("update-chat", help="修改群聊信息")
    p.add_argument("--chat_id", required=True)
    p.add_argument("--name", help="新群名")
    p.add_argument("--description", help="新群描述")

    p = subparsers.add_parser("list-chat-members", help="列出群聊成员")
    p.add_argument("--chat_id", required=True)
    p.add_argument("--page_size", type=int, default=50)
    p.add_argument("--page_token", type=str)

    p = subparsers.add_parser("dissolve-chat", help="解散群聊")
    p.add_argument("--chat_id", required=True)

    # ── 文档 ──
    p = subparsers.add_parser("create-doc", help="创建文档")
    p.add_argument("--title", required=True)
    p.add_argument("--content", default="")
    p.add_argument("--folder_token")

    p = subparsers.add_parser("update-doc", help="更新文档")
    p.add_argument("--doc_token", required=True)
    p.add_argument("--content", required=True)

    # ── 日历 ──
    subparsers.add_parser("list-calendars", help="列出日历列表")

    p = subparsers.add_parser("list-events", help="列出日历事件")
    p.add_argument("--calendar_id", default="primary")
    p.add_argument("--start_time", type=str, help="起始时间，格式 YYYY-MM-DD HH:MM")
    p.add_argument("--end_time", type=str, help="结束时间，格式 YYYY-MM-DD HH:MM")
    p.add_argument("--page_size", type=int, default=50)
    p.add_argument("--page_token", type=str)

    p = subparsers.add_parser("get-event", help="获取日历事件详情")
    p.add_argument("--calendar_id", default="primary")
    p.add_argument("--event_id", required=True)

    p = subparsers.add_parser("create-event", help="创建日历事件")
    p.add_argument("--summary", required=True)
    p.add_argument("--start_time", required=True, help="格式 YYYY-MM-DD HH:MM")
    p.add_argument("--end_time", required=True, help="格式 YYYY-MM-DD HH:MM")
    p.add_argument("--calendar_id", default="primary")
    p.add_argument("--description", default="")
    p.add_argument("--attendees", help="参会人 open_id，逗号分隔")

    p = subparsers.add_parser("update-event", help="更新日历事件")
    p.add_argument("--calendar_id", default="primary")
    p.add_argument("--event_id", required=True)
    p.add_argument("--summary", type=str)
    p.add_argument("--start_time", type=str, help="格式 YYYY-MM-DD HH:MM")
    p.add_argument("--end_time", type=str, help="格式 YYYY-MM-DD HH:MM")
    p.add_argument("--description", type=str)

    p = subparsers.add_parser("delete-event", help="删除日历事件")
    p.add_argument("--calendar_id", default="primary")
    p.add_argument("--event_id", required=True)

    # ── 文件上传 ──
    p = subparsers.add_parser("upload-file", help="上传文件")
    p.add_argument("--file_path", required=True)
    p.add_argument("--parent_node", required=True)
    p.add_argument("--file_name")

    # ── 用户 ──
    p = subparsers.add_parser("get-user", help="通过邮箱查用户")
    p.add_argument("--email", required=True)

    p = subparsers.add_parser("get-user-detail", help="通过 ID 查用户详情")
    p.add_argument("--user_id", required=True)
    p.add_argument("--user_id_type", default="open_id")

    p = subparsers.add_parser("list-departments", help="获取部门列表")
    p.add_argument("--parent_id", default="0")

    p = subparsers.add_parser("list-department-users", help="获取部门成员")
    p.add_argument("--department_id", required=True)

    p = subparsers.add_parser("get-tenant-info", help="获取企业信息")

    # ── 知识库 ──
    p = subparsers.add_parser("list-wiki-spaces", help="列出知识库空间")
    p.add_argument("--page_size", type=int, default=50)
    p.add_argument("--page_token", type=str)

    p = subparsers.add_parser("list-wiki-nodes", help="列出知识库文章")
    p.add_argument("--space_id", required=True)
    p.add_argument("--parent_node_token", type=str)
    p.add_argument("--page_size", type=int, default=20)
    p.add_argument("--page_token", type=str)

    p = subparsers.add_parser("read-wiki-node", help="读取知识库文章内容")
    p.add_argument("--node_token", required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 不需要 API 连接的命令
    if args.command == "check-config":
        cmd_check_config()
        return
    if args.command == "show-contacts":
        cmd_show_contacts()
        return
    if args.command == "show-spaces":
        cmd_show_spaces()
        return

    # 需要 API 连接的命令
    config = load_config()
    client = create_client(config)

    try:
        if args.command == "refresh-contacts":
            cmd_refresh_contacts(client)
        elif args.command == "refresh-spaces":
            cmd_refresh_spaces(client)
        elif args.command == "show-org":
            cmd_show_org(client)
        elif args.command == "send-message":
            result = client.send_message(args.receive_id, args.type, args.content, args.receive_id_type)
            print(f"消息发送成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "get-chat-messages":
            result = client.get_chat_messages(args.chat_id, args.page_size, getattr(args, "start_time", None), getattr(args, "page_token", None))
            print(f"群组消息: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "create-doc":
            result = client.create_document(args.title, args.content, args.folder_token)
            print(f"文档创建成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "update-doc":
            result = client.update_document(args.doc_token, args.content)
            print(f"文档更新成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "create-event":
            attendees = args.attendees.split(",") if args.attendees else None
            result = client.create_calendar_event(args.summary, args.start_time, args.end_time, args.description, attendees, args.calendar_id)
            print(f"日历事件创建成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-calendars":
            result = client.list_calendars()
            print(f"日历列表: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-events":
            result = client.list_calendar_events(args.calendar_id, getattr(args, "start_time", None), getattr(args, "end_time", None), args.page_size, getattr(args, "page_token", None))
            print(f"日历事件: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "get-event":
            result = client.get_calendar_event(args.calendar_id, args.event_id)
            print(f"事件详情: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "update-event":
            result = client.update_calendar_event(args.calendar_id, args.event_id, args.summary, args.start_time, args.end_time, args.description)
            print(f"事件更新成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "delete-event":
            result = client.delete_calendar_event(args.calendar_id, args.event_id)
            print(f"事件删除成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "create-chat":
            member_ids = args.members.split(",")
            result = client.create_chat(args.name, member_ids, args.description)
            print(f"群聊创建成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "add-chat-members":
            member_ids = args.members.split(",")
            result = client.add_chat_members(args.chat_id, member_ids)
            print(f"成员添加成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "remove-chat-members":
            member_ids = args.members.split(",")
            result = client.remove_chat_members(args.chat_id, member_ids)
            print(f"成员移除成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "get-chat-info":
            result = client.get_chat_info(args.chat_id)
            print(f"群聊信息: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "update-chat":
            result = client.update_chat(args.chat_id, name=args.name, description=args.description)
            print(f"群聊信息修改成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-chat-members":
            result = client.list_chat_members(args.chat_id, args.page_size, getattr(args, "page_token", None))
            print(f"群聊成员: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "dissolve-chat":
            result = client.dissolve_chat(args.chat_id)
            print(f"群聊已解散: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "upload-file":
            result = client.upload_file(args.file_path, args.parent_node, args.file_name)
            print(f"文件上传成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "get-user":
            result = client.get_user_info(args.email)
            print(f"用户信息: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "get-user-detail":
            result = client.get_user_by_id(args.user_id, args.user_id_type)
            print(f"用户详情: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-departments":
            result = client.list_departments(args.parent_id)
            print(f"部门列表: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-department-users":
            result = client.list_department_users(args.department_id)
            print(f"部门成员: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "get-tenant-info":
            result = client.get_tenant_info()
            print(f"企业信息: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-wiki-spaces":
            result = client.list_wiki_spaces(args.page_size, getattr(args, "page_token", None))
            print(f"知识库空间: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "list-wiki-nodes":
            result = client.list_wiki_nodes(args.space_id, getattr(args, "parent_node_token", None), args.page_size, getattr(args, "page_token", None))
            print(f"知识库节点: {json.dumps(result, ensure_ascii=False, indent=2)}")
        elif args.command == "read-wiki-node":
            result = client.read_wiki_node_content(args.node_token)
            print(f"文章内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
