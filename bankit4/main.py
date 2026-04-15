"""
main.py — BankIT IT Support Ticketing System v4
Run:  python main.py
Login: PR12345 / 246810  (Project Manager)
"""
import tkinter as tk
from gui.login_window import LoginWindow

def main():
    root = tk.Tk(); root.withdraw()
    LoginWindow(root); root.mainloop()

if __name__ == "__main__":
    main()
