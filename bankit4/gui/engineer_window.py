"""
gui/engineer_window.py — L1 & L2 Engineer Dashboard
NEW FEATURES:
  1. Personal stats dashboard (cards + table)
  2. Asset search for L2 only
  3. Resolve records the EXACT engineer who clicked Resolve (not L1)
  4. L2 can fully act on escalated tickets (the core bug fix)
"""
import tkinter as tk
from tkinter import messagebox, ttk
from backend import data_manager as dm
from gui.utils import (BG,HEADER_BG,HEADER_FG,LABEL_FG,FONT,FONT_B,FONT_TITLE,FONT_SMALL,
                       GREEN_BG,RED_BG,ORANGE_BG,PURPLE_BG,TEAL_BG,NAVY_BG,CARD_COLS,DAYS,HOURS,
                       center,toplevel,header,btn,nav_btn,table,_fill_table,
                       pw_change_dialog,ticket_detail,notification_popup,
                       lbl,ent,scroll_frame,kv_block,ask_reason,metric_card)


class EngineerWindow:
    def __init__(self,root,engineer,level,on_logout):
        self.root=root; self.eng=engineer; self.level=level; self.on_logout=on_logout
        self.win=tk.Toplevel(root); self.win.title(f"BankIT — L{level} Engineer: {engineer['id']}")
        self.win.configure(bg=BG); self.win.protocol("WM_DELETE_WINDOW",self._logout)
        self.win.geometry("1060x720"); center(self.win,1060,720); self._build()

    def _build(self):
        name=f"{self.eng.get('first_name','')} {self.eng.get('last_name','')}"
        header(self.win,f"L{self.level} Engineer: {name}  |  ID: {self.eng['id']}")

        notifs=dm.get_notifications(self.eng["id"],unread_only=True)
        notif_lbl=f"🔔 ({len(notifs)})" if notifs else "🔔"

        nav=tk.Frame(self.win,bg=HEADER_BG,pady=4); nav.pack(fill="x")
        items=[
            ("📊 My Dashboard",  self._dashboard),
            ("📅 Availability",  self._availability),
            ("🆕 New Tickets",   lambda:self._show_list("New",     ["open"])),
            ("⏳ Pending",        lambda:self._show_list("Pending", ["pending"])),
            ("✅ Completed",      lambda:self._show_list("Completed",["resolved"])),
            ("⬆ Escalated",     lambda:self._show_list("Escalated",["escalated"])),
            ("🔍 Search Ticket", self._search),
        ]
        if self.level==2:
            items.append(("🖥 Asset Search", self._asset_search))
        items+=[
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

    # ── NEW: Personal Stats Dashboard ─────────────────────────────────────────
    def _dashboard(self):
        self._clear(); frm=self.content
        name=f"{self.eng.get('first_name','')} {self.eng.get('last_name','')}"
        tk.Label(frm,text=f"My Dashboard  —  {name}",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=6,sticky="w",pady=(0,8))

        stats=dm.get_engineer_stats(self.eng["id"])

        # Stats cards — clickable to filter the list below
        cards=[
            ("Total Assigned", stats["total"],     CARD_COLS[0], lambda:self._show_list("All",["open","pending","escalated","resolved"])),
            ("Open",           stats["open"],      CARD_COLS[1], lambda:self._show_list("New",["open"])),
            ("Pending",        stats["pending"],   CARD_COLS[2], lambda:self._show_list("Pending",["pending"])),
            ("Escalated",      stats["escalated"], CARD_COLS[3], lambda:self._show_list("Escalated",["escalated"])),
            ("Resolved by Me", stats["resolved"],  CARD_COLS[4], lambda:self._show_list("Completed",["resolved"])),
            ("I Escalated",    stats["escalated_by_me"], CARD_COLS[5], None),
        ]
        for i,(lab,val,color,cmd) in enumerate(cards):
            metric_card(frm,lab,val,color,row=1,col=i,cmd=cmd)

        tk.Label(frm,text="(Click a card to view those tickets)",bg=BG,fg="#888",font=FONT_SMALL).grid(
            row=2,column=0,columnspan=6,sticky="w",pady=(2,8))

        # My active tickets table below
        my_tickets=dm.get_tickets_by_engineer(self.eng["id"])
        active={k:v for k,v in my_tickets.items() if v.get("status")!="resolved"}

        tk.Label(frm,text="My Active Tickets",bg=BG,fg=LABEL_FG,font=FONT_B).grid(
            row=3,column=0,columnspan=6,sticky="w",pady=(4,2))

        rows=[(t["id"],t.get("user_name",""),t.get("category",""),
               t.get("status","").upper(),t.get("created_at","")[:16])
              for t in active.values()]
        tbl,tree=table(frm,("Ticket ID","User","Category","Status","Created"),rows,height=10,
                       on_dbl=lambda tv:self._open_from_dict(tv,my_tickets))
        tbl.grid(row=4,column=0,columnspan=6,sticky="nsew")
        tk.Label(frm,text="Double-click to open.",bg=BG,fg="#888",font=FONT_SMALL).grid(
            row=5,column=0,columnspan=6,sticky="w")

    def _open_from_dict(self,tree,tdict):
        sel=tree.selection()
        if not sel: return
        tid=str(tree.item(sel[0])["values"][0])
        t=tdict.get(tid)
        if not t: return
        is_mine=t.get("assigned_to","").upper()==self.eng["id"].upper()
        can_act=is_mine and t.get("status")!="resolved"
        esc_lbl="⬆ Escalate to Manager" if self.level==2 else "⬆ Escalate to L2"
        ticket_detail(self.win,t,can_act=can_act,
                      action_fn=(lambda action,note,reason:self._act(t,action,note,reason)) if can_act else None,
                      current_user_id=self.eng["id"],escalate_label=esc_lbl)

    # ── Availability ──────────────────────────────────────────────────────────
    def _availability(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="Set My Availability",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=5,sticky="w",pady=(0,10))
        avail=self.eng.get("availability",{}); dvars={}
        for c,ht in enumerate(["Day","Available","From","To"]):
            tk.Label(frm,text=ht,bg=BG,fg=LABEL_FG,font=FONT_B,width=10).grid(row=1,column=c,padx=8,pady=4)
        for i,day in enumerate(DAYS):
            r=i+2; info=avail.get(day,{})
            tk.Label(frm,text=day,bg=BG,fg="#333",font=FONT,width=12,anchor="w").grid(row=r,column=0,padx=8,pady=4)
            ev=tk.BooleanVar(value=info.get("enabled",False)); tk.Checkbutton(frm,variable=ev,bg=BG).grid(row=r,column=1)
            fv=tk.StringVar(value=info.get("from","09:00")); tv=tk.StringVar(value=info.get("to","18:00"))
            ttk.Combobox(frm,textvariable=fv,values=HOURS,width=8,state="readonly",font=FONT).grid(row=r,column=2,padx=8)
            ttk.Combobox(frm,textvariable=tv,values=HOURS,width=8,state="readonly",font=FONT).grid(row=r,column=3,padx=8)
            dvars[day]=(ev,fv,tv)

        def save():
            new_avail={day:{"enabled":ev.get(),"from":fv.get(),"to":tv.get()} for day,(ev,fv,tv) in dvars.items()}
            dm.update_engineer_availability(self.eng["id"],new_avail); self.eng["availability"]=new_avail
            messagebox.showinfo("Saved","Availability updated! ✓")
        btn(frm,"💾 Save Availability",save,22).grid(row=len(DAYS)+2,column=0,columnspan=4,pady=16)

    # ── Ticket list ───────────────────────────────────────────────────────────
    def _show_list(self,title,statuses):
        self._clear()
        tk.Label(self.content,text=f"{title} Tickets",bg=BG,fg=LABEL_FG,font=FONT_TITLE).pack(anchor="w",pady=(0,6))
        my=dm.get_tickets_by_engineer(self.eng["id"])
        filtered={k:v for k,v in my.items() if v.get("status") in statuses}
        rows=[(t["id"],t.get("user_name",""),t.get("category",""),
               t.get("subcategory",""),t.get("status","").upper(),t.get("created_at","")[:16])
              for t in filtered.values()]
        frm,tree=table(self.content,("Ticket ID","User","Category","Subcategory","Status","Created"),
                       rows,height=18,on_dbl=lambda tv:self._open_from_dict(tv,filtered))
        frm.pack(fill="both",expand=True)
        tk.Label(self.content,text="Double-click to open and act on a ticket.",bg=BG,fg="#888",font=FONT_SMALL).pack(anchor="w",pady=2)

    # ── Core action handler (THE FIX: uses resolve_ticket with exact resolver) ─
    def _act(self,ticket_dict,action,note,reason):
        tid=ticket_dict["id"]
        eng_name=f"{self.eng.get('first_name','')} {self.eng.get('last_name','')}"

        if action=="resolved":
            # Uses resolve_ticket which records THIS engineer's name as resolver
            dm.resolve_ticket(tid, self.eng["id"], f"{eng_name} (L{self.level})", note)
            messagebox.showinfo("Resolved",f"Ticket {tid} resolved by {eng_name}. ✓")

        elif action=="pending":
            if note: dm.add_work_note(tid,self.eng["id"],eng_name,note)
            dm.update_ticket(tid,{"status":"pending"})
            messagebox.showinfo("Updated",f"Ticket {tid} set to PENDING.")

        elif action=="escalated":
            if note: dm.add_work_note(tid,self.eng["id"],eng_name,note)
            if self.level==1:
                next_eng=dm.get_available_engineer(2)
                if not next_eng:
                    messagebox.showerror("Error","No L2 engineers available.\nAsk the manager to create one."); return
                to_id=next_eng["id"]; to_name=f"{next_eng.get('first_name','')} {next_eng.get('last_name','')} (L2)"
            else:
                managers=dm.get_all_managers()
                if not managers: messagebox.showerror("Error","No manager found."); return
                mgr=next(iter(managers.values())); to_id=mgr["id"]
                to_name=f"{mgr.get('first_name','Admin')} {mgr.get('last_name','Manager')} (PM)"
            dm.escalate_ticket(tid,self.eng["id"],f"{eng_name} (L{self.level})",reason,to_id,to_name)
            messagebox.showinfo("Escalated",f"Ticket {tid} escalated to: {to_name}")

        self._dashboard()   # refresh

    # ── Search ────────────────────────────────────────────────────────────────
    def _search(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="Search Any Ticket by ID",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=3,sticky="w",pady=(0,8))
        lbl(frm,"Ticket ID:",1,w=14); id_e=ent(frm,1); id_e.focus_set()
        def search():
            tid=id_e.get().strip()
            if not tid: return
            t=dm.get_ticket(tid)
            if not t: messagebox.showerror("Not Found",f"Ticket '{tid}' not found."); return
            is_mine=t.get("assigned_to","").upper()==self.eng["id"].upper()
            can_act=is_mine and t.get("status")!="resolved"
            esc_lbl="⬆ Escalate to Manager" if self.level==2 else "⬆ Escalate to L2"
            ticket_detail(self.win,t,can_act=can_act,
                          action_fn=(lambda a,n,r:self._act(t,a,n,r)) if can_act else None,
                          current_user_id=self.eng["id"],escalate_label=esc_lbl)
        btn(frm,"🔍 Search",search,14).grid(row=1,column=2,padx=8)

    # ── NEW: Asset Search (L2 only) ───────────────────────────────────────────
    def _asset_search(self):
        self._clear(); frm=self.content
        tk.Label(frm,text="🖥  Asset Search",bg=BG,fg=LABEL_FG,font=FONT_TITLE).grid(
            row=0,column=0,columnspan=3,sticky="w",pady=(0,4))
        tk.Label(frm,text="Search by device serial number to find the assigned owner.",
                 bg=BG,fg="#555",font=FONT).grid(row=1,column=0,columnspan=3,sticky="w",pady=(0,8))

        lbl(frm,"Serial Number:",2,w=16); q_e=ent(frm,2,width=24); q_e.focus_set()
        result_holder=[None]

        def search():
            if result_holder[0]: result_holder[0].destroy()
            q=q_e.get().strip()
            if not q: return
            results=dm.search_asset(q)
            result_holder[0]=tk.Frame(frm,bg=BG); result_holder[0].grid(row=4,column=0,columnspan=3,sticky="nsew",pady=8)
            if not results:
                tk.Label(result_holder[0],text=f"No asset found matching '{q}'.",bg=BG,fg=RED_BG,font=FONT_B).pack(pady=10)
                return
            tk.Label(result_holder[0],text=f"  {len(results)} result(s) found for '{q.upper()}':",
                     bg=BG,fg=LABEL_FG,font=FONT_B).pack(anchor="w",pady=(0,4))
            rows=[(a["serial"],a["device_type"],a["owner_name"],a["owner_id"],a["owner_role"])
                  for a in results]
            tbl,_=table(result_holder[0],("Serial Number","Device Type","Owner","Owner ID","Role"),
                        rows,height=min(len(rows)+2,10))
            tbl.pack(fill="x",padx=4)

        btn(frm,"🔍 Search Asset",search,16).grid(row=2,column=2,padx=8)
        # Also search on Enter
        q_e.bind("<Return>",lambda e:search())

        # Show all assets button
        def show_all():
            if result_holder[0]: result_holder[0].destroy()
            all_assets=dm.build_asset_registry()
            result_holder[0]=tk.Frame(frm,bg=BG); result_holder[0].grid(row=4,column=0,columnspan=3,sticky="nsew",pady=8)
            tk.Label(result_holder[0],text=f"  All registered assets ({len(all_assets)} total):",
                     bg=BG,fg=LABEL_FG,font=FONT_B).pack(anchor="w",pady=(0,4))
            rows=[(a["serial"],a["device_type"],a["owner_name"],a["owner_id"],a["owner_role"]) for a in all_assets]
            tbl,_=table(result_holder[0],("Serial Number","Device Type","Owner","Owner ID","Role"),rows,height=14)
            tbl.pack(fill="x",padx=4)

        btn(frm,"📋 Show All Assets",show_all,18,bg=TEAL_BG,fg="white").grid(row=2,column=3,padx=8)

    # ── Notifications ─────────────────────────────────────────────────────────
    def _notifs(self):
        notification_popup(self.win,dm.get_notifications(self.eng["id"]),
                           on_clear=lambda:(dm.mark_notifications_read(self.eng["id"]),self._build_nav_badge()))

    def _build_nav_badge(self): pass  # nav is static; just called for side-effect

    # ── Change password ───────────────────────────────────────────────────────
    def _pw(self):
        pw_change_dialog(self.win,
            verify_fn=lambda old:self.eng.get("password")==old,
            update_fn=lambda new:(dm.update_engineer_password(self.eng["id"],new),self.eng.update({"password":new})))

    def _logout(self): self.win.destroy(); self.on_logout()
