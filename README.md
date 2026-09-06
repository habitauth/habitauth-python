# Habit Auth Python Client SDK

Official cross-platform Python client library for Habit Auth enterprise software protection, licensing, and anti-tamper telemetry.

[![Website](https://img.shields.io/badge/Official_Website-habitauth.com-0284c7?style=flat-square)](https://habitauth.com)
[![Documentation](https://img.shields.io/badge/Developer_Docs-habitauth.com%2Fdocs-2563eb?style=flat-square)](https://habitauth.com/docs)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

---

## Features

- **Cross-Platform:** Seamlessly runs on Windows, Linux, and macOS.
- **Hardware Profile Binding:** Deep hardware profiling via WMI and machine UUID.
- **HMAC-SHA256 Response Integrity:** Cryptographic verification with replay prevention.
- **Background Telemetry:** Dedicated daemon thread for 30-second heartbeats with remote process termination.

---

## Installation

```bash
pip install requests
```

---

## Quick Integration

```python
from habit_auth import HabitAuthApp

# 1. Initialize HabitAuth client
auth = HabitAuthApp(
    name="YOUR_APP_NAME",
    ownerid="YOUR_APP_ID",
    secret="YOUR_APP_SECRET",
    version="1.0"
)

# 2. Handshake with server
if not auth.init():
    print("Init failed:", auth.response.message)
    exit(1)

# 3. User Login
if auth.login("demo_user", "password123"):
    print(f"Logged in successfully. Welcome {auth.user.username}")
    print(f"License Expiration: {auth.user.expires_at}")

    # 4. Start background telemetry heartbeat
    auth.start_heartbeat(30)
else:
    print("Login failed:", auth.response.message)
```

---

## Documentation & Support

- **Full Documentation:** [https://habitauth.com/docs](https://habitauth.com/docs)
- **Official Portal:** [https://habitauth.com](https://habitauth.com)
- **YouTube:** [https://youtube.com/@habitauth](https://youtube.com/@habitauth)
- **Technical Support:** support@habitauth.com
