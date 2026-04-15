"""gui/manager_window.py — Project Manager Dashboard v4
NEW: Asset Search, correct resolver name on resolve
"""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
from backend import data_manager as dm
from gui.utils import (BG,HEADER_BG,HEADER_FG,LABEL_FG,FONT,FONT_B,FONT_TITLE,FONT_SMALL,
                       ENTRY_BG,GREEN_BG,RED_BG,ORANGE_BG,TEAL_BG,CARD_COLS,DAYS,HOURS,
                       center,toplevel,header,btn,nav_btn,table,metric_card,
                       pw_change_dialog,ticket_detail,notification_popup,
                       lbl,ent,drop,date_spin,scroll_frame,kv_block,ask_reason)


class ManagerWindow:
    def __init__(self,root,mgr,on_logout):
        self.root=root; self.mgr=mgr; self.on_logout=on_logout
        self.win=tk.Toplevel(root); self.win.title(f"BankIT — Project Manager: {mgr['id']}")
        self.win.configure(bg=BG); self.win.protocol("WM_DELETE_WINDOW",self._logout)
        self.win.geometry("1120,750".replace(",","x")); center(self.win,1120,750); self._build()

    def _build(self):
        name=f"{self.mgr.get('first_name','Admin')} {self.mgr.get('last_name','Manager')}"
        header(self.win,f"Project Manager: {name}  |  ID: {self.mgr['id']}")
        notifs=dm.get_notifications(self.mgr["id"],unread_only=True)
        notif_lbl=f"🔔 ({len(notifs)})" if notifs else "🔔"
        nav=tk.Frame(self.win,bg=HEADER_BG,pady=4); nav.pack(fill="x")
        items=[
            ("➕ Create Account",  self._create_account),
            ("✏️ Modify Account",  self._modify_account),
            ("📊 Dashboard",       self._dashboard),
            ("📋 My Tickets",      self._my_tickets),
            ("🖥 Asset Search",    self._asset_search),
            ("🔎 Activities",      self._activities),
            ("🔍 Search Ticket",   self._search),
            (notif_lbl,            self._notifs),
            ("🔑 Password",        self._pw),
            ("🚪 Logout",           self._logout),
        ]
        for text,cmd in items:
            nav_btn(nav,text,cmd).pack(side="left",padx=3,pady=2)
        self.content=tk.Frame(self.win,bg=BG)
        self.content.pack(fill="both",expand=True,padx=10,pady=10)
        self._dashboard()

    def _clear(self):
        for w in self.content.winfo_children(): w.destroy()

    # ── Dashboard ─────────────────────────────────────────────────────────────
    def _dashboard(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="Dashboard",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=6,sticky="w",pady=(0,8))
        all_t=dm.get_all_tickets(); today_str=date.today().isoformat()
        metrics=[("Total",len(all_t)),("Open",sum(1 for t in all_t.values() if t.get("status")=="open")),
                 ("Pending",sum(1 for t in all_t.values() if t.get("status")=="pending")),
                 ("Escalated",sum(1 for t in all_t.values() if t.get("status")=="escalated")),
                 ("Resolved",sum(1 for t in all_t.values() if t.get("status")=="resolved")),
                 ("Today",sum(1 for t in all_t.values() if t.get("created_at","")[:10]==today_str))]
        for i,(lab,val) in enumerate(metrics):
            metric_card(frm,lab,val,CARD_COLS[i],row=1,col=i)

        filt=tk.LabelFrame(frm,text="  Filter & Report  ",bg=BG,fg=LABEL_FG,font=FONT_B,padx=10,pady=8)
        filt.grid(row=2,column=0,columnspan=6,sticky="ew",pady=12)
        get_from=date_spin(filt,0,1,"From Date:",0); get_to=date_spin(filt,1,1,"To Date:",0)
        lbl(filt,"Status:",0,2,w=10); _,st_var=drop(filt,0,3,["All","open","pending","escalated","resolved"],14); st_var.set("All")
        lbl(filt,"Category:",1,2,w=10); _,cat_var=drop(filt,1,3,["All","Hardware Related","Software Related","Account/Network Related"],22); cat_var.set("All")
        result_holder=[None]
        def run():
            if result_holder[0]: result_holder[0].destroy()
            fd=get_from(); td=get_to(); st=st_var.get(); cat=cat_var.get()
            filtered=[t for t in all_t.values() if fd<=t.get("created_at","")[:10]<=td
                      and(st=="All" or t.get("status")==st) and(cat=="All" or t.get("category")==cat)]
            rows=[(t["id"],t.get("user_name",""),t.get("category",""),
                   t.get("status","").upper(),t.get("assigned_to_name",""),t.get("created_at","")[:16]) for t in filtered]
            result_holder[0]=tk.Frame(frm,bg=BG); result_holder[0].grid(row=3,column=0,columnspan=6,sticky="nsew")
            tbl,tree=table(result_holder[0],("Ticket ID","User","Category","Status","Assigned To","Created"),
                           rows,height=10,on_dbl=lambda tv:self._open_any(tv,all_t))
            tbl.pack(fill="both",expand=True)
            tk.Label(result_holder[0],text=f"{len(filtered)} ticket(s) found.",bg=BG,fg="#555",font=FONT_SMALL).pack(anchor="w")
        btn(filt,"📊 Generate Report",run,22).grid(row=2,column=0,columnspan=4,pady=8)

    def _open_any(self,tree,all_t):
        sel=tree.selection()
        if not sel: return
        t=all_t.get(str(tree.item(sel[0])["values"][0]))
        if t: ticket_detail(self.win,t,can_act=False)

    # ── Create Account ────────────────────────────────────────────────────────
    def _create_account(self): CreateAccountDialog(self.win)

    # ── Modify Account ────────────────────────────────────────────────────────
    def _modify_account(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="Modify / Delete Account",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=3,sticky="w",pady=(0,8))
        lbl(frm,"Staff ID:",1,w=12); id_e=ent(frm,1); id_e.focus_set()
        holder=[None]
        def search():
            if holder[0]: holder[0].destroy()
            sid=id_e.get().strip()
            if not sid: return
            role,rec=dm.get_account_by_id(sid)
            if not rec: messagebox.showerror("Not Found",f"No account for: {sid}"); return
            holder[0]=AccountEditor(frm,role,rec,row_start=3)
        btn(frm,"🔍 Search",search,12).grid(row=1,column=2,padx=8)
        id_e.bind("<Return>",lambda e:search())

    # ── My Tickets ────────────────────────────────────────────────────────────
    def _my_tickets(self):
        self._clear()
        tk.Label(self.content,text="Tickets Escalated to Me (from L2)",bg=BG,fg=LABEL_FG,font=FONT_TITLE).pack(anchor="w",pady=(0,6))
        all_t=dm.get_all_tickets()
        mine={k:v for k,v in all_t.items() if v.get("assigned_to","").upper()==self.mgr["id"].upper()}
        rows=[(t["id"],t.get("user_name",""),t.get("category",""),t.get("status","").upper(),t.get("created_at","")[:16]) for t in mine.values()]
        frm,tree=table(self.content,("Ticket ID","User","Category","Status","Created"),rows,height=18,
                       on_dbl=lambda tv:self._open_manager_ticket(tv,mine))
        frm.pack(fill="both",expand=True)
        tk.Label(self.content,text="Double-click to resolve or request more info.",bg=BG,fg="#888",font=FONT_SMALL).pack(anchor="w")

    def _open_manager_ticket(self,tree,tdict):
        sel=tree.selection()
        if not sel: return
        t=tdict.get(str(tree.item(sel[0])["values"][0]))
        if not t: return
        is_mine=t.get("assigned_to","").upper()==self.mgr["id"].upper()
        can_act=is_mine and t.get("status")!="resolved"
        ManagerTicketDialog(self.win,t,self.mgr,on_done=self._my_tickets,can_act=can_act)

    # ── NEW: Asset Search ─────────────────────────────────────────────────────
    def _asset_search(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="🖥  Asset Search",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=4,sticky="w",pady=(0,4))
        tk.Label(frm,text="Search any device by serial number. Shows device type and assigned owner.",
                 bg=BG,fg="#555",font=FONT).grid(row=1,column=0,columnspan=4,sticky="w",pady=(0,8))

        lbl(frm,"Serial Number:",2,w=16); q_e=ent(frm,2,width=24); q_e.focus_set()
        result_holder=[None]

        def search():
            if result_holder[0]: result_holder[0].destroy()
            q=q_e.get().strip()
            if not q: return
            results=dm.search_asset(q)
            result_holder[0]=tk.Frame(frm,bg=BG); result_holder[0].grid(row=4,column=0,columnspan=4,sticky="nsew",pady=8)
            if not results:
                tk.Label(result_holder[0],text=f"❌  No asset found matching '{q}'.",bg=BG,fg=RED_BG,font=FONT_B).pack(pady=12)
                return

            # Show result cards for each match
            for a in results:
                card=tk.Frame(result_holder[0],bg="#EEF4FF",relief="solid",bd=1)
                card.pack(fill="x",padx=4,pady=4)
                kv_block(card,[
                    ("Serial Number:", a["serial"]),
                    ("Device Type:",   a["device_type"]),
                    ("Assigned To:",   a["owner_name"]),
                    ("Staff ID:",      a["owner_id"]),
                    ("Role:",          a["owner_role"]),
                ],lw=16,wrap=420)

        def show_all():
            if result_holder[0]: result_holder[0].destroy()
            all_assets=dm.build_asset_registry()
            result_holder[0]=tk.Frame(frm,bg=BG); result_holder[0].grid(row=4,column=0,columnspan=4,sticky="nsew",pady=8)
            tk.Label(result_holder[0],text=f"All Registered Assets  ({len(all_assets)} devices):",
                     bg=BG,fg=LABEL_FG,font=FONT_B).pack(anchor="w",pady=(0,4))
            rows=[(a["serial"],a["device_type"],a["owner_name"],a["owner_id"],a["owner_role"]) for a in all_assets]
            tbl,_=table(result_holder[0],("Serial Number","Device Type","Owner","Owner ID","Role"),rows,height=16)
            tbl.pack(fill="x",padx=4)

        btn(frm,"🔍 Search Asset",search,16).grid(row=2,column=2,padx=8)
        btn(frm,"📋 All Assets",show_all,14,bg=TEAL_BG,fg="white").grid(row=2,column=3,padx=4)
        q_e.bind("<Return>",lambda e:search())

    # ── Check Activities ──────────────────────────────────────────────────────
    def _activities(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="Check Activities by Staff ID",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=3,sticky="w",pady=(0,8))
        lbl(frm,"Staff ID:",1,w=12); id_e=ent(frm,1); id_e.focus_set()
        holder=[None]
        def lookup():
            if holder[0]: holder[0].destroy()
            sid=id_e.get().strip()
            if not sid: return
            role,rec=dm.get_account_by_id(sid)
            if not rec: messagebox.showerror("Not Found",f"No account for: {sid}"); return
            all_t=dm.get_all_tickets()
            holder[0]=tk.Frame(frm,bg=BG,relief="solid",bd=1); holder[0].grid(row=3,column=0,columnspan=3,sticky="nsew",pady=8,padx=4)
            rf=holder[0]
            if "engineer" in role:
                stats=dm.get_engineer_stats(rec["id"])
                kv_block(rf,[("ID:",rec.get("id")),("Name:",f"{rec.get('first_name','')} {rec.get('last_name','')}"),
                             ("Role:",role.replace("_"," ").title()),
                             ("Total Assigned:",stats["total"]),("Open:",stats["open"]),
                             ("Pending:",stats["pending"]),("Escalated (to them):",stats["escalated"]),
                             ("Resolved by Them:",stats["resolved"]),("Escalated by Them:",stats["escalated_by_me"]),
                             ("PC Serial:",rec.get("computer_serial","N/A")),("Mobile Serial:",rec.get("mobile_serial","N/A"))])
            elif role=="user":
                user_t={k:v for k,v in all_t.items() if v.get("user_id","").upper()==rec["id"].upper()}
                kv_block(rf,[("ID:",rec.get("id")),("Name:",f"{rec.get('first_name','')} {rec.get('last_name','')}"),
                             ("Total Tickets:",len(user_t)),
                             ("Resolved:",sum(1 for t in user_t.values() if t.get("status")=="resolved")),
                             ("Pending:",sum(1 for t in user_t.values() if t.get("status")=="pending")),
                             ("Escalated:",sum(1 for t in user_t.values() if t.get("status")=="escalated")),
                             ("PC Serial:",rec.get("computer_serial","N/A")),("Mobile Serial:",rec.get("mobile_serial","N/A"))])
                rows=[(t["id"],t.get("category",""),t.get("status","").upper(),t.get("created_at","")[:16]) for t in user_t.values()]
                if rows:
                    tbl,_=table(rf,("Ticket ID","Category","Status","Created"),rows,height=6); tbl.pack(fill="x",padx=10,pady=6)
        btn(frm,"🔍 Look Up",lookup,14).grid(row=1,column=2,padx=8); id_e.bind("<Return>",lambda e:lookup())

    # ── Search Ticket ─────────────────────────────────────────────────────────
    def _search(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="Search Any Ticket",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=3,sticky="w",pady=(0,8))
        lbl(frm,"Ticket ID:",1,w=12); id_e=ent(frm,1); id_e.focus_set()
        def search():
            tid=id_e.get().strip()
            if not tid: return
            t=dm.get_ticket(tid)
            if not t: messagebox.showerror("Not Found",f"Ticket '{tid}' not found."); return
            ticket_detail(self.win,t,can_act=False)
        btn(frm,"🔍 Search",search,12).grid(row=1,column=2,padx=8); id_e.bind("<Return>",lambda e:search())

    def _notifs(self):
        notification_popup(self.win,dm.get_notifications(self.mgr["id"]),
                           on_clear=lambda:dm.mark_notifications_read(self.mgr["id"]))

    def _pw(self):
        pw_change_dialog(self.win,verify_fn=lambda old:self.mgr.get("password")==old,
                         update_fn=lambda new:(dm.update_manager_password(self.mgr["id"],new),self.mgr.update({"password":new})))

    def _logout(self): self.win.destroy(); self.on_logout()


