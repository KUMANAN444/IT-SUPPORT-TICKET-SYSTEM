"""gui/user_window.py"""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from backend import data_manager as dm
from gui.utils import (BG,LABEL_FG,FONT,FONT_B,FONT_TITLE,ENTRY_BG,RED_BG,GREEN_BG,ORANGE_BG,
                       center,toplevel,header,btn,nav_btn,table,pw_change_dialog,
                       ticket_detail,notification_popup,lbl,ent,scroll_frame)

TICKET_TREE={
    "Hardware Related":{
        "Corp Mobile":{
            "Corp phone damaged":  {"sub_issues":["Display broken","Charging port broken"],"fields":["description"]},
            "Phone lost":          {"fields":["where_lost","line_manager_id","police_complaint"]},
            "Apply for new phone": {"fields":["reason","old_serial","line_manager_id"]},
            "Return phone":        {"fields":["reason","return_date"]},
        },
        "Corp Laptop/Desktop/Workstation":{
            "Corp PC damaged":   {"sub_issues":["Cooling Fan","Display","Keyboard/Mousepad","Charging/Other Port","Camera"],"fields":["description"]},
            "Apply for new PC":  {"fields":["reason","old_serial","line_manager_id"]},
            "Lost of PC":        {"fields":["where_lost","line_manager_id","police_complaint"]},
            "Return my PC":      {"fields":["reason","return_date"]},
        },
    },
    "Software Related":{
        "MS Application":{"Outlook related":{"fields":["description"]},"Teams related":{"fields":["description"]},"Word/Excel/PowerPoint related":{"fields":["description"]},"OneDrive related":{"fields":["description"]}},
        "Bloomberg Application":{"App is hanging/not opening":{"fields":["description"]},"Failed to login":{"fields":["description"]},"Other issues":{"fields":["description"]}},
        "Printer issue":{"Not connecting with printer":{"fields":["description"]},"Request for printer access":{"fields":["description"]},"Other printer issues":{"fields":["description"]}},
        "Bluetooth issue":{"Bluetooth connectivity issue":{"fields":["description"]}},
    },
    "Account/Network Related":{
        "Account related issue":{"Forgot password":{"fields":["description"]},"Reset locked account":{"fields":["description"]},"Login issue":{"fields":["description"]}},
        "Network related issue":{"Cannot connect to office network":{"fields":["description"]},"VPN related issue":{"fields":["description"]},"LAN network not working":{"fields":["description"]}},
    },
}
FIELD_LBL={"description":"Description:","where_lost":"Where was the device lost?",
            "line_manager_id":"Line Manager Staff ID:","police_complaint":"Police complaint filed?",
            "reason":"Reason:","old_serial":"Old device serial number:","return_date":"Return date (YYYY-MM-DD):"}


