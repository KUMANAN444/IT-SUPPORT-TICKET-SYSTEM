"""gui/utils.py — Shared GUI helpers for BankIT v4"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

BG="#F0F4F8"; HEADER_BG="#1A3C5E"; HEADER_FG="#FFFFFF"
BTN_BG="#1A3C5E"; BTN_FG="#FFFFFF"; BTN_HOVER="#254E7A"
ENTRY_BG="#FFFFFF"; LABEL_FG="#1A3C5E"
ROW_ODD="#EAF0F6"; ROW_EVEN="#FFFFFF"
GREEN_BG="#388E3C"; RED_BG="#C62828"; ORANGE_BG="#F57C00"; PURPLE_BG="#7B1FA2"
TEAL_BG="#00838F"; NAVY_BG="#1565C0"
CARD_COLS=["#1565C0","#0288D1","#F57C00","#7B1FA2","#388E3C","#D32F2F"]
STATUS_COL={"open":"#2196F3","pending":"#FF9800","escalated":"#9C27B0","resolved":"#4CAF50"}

FONT=("Segoe UI",10); FONT_B=("Segoe UI",10,"bold")
FONT_TITLE=("Segoe UI",14,"bold"); FONT_SMALL=("Segoe UI",9)
DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
HOURS=[f"{h:02d}:{m:02d}" for h in range(0,24) for m in (0,30)]


def center(win,w,h):
    win.update_idletasks()
    x=(win.winfo_screenwidth()-w)//2; y=(win.winfo_screenheight()-h)//2
    win.geometry(f"{w}x{h}+{x}+{y}")

def toplevel(parent,title,w,h):
    t=tk.Toplevel(parent); t.title(title); t.configure(bg=BG)
    t.resizable(True,True); center(t,w,h); t.grab_set(); return t

def header(parent,text):
    f=tk.Frame(parent,bg=HEADER_BG); f.pack(fill="x")
    tk.Label(f,text=text,bg=HEADER_BG,fg=HEADER_FG,font=FONT_TITLE,pady=10).pack()
    return f

def btn(parent,text,cmd,w=16,bg=BTN_BG,fg=BTN_FG,**gkw):
    b=tk.Button(parent,text=text,command=cmd,bg=bg,fg=fg,font=FONT_B,width=w,
                relief="flat",cursor="hand2",activebackground=BTN_HOVER,
                activeforeground=fg,padx=8,pady=6)
    b.bind("<Enter>",lambda e:b.config(bg=BTN_HOVER if bg==BTN_BG else bg))
    b.bind("<Leave>",lambda e:b.config(bg=bg))
    if gkw: b.grid(**gkw)
    return b

def nav_btn(parent,text,cmd):
    b=tk.Button(parent,text=text,command=cmd,bg=HEADER_BG,fg=HEADER_FG,
                font=("Segoe UI",9,"bold"),relief="flat",padx=9,pady=5,
                cursor="hand2",activebackground=BTN_HOVER,activeforeground=HEADER_FG)
    b.bind("<Enter>",lambda e:b.config(bg=BTN_HOVER))
    b.bind("<Leave>",lambda e:b.config(bg=HEADER_BG))
    return b

def lbl(parent,text,row,col=0,w=20,sticky="e"):
    l=tk.Label(parent,text=text,bg=BG,fg=LABEL_FG,font=FONT_B,anchor="e",width=w)
    l.grid(row=row,column=col,sticky=sticky,padx=8,pady=5); return l

def ent(parent,row,col=1,width=28,show=""):
    e=tk.Entry(parent,width=width,bg=ENTRY_BG,relief="solid",font=FONT,show=show)
    e.grid(row=row,column=col,sticky="w",padx=8,pady=5); return e

def drop(parent,row,col=1,values=None,width=26):
    var=tk.StringVar()
    cb=ttk.Combobox(parent,textvariable=var,values=values or [],
                    width=width,state="readonly",font=FONT)
    cb.grid(row=row,column=col,sticky="w",padx=8,pady=5)
    return cb,var

def date_spin(parent,row,col=1,label=None,lcol=0):
    if label: lbl(parent,label,row,lcol)
    f=tk.Frame(parent,bg=BG); f.grid(row=row,column=col,sticky="w",padx=8,pady=5)
    now=datetime.now()
    yv=tk.StringVar(value=str(now.year)); mv=tk.StringVar(value=f"{now.month:02d}"); dv=tk.StringVar(value=f"{now.day:02d}")
    tk.Spinbox(f,from_=2020,to=2035,textvariable=yv,width=5,font=FONT).pack(side="left")
    tk.Label(f,text="-",bg=BG,font=FONT).pack(side="left")
    tk.Spinbox(f,from_=1,to=12,textvariable=mv,format="%02.0f",width=3,font=FONT).pack(side="left")
    tk.Label(f,text="-",bg=BG,font=FONT).pack(side="left")
    tk.Spinbox(f,from_=1,to=31,textvariable=dv,format="%02.0f",width=3,font=FONT).pack(side="left")
    return lambda: f"{yv.get()}-{mv.get()}-{dv.get()}"

def table(parent,columns,rows,on_dbl=None,height=14):
    style=ttk.Style(); style.theme_use("clam")
    style.configure("BK.Treeview",background=ROW_EVEN,fieldbackground=ROW_EVEN,font=FONT,rowheight=26)
    style.configure("BK.Treeview.Heading",font=FONT_B,background=HEADER_BG,foreground=HEADER_FG)
    style.map("BK.Treeview",background=[("selected","#254E7A")],foreground=[("selected","#FFF")])
    frame=tk.Frame(parent,bg=BG)
    tree=ttk.Treeview(frame,columns=columns,show="headings",height=height,
                      style="BK.Treeview",selectmode="browse")
    vsb=ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
    hsb=ttk.Scrollbar(frame,orient="horizontal",command=tree.xview)
    tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
    CW={"Ticket ID":90,"User":110,"Category":140,"Subcategory":140,"Status":80,
        "Created":130,"Assigned To":140,"Issue Type":130,"Serial Number":130,
        "Device Type":160,"Owner":120,"Owner ID":90,"Role":100,"Priority":70}
    for c in columns:
        tree.heading(c,text=c); tree.column(c,width=CW.get(c,110),anchor="center",minwidth=60)
    tree.tag_configure("odd",background=ROW_ODD); tree.tag_configure("even",background=ROW_EVEN)
    _fill_table(tree,rows)
    if on_dbl: tree.bind("<Double-1>",lambda e:on_dbl(tree))
    vsb.pack(side="right",fill="y"); hsb.pack(side="bottom",fill="x")
    tree.pack(fill="both",expand=True)
    return frame,tree

def _fill_table(tree,rows):
    tree.delete(*tree.get_children())
    for i,row in enumerate(rows):
        tree.insert("","end",values=row,tags=("odd" if i%2 else "even",))

def scroll_frame(parent):
    outer=tk.Frame(parent,bg=BG); canvas=tk.Canvas(outer,bg=BG,highlightthickness=0)
    vsb=ttk.Scrollbar(outer,orient="vertical",command=canvas.yview)
    inner=tk.Frame(canvas,bg=BG)
    inner.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0),window=inner,anchor="nw")
    canvas.configure(yscrollcommand=vsb.set)
    canvas.bind_all("<MouseWheel>",lambda e:canvas.yview_scroll(int(-1*(e.delta/120)),"units"))
    canvas.pack(side="left",fill="both",expand=True); vsb.pack(side="right",fill="y")
    return outer,inner

def metric_card(parent,label,value,color,row,col,cmd=None):
    f=tk.Frame(parent,bg=color,padx=14,pady=10,cursor="hand2" if cmd else "")
    f.grid(row=row,column=col,padx=6,pady=6,sticky="nsew")
    tk.Label(f,text=str(value),bg=color,fg="white",font=("Segoe UI",20,"bold")).pack()
    tk.Label(f,text=label,bg=color,fg="#DDD",font=FONT_SMALL).pack()
    if cmd: f.bind("<Button-1>",lambda e:cmd()); [w.bind("<Button-1>",lambda e:cmd()) for w in f.winfo_children()]

def kv_block(parent,pairs,start=0,lw=22,wrap=380):
    for i,(k,v) in enumerate(pairs):
        r=start+i
        tk.Label(parent,text=k,bg=BG,fg=LABEL_FG,font=FONT_B,anchor="e",width=lw).grid(
            row=r,column=0,sticky="e",padx=8,pady=3)
        tk.Label(parent,text=str(v),bg=BG,fg="#333",font=FONT,anchor="w",
                 wraplength=wrap,justify="left").grid(row=r,column=1,sticky="w",padx=8,pady=3)
    return start+len(pairs)

def ask_reason(parent,title="Enter Reason"):
    res={"v":None}
    win=toplevel(parent,title,440,210)
    tk.Label(win,text=title+":",bg=BG,fg=LABEL_FG,font=FONT_B).pack(padx=12,pady=(10,4),anchor="w")
    txt=tk.Text(win,width=50,height=4,font=FONT,relief="solid",bd=1)
    txt.pack(padx=12); txt.focus_set()
    def ok(): res["v"]=txt.get("1.0","end").strip(); win.destroy()
    def cancel(): win.destroy()
    f=tk.Frame(win,bg=BG); f.pack(pady=8)
    btn(f,"OK",ok,10).pack(side="left",padx=6)
    btn(f,"Cancel",cancel,10,RED_BG,"white").pack(side="left",padx=6)
    win.bind("<Return>",lambda e:ok()); parent.wait_window(win); return res["v"]

def pw_change_dialog(parent,verify_fn,update_fn):
    win=toplevel(parent,"Change Password",380,270); header(win,"Change Password")
    f=tk.Frame(win,bg=BG); f.pack(padx=20,pady=12)
    lbl(f,"Current Password:",0); old_e=ent(f,0,show="*")
    lbl(f,"New Password:",1);     new_e=ent(f,1,show="*")
    lbl(f,"Confirm Password:",2); con_e=ent(f,2,show="*")
    def submit():
        if not verify_fn(old_e.get().strip()):
            messagebox.showerror("Error","Current password incorrect.",parent=win); return
        n=new_e.get().strip()
        if len(n)<4: messagebox.showerror("Error","Min 4 characters.",parent=win); return
        if n!=con_e.get().strip(): messagebox.showerror("Error","Passwords don't match.",parent=win); return
        update_fn(n); messagebox.showinfo("Success","Password changed! ✓",parent=win); win.destroy()
    btn(f,"Change Password",submit,20,row=3,column=0,columnspan=2,pady=14)

def first_login_dialog(parent,update_fn):
    win=toplevel(parent,"Set Your Password",400,240); header(win,"Set Your New Password")
    tk.Label(win,text="You logged in with a one-time password.\nPlease set a permanent password.",
             bg=BG,fg=LABEL_FG,font=FONT,justify="center").pack(pady=8)
    f=tk.Frame(win,bg=BG); f.pack()
    lbl(f,"New Password:",0);     new_e=ent(f,0,show="*")
    lbl(f,"Confirm Password:",1); con_e=ent(f,1,show="*")
    def submit():
        n=new_e.get().strip()
        if len(n)<4: messagebox.showerror("Error","Min 4 characters.",parent=win); return
        if n!=con_e.get().strip(): messagebox.showerror("Error","Passwords don't match.",parent=win); return
        update_fn(n); win.destroy()
    btn(f,"Set Password",submit,20,row=2,column=0,columnspan=2,pady=12)
    win.protocol("WM_DELETE_WINDOW",lambda:None); parent.wait_window(win)


def ticket_detail(parent,ticket_dict,can_act=False,action_fn=None,
                  current_user_id="",escalate_label="⬆ Escalate"):
    """Universal ticket detail popup. THE FIX: can_act is based on assignment, not status."""
    t=ticket_dict; tid=t.get("id","?")
    win=toplevel(parent,f"Ticket {tid}",740,680); win.resizable(True,True)
    sc=STATUS_COL.get(t.get("status","open"),HEADER_BG)
    tk.Frame(win,bg=sc,height=6).pack(fill="x")
    header(win,f"Ticket {tid}"+(""if can_act else"  (View Only)"))

    outer,inner=scroll_frame(win); outer.pack(fill="both",expand=True,padx=8,pady=4)

    esc_count=len(t.get("escalation_history",[])); 
    priority="🔴 CRITICAL" if esc_count>=2 else("🟠 HIGH" if esc_count==1 else"🟢 NORMAL")

    pairs=[
        ("Ticket ID:",   t.get("id","")),
        ("Priority:",    priority),
        ("Status:",      t.get("status","").upper()),
        ("Category:",    t.get("category","")),
        ("Subcategory:", t.get("subcategory","")),
        ("Issue Type:",  t.get("issue_type","")),
        ("Sub-Issue:",   t.get("sub_issue","")),
        ("Description:", t.get("description","")),
        ("Raised By:",   f"{t.get('user_name','')} ({t.get('user_id','')})"),
        ("Assigned To:", f"{t.get('assigned_to_name','')} ({t.get('assigned_to','')})"),
        ("Created At:",  t.get("created_at","")[:16]),
    ]
    # Show who resolved it if resolved
    if t.get("status")=="resolved" and t.get("resolved_by_name"):
        pairs.append(("Resolved By:", f"{t.get('resolved_by_name','')} ({t.get('resolved_by_id','')})"))

    r=kv_block(inner,pairs)

    tk.Label(inner,text="Work Notes:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne").grid(
        row=r,column=0,sticky="ne",padx=8,pady=6)
    wn=tk.Text(inner,width=52,height=5,font=FONT,relief="solid",bd=1)
    wn.grid(row=r,column=1,sticky="w",padx=8,pady=6)
    for n in t.get("work_notes",[]):
        ts=n.get("timestamp","")[:16] if isinstance(n,dict) else""
        nm=n.get("author_name","")    if isinstance(n,dict) else""
        nt=n.get("note","")           if isinstance(n,dict) else str(n)
        wn.insert("end",f"[{ts}] {nm}: {nt}\n")
    wn.config(state="disabled"); r+=1

    if t.get("escalation_history"):
        tk.Label(inner,text="Escalation History:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne").grid(
            row=r,column=0,sticky="ne",padx=8,pady=6)
        et=tk.Text(inner,width=52,height=3,font=FONT,relief="solid",bd=1)
        et.grid(row=r,column=1,sticky="w",padx=8,pady=6)
        for eh in t.get("escalation_history",[]):
            ts=eh.get("timestamp","")[:16] if isinstance(eh,dict) else""
            fn=eh.get("from_name","")      if isinstance(eh,dict) else""
            tn=eh.get("to_name","")        if isinstance(eh,dict) else""
            rs=eh.get("reason","")         if isinstance(eh,dict) else str(eh)
            et.insert("end",f"[{ts}] {fn} → {tn}: {rs}\n")
        et.config(state="disabled"); r+=1

    if can_act and action_fn:
        tk.Label(inner,text="Add Work Note:",bg=BG,fg=LABEL_FG,font=FONT_B,anchor="ne").grid(
            row=r,column=0,sticky="ne",padx=8,pady=6)
        note_txt=tk.Text(inner,width=52,height=3,font=FONT,relief="solid",bd=1)
        note_txt.grid(row=r,column=1,sticky="w",padx=8,pady=6); r+=1

        bf=tk.Frame(inner,bg=BG); bf.grid(row=r,column=0,columnspan=2,pady=12)
        def do(action):
            note=note_txt.get("1.0","end").strip()
            if action=="escalated":
                reason=ask_reason(win,"Reason for Escalation")
                if not reason: return
                action_fn(action,note,reason)
            else: action_fn(action,note,"")
            win.destroy()
        if t.get("status")!="resolved":
            btn(bf,"✔ Resolve",  lambda:do("resolved"),12,GREEN_BG,"white").pack(side="left",padx=5)
            btn(bf,"⏳ Pending", lambda:do("pending"), 12,ORANGE_BG,"white").pack(side="left",padx=5)
            btn(bf,escalate_label,lambda:do("escalated"),15,PURPLE_BG,"white").pack(side="left",padx=5)

    btn(win,"Close",win.destroy,10).pack(pady=8)


def notification_popup(parent,notifs,on_clear):
    win=toplevel(parent,"Notifications",580,460)
    header(win,f"🔔 Notifications  ({len(notifs)} total)")
    outer,inner=scroll_frame(win); outer.pack(fill="both",expand=True,padx=8,pady=6)
    if not notifs:
        tk.Label(inner,text="No notifications.",bg=BG,fg="#888",font=FONT).pack(pady=20)
    else:
        for n in reversed(notifs):
            bg2="#EEF4FF" if not n.get("read") else BG
            f=tk.Frame(inner,bg=bg2,relief="solid",bd=1); f.pack(fill="x",padx=4,pady=3)
            tk.Label(f,text=n.get("timestamp","")[:16],bg=bg2,fg="#888",font=FONT_SMALL).pack(anchor="w",padx=6)
            tk.Label(f,text=n.get("message",""),bg=bg2,fg="#333",font=FONT,
                     wraplength=520,justify="left").pack(anchor="w",padx=6,pady=(0,4))
    btn(win,"✓ Mark All Read",on_clear,18).pack(pady=8)
