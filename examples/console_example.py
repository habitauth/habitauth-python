import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from habitauth import HabitAuth

APP_ID = "app_c0049143710d4e5c"
APP_SECRET = "sec_0000000000000000"
VERSION = "1.0.0"

def main():
    print("=====================================================")
    print("   HABIT AUTH - PYTHON CLIENT EXAMPLE")
    print("   Hardware-Locked Software Protection")
    print("=====================================================\n")

    auth = HabitAuth(APP_ID, APP_SECRET, VERSION)
    print("[*] Connecting to Habit Auth...")
    init_res = auth.initialize()

    if not init_res.success:
        print(f"[-] Initialization error: {init_res.message}")
        return

    print(f"[+] Connected successfully.")
    print(f"[*] Machine HWID: {auth.get_hwid()}\n")

    while True:
        print("---------------------------------------------")
        print("[1] Login (Username & Password)")
        print("[2] Register (Username, Password & License)")
        print("[3] Key Only Login")
        print("[4] Reset HWID")
        print("[5] Exit")
        print("---------------------------------------------")
        choice = input("Select an option [1-5]: ").strip()

        if choice == "1":
            user = input("Username: ").strip()
            pw = input("Password: ")
            print("[*] Authenticating...")
            res = auth.login(user, pw)
            if res.success:
                print(f"[+] Login successful! Welcome {auth.user.username}")
                print(f"    Subscription: {auth.user.subscription}")
                print(f"    Expires: {'Lifetime' if auth.user.expires_at == 0 else auth.user.expires_at}")
                break
            else:
                print(f"[-] Error: {res.message}")

        elif choice == "2":
            user = input("Username: ").strip()
            pw = input("Password: ")
            key = input("License Key: ").strip()
            print("[*] Registering...")
            res = auth.register(user, pw, key)
            if res.success:
                print("[+] Account registered successfully! You can now log in.")
            else:
                print(f"[-] Error: {res.message}")

        elif choice == "3":
            key = input("License Key: ").strip()
            print("[*] Verifying license...")
            res = auth.license_login(key)
            if res.success:
                print("[+] License verified successfully!")
                break
            else:
                print(f"[-] Error: {res.message}")

        elif choice == "4":
            user = input("Username: ").strip()
            pw = input("Password: ")
            print("[*] Resetting HWID...")
            res = auth.reset_hwid(user, pw)
            if res.success:
                print("[+] HWID reset successfully! You can now log in from this PC.")
            else:
                print(f"[-] Error: {res.message}")

        elif choice == "5":
            return

    print("\n[+] Protected payload unlocked! Starting main application loop...")

if __name__ == "__main__":
    main()