class UserWindow:
    def __init__(self,root,user,on_logout):
        self.root=root; self.user=user; self.on_logout=on_logout
        self.win=tk.Toplevel(root); self.win.title(f"BankIT — User: {user['id']}")
        self.win.configure(bg=BG); self.win.protocol("WM_DELETE_WINDOW",self._logout)
        self.win.geometry("980x680"); center(self.win,980,680); self._build()

    def _build(self):
        name=f"{self.user.get('first_name','')} {self.user.get('last_name','')}"
        header(self.win,f"Welcome, {name}  |  ID: {self.user['id']}")
        nav=tk.Frame(self.win,bg="#1A3C5E",pady=4); nav.pack(fill="x")
        for text,cmd in [("➕ Create Ticket",self._create),("📋 My Tickets",self._tickets),
                          ("📜 History",self._tickets),("🔔 Notifications",self._notifs),
                          ("🔑 Change Password",self._pw),("🚪 Logout",self._logout)]:
            nav_btn(nav,text,cmd).pack(side="left",padx=5,pady=2)
        self.content=tk.Frame(self.win,bg=BG); self.content.pack(fill="both",expand=True,padx=10,pady=10)
        self._tickets()

    def _clear(self):
        for w in self.content.winfo_children(): w.destroy()

    def _tickets(self):
        self._clear()
        tk.Label(self.content,text="My Tickets",bg=BG,fg=LABEL_FG,font=FONT_TITLE).pack(anchor="w",pady=(0,6))
        tickets=dm.get_tickets_by_user(self.user["id"])
        rows=[(t["id"],t.get("category",""),t.get("subcategory",""),
               t.get("status","").upper(),t.get("assigned_to_name",""),t.get("created_at","")[:16])
              for t in tickets.values()]
        frm,tree=table(self.content,("Ticket ID","Category","Subcategory","Status","Assigned To","Created"),
                       rows,height=18,on_dbl=lambda tv:self._open(tv,tickets))
        frm.pack(fill="both",expand=True)
        tk.Label(self.content,text="Double-click a row to view details.",bg=BG,fg="#888",font=("Segoe UI",9)).pack(anchor="w")

    def _open(self,tree,tdict):
        sel=tree.selection()
        if not sel: return
        t=tdict.get(str(tree.item(sel[0])["values"][0]))
        if t: ticket_detail(self.win,t,can_act=False)

    def _create(self): TicketWizard(self.win,self.user,on_done=self._tickets)

    def _notifs(self):
        notification_popup(self.win,dm.get_notifications(self.user["id"]),
                           on_clear=lambda:(dm.mark_notifications_read(self.user["id"]),self.win.focus()))

    def _pw(self):
        pw_change_dialog(self.win,verify_fn=lambda old:self.user.get("password")==old,
                         update_fn=lambda new:(dm.update_user_password(self.user["id"],new),self.user.update({"password":new})))

    def _logout(self): self.win.destroy(); self.on_logout()


