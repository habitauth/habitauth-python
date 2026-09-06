# Habit Auth Python Client SDK & Complete Example Solutions

Official Python client integration library and full source code examples (Console application, Tkinter Dark GUI) for **Habit Auth** enterprise software licensing and hardware-lock security.

[![Website](https://img.shields.io/badge/Official_Website-habitauth.com-6366f1.svg)](https://habitauth.com)
[![Documentation](https://img.shields.io/badge/Documentation-habitauth.com/docs-10b981.svg)](https://habitauth.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Solution Structure

```
habitauth-python/
├── .gitignore
├── README.md
├── requirements.txt
├── habitauth/                           # Core SDK package
│   ├── __init__.py
│   └── habitauth.py                     # HabitAuth Client Implementation
└── examples/
    ├── console_example.py               # Interactive CLI Application
    └── gui_example.py                   # Complete Modern Tkinter GUI (Login & Dashboard)
```

---

## Features

- **Cross-Platform Compatibility:** Works on Windows, Linux, and macOS.
- **Hardware-ID (HWID) Locking:** Automatically generates SHA-256 machine hardware fingerprints.
- **Modern Dark GUI Included:** Pre-built Tkinter Login window and Main Dashboard window (`examples/gui_example.py`).
- **Remote Killswitch & Heartbeat:** Protects your Python scripts and tools from unauthorized distribution.

---

## Quick Setup

\`\`\`bash
git clone https://github.com/habitauth/habitauth-python.git
cd habitauth-python
pip install -r requirements.txt
python examples/gui_example.py
\`\`\`

---

(C) 2026 Habit Auth. All rights reserved.