# ── Create Account Dialog ─────────────────────────────────────────────────────
class CreateAccountDialog:
    def __init__(self,parent):
        self.parent=parent; self.win=toplevel(parent,"Create New Account",520,560)
        header(self.win,"Create New Account"); self._build()
    def _build(self):
        frm=tk.Frame(self.win,bg=BG); frm.pack(padx=20,pady=10)
        lbl(frm,"Role:",0,w=20); self._rv=tk.StringVar()
        ttk.Combobox(frm,textvariable=self._rv,values=["L1 Engineer","L2 Engineer","User"],
                     width=26,state="readonly",font=FONT).grid(row=0,column=1,sticky="w",padx=8,pady=6)
        fields=[(1,"First Name:","first_name"),(2,"Last Name:","last_name"),(3,"Phone Number:","phone"),
                (4,"PC Serial:","computer_serial"),(5,"Mobile Name/Serial:","mobile_serial")]
        self._ents={}
        for row,lab,key in fields: lbl(frm,lab,row,w=20); e=ent(frm,row); self._ents[key]=e
        lbl(frm,"Date of Birth:",6,w=20); self._get_dob=date_spin(frm,6)
        def submit():
            role=self._rv.get()
            if not role: messagebox.showerror("Error","Please select a role.",parent=self.win); return
            info={k:e.get().strip() for k,e in self._ents.items()}
            if not all(info.values()): messagebox.showerror("Error","Please fill all fields.",parent=self.win); return
            info["dob"]=self._get_dob(); otp=dm.generate_otp()
            if role=="L1 Engineer": uid=dm.create_engineer(info,1)
            elif role=="L2 Engineer": uid=dm.create_engineer(info,2)
            else: uid=dm.create_user(info)
            dm.store_otp(uid,otp); self.win.destroy(); self._show_creds(uid,otp,role)
        btn(frm,"✔ Create Account",submit,22).grid(row=7,column=0,columnspan=2,pady=14)
        btn(frm,"✖ Cancel",self.win.destroy,12,RED_BG,"white").grid(row=8,column=0,columnspan=2)
    def _show_creds(self,uid,otp,role):
        win=toplevel(self.parent,"Account Created",440,260); header(win,"✅  Account Created!")
        frm=tk.Frame(win,bg=BG); frm.pack(pady=10)
        kv_block(frm,[("Role:",role),("Staff ID:",uid),("One-Time Password:",otp),("Note:","Share with the new member.")])
        btn(win,"OK",win.destroy,12).pack(pady=12)


