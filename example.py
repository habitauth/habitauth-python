# app_gui.py - Python Tkinter UI Form with HabitAuth
import tkinter as tk
from tkinter import messagebox
from habit_auth import HabitAuth

# 1. Initialize with dashboard credentials (with Ed25519 public key verification)
auth = HabitAuth("TARGET_APP_NAME", "TARGET_APP_ID", app_secret="TARGET_APP_SECRET", public_key="TARGET_PUBLIC_KEY", version="1.0.0")

# 2. Connect & Handshake on Startup
ok, msg = auth.init()
if not ok:
    print(f"[!] Init error: {msg}")
    exit(1)

# 3. Create GUI Window
root = tk.Tk()
root.title("HabitAuth Client")
root.geometry("360x320")

# TextBoxes for User Input
tk.Label(root, text="Username (txtUsername):").pack(pady=(10, 0))
txt_username = tk.Entry(root, width=32)
txt_username.pack()

tk.Label(root, text="Password (txtPassword):").pack(pady=(5, 0))
txt_password = tk.Entry(root, width=32, show="*")
txt_password.pack()

tk.Label(root, text="License Key (txtLicense):").pack(pady=(5, 0))
txt_license = tk.Entry(root, width=32)
txt_license.pack()

# Button Click Handlers
def btn_login_click():
    ok, msg = auth.login(txt_username.get(), txt_password.get())
    if ok:
        messagebox.showinfo("Success", f"Welcome {auth.user['username']}!\nExpires: {auth.user.get('expires_at')}")
        auth.start_heartbeat(30)
    else:
        messagebox.showerror("Error", f"Login Failed: {msg}")

def btn_register_click():
    ok, msg = auth.register(txt_username.get(), txt_password.get(), txt_license.get())
    if ok:
        messagebox.showinfo("Success", "Registered successfully! You can now log in.")
    else:
        messagebox.showerror("Error", f"Registration Failed: {msg}")

def btn_license_only_click():
    ok, msg = auth.license(txt_license.get())
    if ok:
        messagebox.showinfo("Success", f"License Validated!\nExpires: {auth.user.get('expires_at')}")
        auth.start_heartbeat(30)
    else:
        messagebox.showerror("Error", f"Invalid License: {msg}")

# UI Action Buttons
tk.Button(root, text="Login (btnLogin)", command=btn_login_click, width=28, bg="#9333ea", fg="white").pack(pady=8)
tk.Button(root, text="Register (btnRegister)", command=btn_register_click, width=28).pack(pady=4)
tk.Button(root, text="License Only (btnLicense)", command=btn_license_only_click, width=28).pack(pady=4)

root.mainloop()