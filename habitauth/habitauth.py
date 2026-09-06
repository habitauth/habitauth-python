import requests
import hashlib
import platform
import uuid
from typing import Optional, Dict, Any

class UserData:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        data = data or {}
        self.username: str = data.get("username", "")
        self.subscription: str = data.get("subscription", "free")
        self.expires_at: int = data.get("expires_at", 0)
        self.hwid: str = data.get("hwid", "")
        self.token: str = data.get("token", "")

class AppData:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        data = data or {}
        self.name: str = data.get("app_name", "")
        self.version: str = data.get("version", "1.0.0")
        self.latest_version: str = data.get("latest_version", "1.0.0")
        self.download_url: str = data.get("download_url", "")

class HabitAuthResponse:
    def __init__(self, success: bool, message: str, code: str = "", raw: Optional[Dict[str, Any]] = None):
        self.success = success
        self.message = message
        self.code = code
        self.raw = raw or {}

class HabitAuth:
    def __init__(self, app_id: str, app_secret: str, version: str = "1.0.0", base_url: str = "https://habitauth.com/api/v1"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.version = version
        self.base_url = base_url.rstrip("/")
        self.user = UserData()
        self.app = AppData()
        self.is_initialized = False
        self._session = requests.Session()

    def get_hwid(self) -> str:
        try:
            raw = f"{platform.node()}-{platform.machine()}-{platform.processor()}-{platform.system()}"
            return hashlib.sha256(raw.encode()).hexdigest()
        except Exception:
            return "hwid-" + uuid.uuid4().hex[:16]

    def _post(self, endpoint: str, data: dict) -> HabitAuthResponse:
        try:
            res = self._session.post(f"{self.base_url}{endpoint}", json=data, timeout=15)
            json_data = res.json()
            success = json_data.get("success", False)
            message = json_data.get("message", "")
            code = json_data.get("code", "")

            if success:
                if "token" in json_data:
                    self.user.token = json_data["token"]
                if "user" in json_data:
                    self.user = UserData(json_data["user"])
                if "app" in json_data:
                    self.app = AppData(json_data["app"])

            return HabitAuthResponse(success, message, code, json_data)
        except Exception as e:
            return HabitAuthResponse(False, str(e), "NETWORK_ERROR")

    def initialize(self) -> HabitAuthResponse:
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "version": self.version
        }
        res = self._post("/client/init", payload)
        if res.success:
            self.is_initialized = True
        return res

    def login(self, username: str, password: str) -> HabitAuthResponse:
        payload = {
            "app_id": self.app_id,
            "username": username.strip(),
            "password": password,
            "hwid": self.get_hwid(),
            "sid": f"SID-{platform.node()}"
        }
        return self._post("/client/login", payload)

    def register(self, username: str, password: str, license_key: str) -> HabitAuthResponse:
        payload = {
            "app_id": self.app_id,
            "username": username.strip(),
            "password": password,
            "license_key": license_key.strip(),
            "hwid": self.get_hwid(),
            "sid": f"SID-{platform.node()}"
        }
        return self._post("/client/register", payload)

    def license_login(self, license_key: str) -> HabitAuthResponse:
        payload = {
            "app_id": self.app_id,
            "license_key": license_key.strip(),
            "hwid": self.get_hwid(),
            "sid": f"SID-{platform.node()}"
        }
        return self._post("/client/license-login", payload)

    def reset_hwid(self, username: str, password: str) -> HabitAuthResponse:
        payload = {
            "app_id": self.app_id,
            "username": username.strip(),
            "password": password
        }
        return self._post("/client/reset-hwid", payload)

    def heartbeat(self) -> bool:
        if not self.user.token:
            return False
        payload = {
            "app_id": self.app_id,
            "token": self.user.token,
            "hwid": self.get_hwid()
        }
        return self._post("/client/heartbeat", payload).success
