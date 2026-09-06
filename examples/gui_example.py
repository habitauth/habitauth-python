import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from habitauth import HabitAuth

APP_ID = "app_c0049143710d4e5c"
APP_SECRET = "sec_0000000000000000"
VERSION = "1.0.0"

auth = HabitAuth(APP_ID, APP_SECRET, VERSION)

class HabitAuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Auth - Python GUI Example")
        self.geometry("420x520")
        self.configure(bg="#111827")
        self.resizable(False, False)

        # Title
        tk.Label(self, text="Habit Auth", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#111827").place(x=30, y=20)
        tk.Label(self, text="Hardware-Locked Client", font=("Segoe UI", 9), fg="#9ca3af", bg="#111827").place(x=32, y=55)

        # Username
        tk.Label(self, text="Username", font=("Segoe UI", 9), fg="#d1d5db", bg="#111827").place(x=32, y=95)
        self.txt_username = tk.Entry(self, font=("Segoe UI", 10), bg="#1f2937", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.txt_username.place(x=35, y=120, width=350, height=32)

        # Password
        tk.Label(self, text="Password", font=("Segoe UI", 9), fg="#d1d5db", bg="#111827").place(x=32, y=165)
        self.txt_password = tk.Entry(self, font=("Segoe UI", 10), show="*", bg="#1f2937", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.txt_password.place(x=35, y=190, width=350, height=32)

        # License
        tk.Label(self, text="License Key", font=("Segoe UI", 9), fg="#d1d5db", bg="#111827").place(x=32, y=235)
        self.txt_license = tk.Entry(self, font=("Segoe UI", 10), bg="#1f2937", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.txt_license.place(x=35, y=260, width=350, height=32)

        # Buttons
        tk.Button(self, text="Login", font=("Segoe UI", 10, "bold"), bg="#6366f1", fg="#ffffff", relief="flat", activebackground="#4f46e5", command=self.do_login).place(x=35, y=310, width=165, height=38)
        tk.Button(self, text="Register", font=("Segoe UI", 10, "bold"), bg="#374151", fg="#ffffff", relief="flat", activebackground="#4b5563", command=self.do_register).place(x=220, y=310, width=165, height=38)
        tk.Button(self, text="Key Only Login", font=("Segoe UI", 9), bg="#1f2937", fg="#d1d5db", relief="flat", activebackground="#374151", command=self.do_key_login).place(x=35, y=360, width=165, height=34)
        tk.Button(self, text="Reset HWID", font=("Segoe UI", 9), bg="#1f2937", fg="#d1d5db", relief="flat", activebackground="#374151", command=self.do_reset_hwid).place(x=220, y=360, width=165, height=34)

        # Status
        self.lbl_status = tk.Label(self, text="Connecting to Habit Auth...", font=("Segoe UI", 9), fg="#9ca3af", bg="#111827", wraplength=350, justify="left")
        self.lbl_status.place(x=35, y=410)

        # HWID
        self.lbl_hwid = tk.Label(self, text=f"HWID: {auth.get_hwid()[:32]}...", font=("Segoe UI", 7), fg="#6b7280", bg="#111827")
        self.lbl_hwid.place(x=35, y=470)

        self.after(200, self.init_auth)

    def init_auth(self):
        res = auth.initialize()
        if res.success:
            self.lbl_status.config(text="Ready. Connected to Habit Auth.", fg="#10b981")
        else:
            self.lbl_status.config(text=f"Initialization error: {res.message}", fg="#ef4444")

    def do_login(self):
        u = self.txt_username.get().strip()
        p = self.txt_password.get()
        if not u or not p:
            self.lbl_status.config(text="Enter username and password.", fg="#ef4444")
            return

        self.lbl_status.config(text="Authenticating...", fg="#6366f1")
        res = auth.login(u, p)
        if res.success:
            self.open_dashboard()
        else:
            self.lbl_status.config(text=res.message, fg="#ef4444")

    def do_register(self):
        u = self.txt_username.get().strip()
        p = self.txt_password.get()
        k = self.txt_license.get().strip()
        if not u or not p or not k:
            self.lbl_status.config(text="Please fill username, password, and license key.", fg="#ef4444")
            return

        self.lbl_status.config(text="Registering...", fg="#6366f1")
        res = auth.register(u, p, k)
        if res.success:
            self.lbl_status.config(text="Account created successfully! You can now log in.", fg="#10b981")
        else:
            self.lbl_status.config(text=res.message, fg="#ef4444")

    def do_key_login(self):
        k = self.txt_license.get().strip()
        if not k:
            self.lbl_status.config(text="Enter license key.", fg="#ef4444")
            return

        self.lbl_status.config(text="Verifying license...", fg="#6366f1")
        res = auth.license_login(k)
        if res.success:
            self.open_dashboard()
        else:
            self.lbl_status.config(text=res.message, fg="#ef4444")

    def do_reset_hwid(self):
        u = self.txt_username.get().strip()
        p = self.txt_password.get()
        if not u or not p:
            self.lbl_status.config(text="Enter username and password to reset HWID.", fg="#ef4444")
            return

        self.lbl_status.config(text="Resetting HWID...", fg="#6366f1")
        res = auth.reset_hwid(u, p)
        if res.success:
            self.lbl_status.config(text="HWID reset successfully! You can now log in.", fg="#10b981")
        else:
            self.lbl_status.config(text=res.message, fg="#ef4444")

    def open_dashboard(self):
        self.withdraw()
        dash = tk.Toplevel(self)
        dash.title("Habit Auth - Main Dashboard")
        dash.geometry("500x380")
        dash.configure(bg="#111827")
        dash.resizable(False, False)

        tk.Label(dash, text="Dashboard", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#111827").place(x=30, y=25)
        tk.Label(dash, text=f"Welcome back, {auth.user.username}!", font=("Segoe UI", 11), fg="#10b981", bg="#111827").place(x=32, y=65)

        card = tk.Frame(dash, bg="#1f2937")
        card.place(x=35, y=105, width=430, height=160)

        tk.Label(card, text=f"Plan: {auth.user.subscription.upper()}", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#1f2937").place(x=20, y=20)
        exp_text = "Expires: Lifetime" if auth.user.expires_at == 0 else f"Expires: {auth.user.expires_at}"
        tk.Label(card, text=exp_text, font=("Segoe UI", 9), fg="#d1d5db", bg="#1f2937").place(x=20, y=55)
        tk.Label(card, text=f"HWID: {auth.user.hwid[:35]}...", font=("Segoe UI", 8), fg="#9ca3af", bg="#1f2937").place(x=20, y=90)
        tk.Label(card, text=f"App Version: {auth.app.version}", font=("Segoe UI", 8), fg="#9ca3af", bg="#1f2937").place(x=20, y=120)

        def launch_feature():
            messagebox.showinfo("Success", "Protected application feature launched successfully!")

        tk.Button(dash, text="Launch Protected Feature", font=("Segoe UI", 10, "bold"), bg="#6366f1", fg="#ffffff", relief="flat", command=launch_feature).place(x=35, y=290, width=200, height=42)
        tk.Button(dash, text="Logout", font=("Segoe UI", 10, "bold"), bg="#374151", fg="#ffffff", relief="flat", command=self.destroy).place(x=265, y=290, width=200, height=42)

if __name__ == "__main__":
    app = HabitAuthApp()
    app.mainloop()