class TicketWizard:
    def __init__(self,parent,user,on_done=None):
        self.parent=parent; self.user=user; self.on_done=on_done; self.state={}
        self.win=tk.Toplevel(parent); self.win.title("Create New Ticket"); self.win.configure(bg=BG)
        self.win.resizable(True,True); center(self.win,560,540); self.win.grab_set()
        self._hdr=tk.Label(self.win,text="Step 1 of 4 — Select Category",bg="#1A3C5E",fg="white",font=FONT_B,pady=8)
        self._hdr.pack(fill="x")
        self._outer,self._inner=scroll_frame(self.win); self._outer.pack(fill="both",expand=True)
        self._nav=tk.Frame(self.win,bg=BG,pady=8); self._nav.pack(fill="x")
        self._step1()

    def _sh(self,t): self._hdr.config(text=t)
    def _ci(self):
        for w in self._inner.winfo_children(): w.destroy()
    def _sn(self,back=None,next_cmd=None,next_lbl="Next →",cancel=True):
        for w in self._nav.winfo_children(): w.destroy()
        if back: btn(self._nav,"← Back",back,10).pack(side="left",padx=8)
        if next_cmd: btn(self._nav,next_lbl,next_cmd,16).pack(side="left",padx=8)
        if cancel: btn(self._nav,"✖ Cancel",self.win.destroy,10,"#C62828","white").pack(side="right",padx=8)

    def _step1(self):
        self._sh("Step 1 of 4 — Select Category"); self._ci()
        tk.Label(self._inner,text="Select the issue category:",bg=BG,fg=LABEL_FG,font=FONT_B).pack(anchor="w",padx=16,pady=(14,6))
        self._cv=tk.StringVar()
        for cat in TICKET_TREE:
            tk.Radiobutton(self._inner,text=cat,variable=self._cv,value=cat,bg=BG,fg="#333",font=FONT,activebackground=BG,selectcolor=BG).pack(anchor="w",padx=36,pady=5)
        self._sn(next_cmd=self._g2)

    def _g2(self):
        if not self._cv.get(): messagebox.showerror("Error","Please select a category.",parent=self.win); return
        self.state["category"]=self._cv.get(); self._step2()

    def _step2(self):
        self._sh("Step 2 of 4 — Select Subcategory"); self._ci()
        cat=self.state["category"]
        tk.Label(self._inner,text=f"Category: {cat}",bg=BG,fg=LABEL_FG,font=FONT_B).pack(anchor="w",padx=16,pady=(12,4))
        self._sv=tk.StringVar()
        for sub in TICKET_TREE[cat]:
            tk.Radiobutton(self._inner,text=sub,variable=self._sv,value=sub,bg=BG,fg="#333",font=FONT,activebackground=BG,selectcolor=BG).pack(anchor="w",padx=36,pady=5)
        self._sn(back=self._step1,next_cmd=self._g3)

    def _g3(self):
        if not self._sv.get(): messagebox.showerror("Error","Please select a subcategory.",parent=self.win); return
        self.state["subcategory"]=self._sv.get(); self._step3()

    def _step3(self):
        self._sh("Step 3 of 4 — Select Issue Type"); self._ci()
        cat,sub=self.state["category"],self.state["subcategory"]
        tk.Label(self._inner,text=f"{cat}  ›  {sub}",bg=BG,fg=LABEL_FG,font=FONT_B).pack(anchor="w",padx=16,pady=(12,4))
        self._iv=tk.StringVar()
        for issue in TICKET_TREE[cat][sub]:
            tk.Radiobutton(self._inner,text=issue,variable=self._iv,value=issue,bg=BG,fg="#333",font=FONT,activebackground=BG,selectcolor=BG).pack(anchor="w",padx=36,pady=5)
        self._sn(back=self._step2,next_cmd=self._g4)

    def _g4(self):
        if not self._iv.get(): messagebox.showerror("Error","Please select an issue type.",parent=self.win); return
        self.state["issue_type"]=self._iv.get(); self._step4()

    def _step4(self):
        self._sh("Step 4 of 4 — Provide Details"); self._ci()
        cat,sub,issue=self.state["category"],self.state["subcategory"],self.state["issue_type"]
        info=TICKET_TREE[cat][sub][issue]; sub_issues=info.get("sub_issues",[]); fields=info.get("fields",["description"])
        tk.Label(self._inner,text=f"{cat}  ›  {sub}  ›  {issue}",bg=BG,fg=LABEL_FG,font=FONT_B,wraplength=500,justify="left").grid(row=0,column=0,columnspan=2,sticky="w",padx=14,pady=(12,8))
        self._fw={}; row=1
        if sub_issues:
            tk.Label(self._inner,text="Sub-Issue:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="e",width=22).grid(row=row,column=0,sticky="e",padx=8,pady=6)
            sv=tk.StringVar()
            ttk.Combobox(self._inner,textvariable=sv,values=sub_issues,width=32,state="readonly",font=FONT).grid(row=row,column=1,sticky="w",padx=8,pady=6)
            self._fw["sub_issue"]=sv; row+=1
        for field in fields:
            lbl_text=FIELD_LBL.get(field,field.replace("_"," ").title()+":")
            tk.Label(self._inner,text=lbl_text,bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne",width=22).grid(row=row,column=0,sticky="ne",padx=8,pady=6)
            if field=="police_complaint":
                pv=tk.StringVar(value="No"); ttk.Combobox(self._inner,textvariable=pv,values=["Yes","No"],width=10,state="readonly",font=FONT).grid(row=row,column=1,sticky="w",padx=8,pady=6); self._fw[field]=pv
            elif field in("description","reason"):
                ta=tk.Text(self._inner,width=34,height=5,font=FONT,relief="solid",bd=1); ta.grid(row=row,column=1,sticky="w",padx=8,pady=6); self._fw[field]=ta
            elif field=="return_date":
                df=tk.Frame(self._inner,bg=BG); df.grid(row=row,column=1,sticky="w",padx=8,pady=6)
                now=datetime.now(); yv=tk.StringVar(value=str(now.year)); mv=tk.StringVar(value=f"{now.month:02d}"); dv=tk.StringVar(value=f"{now.day:02d}")
                tk.Spinbox(df,from_=2024,to=2030,textvariable=yv,width=5,font=FONT).pack(side="left")
                tk.Label(df,text="-",bg=BG,font=FONT).pack(side="left")
                tk.Spinbox(df,from_=1,to=12,textvariable=mv,format="%02.0f",width=3,font=FONT).pack(side="left")
                tk.Label(df,text="-",bg=BG,font=FONT).pack(side="left")
                tk.Spinbox(df,from_=1,to=31,textvariable=dv,format="%02.0f",width=3,font=FONT).pack(side="left")
                self._fw[field]=(yv,mv,dv)
            else:
                e=tk.Entry(self._inner,width=34,font=FONT,relief="solid",bg=ENTRY_BG); e.grid(row=row,column=1,sticky="w",padx=8,pady=6); self._fw[field]=e
            row+=1
        self._sn(back=self._step3,next_cmd=self._submit,next_lbl="✔ Submit Ticket")

    def _submit(self):
        cat,sub,issue=self.state["category"],self.state["subcategory"],self.state["issue_type"]
        info=TICKET_TREE[cat][sub][issue]; fields=info.get("fields",["description"]); sub_issues=info.get("sub_issues",[])
        collected={}
        if sub_issues:
            sv=self._fw.get("sub_issue")
            if sv and not sv.get(): messagebox.showerror("Error","Please select a sub-issue.",parent=self.win); return
            collected["sub_issue"]=sv.get() if sv else ""
        else: collected["sub_issue"]=""
        for f in fields:
            w=self._fw.get(f)
            if w is None: continue
            if isinstance(w,tuple): val=f"{w[0].get()}-{w[1].get()}-{w[2].get()}"
            elif isinstance(w,tk.Text): val=w.get("1.0","end").strip()
            elif isinstance(w,tk.StringVar): val=w.get().strip()
            else: val=w.get().strip()
            if not val and f!="police_complaint": messagebox.showerror("Error",f"Please fill in: {FIELD_LBL.get(f,f)}",parent=self.win); return
            collected[f]=val
        desc=collected.get("description") or collected.get("reason") or "\n".join(f"{FIELD_LBL.get(k,k).rstrip(':')} : {v}" for k,v in collected.items())
        eng=dm.get_available_engineer(1)
        if not eng: messagebox.showerror("No Engineers","No L1 engineers available.\nAsk the manager to create one first.",parent=self.win); return
        tid=dm.create_ticket({"user_id":self.user["id"],"user_name":f"{self.user.get('first_name','')} {self.user.get('last_name','')}","category":cat,"subcategory":sub,"issue_type":issue,"sub_issue":collected.get("sub_issue",""),"description":desc,"assigned_to":eng["id"],"assigned_to_name":f"{eng.get('first_name','')} {eng.get('last_name','')}","assigned_level":1})
        now=datetime.now(); eng_name=f"{eng.get('first_name','')} {eng.get('last_name','')}"
        self.win.destroy(); self._success(tid,eng_name,now,desc)
        if self.on_done: self.on_done()

    def _success(self,tid,eng_name,now,desc):
        win=tk.Toplevel(self.parent); win.title("Ticket Created"); win.configure(bg=BG); win.resizable(False,False); center(win,460,320)
        tk.Frame(win,bg=GREEN_BG,height=6).pack(fill="x")
        tk.Label(win,text="✅  Ticket Created Successfully!",bg=BG,fg=GREEN_BG,font=("Segoe UI",14,"bold")).pack(pady=(14,6))
        frm=tk.Frame(win,bg=BG); frm.pack(pady=4)
        for i,(ll,vv) in enumerate([("Ticket Number:",tid),("Assigned To:",f"{eng_name} (L1)"),("Date:",now.strftime("%Y-%m-%d")),("Time:",now.strftime("%H:%M")),("Summary:",(desc[:70]+"…") if len(desc)>70 else desc)]):
            tk.Label(frm,text=ll,bg=BG,fg=LABEL_FG,font=FONT_B,anchor="e",width=16).grid(row=i,column=0,sticky="e",padx=8,pady=4)
            tk.Label(frm,text=vv,bg=BG,fg="#1A3C5E",font=FONT,anchor="w",wraplength=260).grid(row=i,column=1,sticky="w",padx=8,pady=4)
        btn(win,"OK",win.destroy,12).pack(pady=12)