# ── Account Editor ────────────────────────────────────────────────────────────
class AccountEditor:
    def __init__(self,parent_frm,role,record,row_start=3):
        self.role=role; self.record=record
        self.frm=tk.Frame(parent_frm,bg=BG,relief="solid",bd=1)
        self.frm.grid(row=row_start,column=0,columnspan=3,sticky="nsew",pady=8,padx=4); self._build()
    def _build(self):
        rec=self.record
        info=[("ID:",rec.get("id","")),("Role:",self.role.replace("_"," ").title()),
              ("Name:",f"{rec.get('first_name','')} {rec.get('last_name','')}"),
              ("Phone:",rec.get("phone","")),("PC Serial:",rec.get("computer_serial","")),
              ("Mobile:",rec.get("mobile_serial","")),("DOB:",rec.get("dob","")),
              ("Created:",rec.get("created_at","")[:16])]
        kv_block(self.frm,info)
        bf=tk.Frame(self.frm,bg=BG); bf.grid(row=len(info),column=0,columnspan=2,pady=10)
        btn(bf,"✏️ Modify",self._modify,12).pack(side="left",padx=6)
        btn(bf,"🗑 Delete",self._delete,12,RED_BG,"white").pack(side="left",padx=6)
    def _modify(self): EditAccountDialog(self.frm.winfo_toplevel(),self.role,self.record)
    def _delete(self):
        rid=self.record["id"]
        if not messagebox.askyesno("Confirm",f"Permanently delete {rid}?"): return
        if self.role=="user": dm.delete_user(rid)
        elif "engineer" in self.role: dm.delete_engineer(rid)
        messagebox.showinfo("Deleted",f"Account {rid} deleted."); self.frm.destroy()


