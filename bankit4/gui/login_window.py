"""gui/login_window.py"""
import tkinter as tk
from tkinter import messagebox
from backend import data_manager as dm
from gui.utils import center,FONT,FONT_B,BG,HEADER_BG,HEADER_FG,LABEL_FG,ENTRY_BG,btn,first_login_dialog


class LoginWindow:
    def __init__(self, root):
        self.root = root; dm.init_default_manager()
        self.win = tk.Toplevel(root); self.win.title("BankIT — IT Support Ticketing System")
        self.win.configure(bg=BG); self.win.resizable(False,False)
        center(self.win,440,460); self.win.protocol("WM_DELETE_WINDOW",lambda:root.destroy())
        self._build()

    def _build(self):
        h=tk.Frame(self.win,bg=HEADER_BG); h.pack(fill="x")
        tk.Label(h,text="🏦  BankIT",bg=HEADER_BG,fg=HEADER_FG,font=("Segoe UI",24,"bold"),pady=10).pack()
        tk.Label(h,text="IT Support Ticketing System",bg=HEADER_BG,fg="#B0C4DE",font=("Segoe UI",11)).pack(pady=(0,12))

        frm=tk.Frame(self.win,bg=BG); frm.pack(pady=28)
        tk.Label(frm,text="Staff ID",bg=BG,fg=LABEL_FG,font=FONT_B).grid(row=0,column=0,sticky="w",pady=4)
        self.id_var=tk.StringVar()
        id_e=tk.Entry(frm,textvariable=self.id_var,width=30,font=FONT,relief="solid",bg=ENTRY_BG)
        id_e.grid(row=1,column=0,pady=(0,16)); id_e.focus_set()
        tk.Label(frm,text="Password / One-Time Password",bg=BG,fg=LABEL_FG,font=FONT_B).grid(row=2,column=0,sticky="w",pady=4)
        self.pw_var=tk.StringVar()
        pw_e=tk.Entry(frm,textvariable=self.pw_var,width=30,font=FONT,show="*",relief="solid",bg=ENTRY_BG)
        pw_e.grid(row=3,column=0,pady=(0,22)); pw_e.bind("<Return>",lambda e:self._login())
        btn(frm,"Login →",self._login,26).grid(row=4,column=0)
        tk.Label(self.win,text="Default Manager  →  PR12345 / 246810",bg=BG,fg="#888",font=("Segoe UI",9)).pack(pady=6)

    def _login(self):
        uid=self.id_var.get().strip(); pw=self.pw_var.get().strip()
        if not uid or not pw:
            messagebox.showerror("Error","Please enter ID and Password.",parent=self.win); return
        role,record=dm.authenticate(uid,pw)
        if role is None:
            messagebox.showerror("Login Failed","Invalid Staff ID or Password.\n\nFirst-time users: use the One-Time Password from your manager.",parent=self.win); return
        if role.startswith("otp_"):
            actual=role[4:]
            def do_set(new_pw):
                if "user"==actual: dm.update_user_password(record["id"],new_pw)
                else:              dm.update_engineer_password(record["id"],new_pw)
                dm.remove_otp(record["id"]); record["password"]=new_pw; self._open(actual,record)
            first_login_dialog(self.win,do_set); return
        self._open(role,record)

    def _open(self,role,record):
        self.win.withdraw()
        def on_logout(): self.id_var.set(""); self.pw_var.set(""); self.win.deiconify()
        if role=="manager":
            from gui.manager_window import ManagerWindow; ManagerWindow(self.root,record,on_logout)
        elif role=="user":
            from gui.user_window import UserWindow; UserWindow(self.root,record,on_logout)
        elif role=="l1_engineer":
            from gui.engineer_window import EngineerWindow; EngineerWindow(self.root,record,1,on_logout)
        elif role=="l2_engineer":
            from gui.engineer_window import EngineerWindow; EngineerWindow(self.root,record,2,on_logout)