class EditAccountDialog:
    def __init__(self,parent,role,record):
        self.role=role; self.record=record
        win=toplevel(parent,f"Edit {record['id']}",480,380); header(win,f"Edit — {record['id']}")
        frm=tk.Frame(win,bg=BG); frm.pack(padx=20,pady=12)
        fields=[(0,"First Name:","first_name"),(1,"Last Name:","last_name"),(2,"Phone:","phone"),
                (3,"PC Serial:","computer_serial"),(4,"Mobile Serial:","mobile_serial")]
        entries={}
        for r,lab,key in fields: lbl(frm,lab,r,w=18); e=ent(frm,r); e.insert(0,record.get(key,"")); entries[key]=e
        def save():
            updates={k:e.get().strip() for k,e in entries.items()}
            if role=="user": dm.update_user(record["id"],updates)
            elif "engineer" in role: dm.update_engineer(record["id"],updates)
            record.update(updates); messagebox.showinfo("Saved","Account updated.",parent=win); win.destroy()
        btn(frm,"💾 Save Changes",save,20).grid(row=5,column=0,columnspan=2,pady=14)


# ── Manager Ticket Action Dialog ──────────────────────────────────────────────
class ManagerTicketDialog:
    """Manager resolves or requests more info. Uses resolve_ticket to record manager's name."""
    def __init__(self,parent,ticket,manager,on_done=None,can_act=True):
        self.ticket=ticket; self.manager=manager; self.on_done=on_done; self.can_act=can_act
        self.win=toplevel(parent,f"Ticket {ticket['id']}",740,660)
        header(self.win,f"Ticket {ticket['id']}  —  Manager Action"); self._build()

    def _build(self):
        t=self.ticket; outer,inner=scroll_frame(self.win); outer.pack(fill="both",expand=True,padx=8,pady=4)

        pairs=[("Ticket ID:",t.get("id","")),("Status:",t.get("status","").upper()),
               ("Category:",t.get("category","")),("Subcategory:",t.get("subcategory","")),
               ("Issue Type:",t.get("issue_type","")),("Description:",t.get("description","")),
               ("User:",f"{t.get('user_name','')} ({t.get('user_id','')})"),
               ("Assigned To:",f"{t.get('assigned_to_name','')} ({t.get('assigned_to','')})"),
               ("Created:",t.get("created_at","")[:16])]
        if t.get("status")=="resolved" and t.get("resolved_by_name"):
            pairs.append(("Resolved By:",f"{t.get('resolved_by_name','')} ({t.get('resolved_by_id','')})"))

        r=kv_block(inner,pairs)

        # Work notes
        tk.Label(inner,text="Work Notes:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne").grid(row=r,column=0,sticky="ne",padx=8,pady=6)
        wn=tk.Text(inner,width=52,height=6,font=FONT,relief="solid",bd=1)
        wn.grid(row=r,column=1,sticky="w",padx=8,pady=6)
        for n in t.get("work_notes",[]):
            ts=n.get("timestamp","")[:16] if isinstance(n,dict) else""
            nm=n.get("author_name","")    if isinstance(n,dict) else""
            nt=n.get("note","")           if isinstance(n,dict) else str(n)
            wn.insert("end",f"[{ts}] {nm}: {nt}\n")
        wn.config(state="disabled"); r+=1

        # Escalation chain
        if t.get("escalation_history"):
            tk.Label(inner,text="Escalation Chain:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne").grid(row=r,column=0,sticky="ne",padx=8,pady=6)
            et=tk.Text(inner,width=52,height=3,font=FONT,relief="solid",bd=1)
            et.grid(row=r,column=1,sticky="w",padx=8,pady=6)
            for eh in t.get("escalation_history",[]):
                ts=eh.get("timestamp","")[:16] if isinstance(eh,dict) else""
                fn=eh.get("from_name","")      if isinstance(eh,dict) else""
                tn=eh.get("to_name","")        if isinstance(eh,dict) else""
                rs=eh.get("reason","")         if isinstance(eh,dict) else str(eh)
                et.insert("end",f"[{ts}] {fn} → {tn}: {rs}\n")
            et.config(state="disabled"); r+=1

        if self.can_act:
            tk.Label(inner,text="Manager Note:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne").grid(row=r,column=0,sticky="ne",padx=8,pady=6)
            self._note=tk.Text(inner,width=52,height=3,font=FONT,relief="solid",bd=1)
            self._note.grid(row=r,column=1,sticky="w",padx=8,pady=6); r+=1
            bf=tk.Frame(inner,bg=BG); bf.grid(row=r,column=0,columnspan=2,pady=12)
            if t.get("status")!="resolved":
                btn(bf,"✔ Resolve",        lambda:self._act("resolved"),14,GREEN_BG,"white").pack(side="left",padx=6)
                btn(bf,"⏳ Request More Info",lambda:self._act("pending"),18,ORANGE_BG,"white").pack(side="left",padx=6)
        btn(self.win,"Close",self.win.destroy,10).pack(pady=8)

    def _act(self,status):
        note=self._note.get("1.0","end").strip() if self.can_act else ""
        mgr_name=f"{self.manager.get('first_name','Admin')} {self.manager.get('last_name','Manager')} (PM)"
        if status=="resolved":
            # CORRECT: resolve_ticket records manager's name as resolver
            dm.resolve_ticket(self.ticket["id"],self.manager["id"],mgr_name,note)
        else:
            if note: dm.add_work_note(self.ticket["id"],self.manager["id"],mgr_name,note)
            dm.update_ticket(self.ticket["id"],{"status":status})
        messagebox.showinfo("Updated",f"Ticket status: {status.upper()}")
        self.win.destroy()
        if self.on_done: self.on_done()
