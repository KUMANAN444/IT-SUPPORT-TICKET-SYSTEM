"""backend/data_manager.py — JSON persistence layer for BankIT v4"""
import json, os, random, string
from datetime import datetime
from backend.models import User, Engineer, Manager, Ticket

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FILES = {k: os.path.join(DATA_DIR, f"{k}.json") for k in
         ("users","l1_engineers","l2_engineers","managers",
          "tickets","otp","counters","notifications")}


# ── File I/O ──────────────────────────────────────────────────────────────────
def _ensure(): os.makedirs(DATA_DIR, exist_ok=True)

def _load(key):
    _ensure(); p = FILES[key]
    if not os.path.exists(p): return {}
    with open(p, encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def _save(key, data):
    _ensure()
    with open(FILES[key], "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ── Counters ──────────────────────────────────────────────────────────────────
def _next(name):
    c = _load("counters"); v = c.get(name,10000)+1; c[name]=v; _save("counters",c); return v

# ── OTP ───────────────────────────────────────────────────────────────────────
def generate_otp():       return "".join(random.choices(string.digits, k=6))
def store_otp(uid, otp):  d=_load("otp"); d[uid.upper()]=otp; _save("otp",d)
def get_otp(uid):         return _load("otp").get(uid.upper())
def remove_otp(uid):      d=_load("otp"); d.pop(uid.upper(),None); _save("otp",d)

# ── Notifications ─────────────────────────────────────────────────────────────
def add_notification(recipient_id, message, ticket_id=""):
    d = _load("notifications"); uid = recipient_id.upper()
    if uid not in d: d[uid] = []
    d[uid].append({"message":message,"ticket_id":ticket_id,
                   "timestamp":datetime.now().isoformat(),"read":False})
    _save("notifications", d)

def get_notifications(recipient_id, unread_only=False):
    items = _load("notifications").get(recipient_id.upper(), [])
    return [n for n in items if not n.get("read")] if unread_only else items

def mark_notifications_read(recipient_id):
    d = _load("notifications"); uid = recipient_id.upper()
    for n in d.get(uid,[]): n["read"] = True
    _save("notifications", d)

# ── Managers ──────────────────────────────────────────────────────────────────
def init_default_manager():
    d = _load("managers")
    if "PR12345" not in d:
        mgr = Manager(person_id="PR12345", first_name="Admin", last_name="Manager",
                      phone="00000000", computer_serial="MGR-PC-001",
                      mobile_serial="MGR-MOB-001", dob="1980-01-01", password="246810")
        d["PR12345"] = mgr.to_dict(); _save("managers", d)

def get_manager(mid):    return _load("managers").get(mid.upper())
def get_all_managers():  return _load("managers")

def update_manager_password(mid, pw):
    d = _load("managers"); k = mid.upper()
    if k in d: d[k]["password"]=pw; _save("managers",d); return True
    return False

def save_manager(rec):
    d = _load("managers"); d[rec["id"].upper()] = rec; _save("managers", d)

# ── Users ─────────────────────────────────────────────────────────────────────
def create_user(info):
    uid = f"US{_next('user'):05d}"
    u   = User(person_id=uid, first_name=info.get("first_name",""),
               last_name=info.get("last_name",""), phone=info.get("phone",""),
               computer_serial=info.get("computer_serial",""),
               mobile_serial=info.get("mobile_serial",""), dob=info.get("dob",""))
    d = _load("users"); d[uid] = u.to_dict(); _save("users", d); return uid

def get_user(uid):   return _load("users").get(uid.upper())
def get_all_users(): return _load("users")

def update_user(uid, info):
    d = _load("users"); k = uid.upper()
    if k in d: d[k].update(info); _save("users",d); return True
    return False

def update_user_password(uid, pw): return update_user(uid, {"password":pw})

def delete_user(uid):
    d = _load("users"); k = uid.upper()
    if k in d: del d[k]; _save("users",d); return True
    return False

# ── Engineers ─────────────────────────────────────────────────────────────────
def create_engineer(info, level):
    eid = f"LE{_next('engineer'):05d}"
    e   = Engineer(level=level, person_id=eid, first_name=info.get("first_name",""),
                   last_name=info.get("last_name",""), phone=info.get("phone",""),
                   computer_serial=info.get("computer_serial",""),
                   mobile_serial=info.get("mobile_serial",""), dob=info.get("dob",""))
    key = f"l{level}_engineers"
    d = _load(key); d[eid] = e.to_dict(); _save(key,d); return eid

def get_engineer(eid):
    k = eid.upper()
    for lv in (1,2):
        d = _load(f"l{lv}_engineers")
        if k in d: return d[k]
    return None

def update_engineer(eid, info):
    k = eid.upper()
    for lv in (1,2):
        key = f"l{lv}_engineers"; d = _load(key)
        if k in d: d[k].update(info); _save(key,d); return True
    return False

def update_engineer_password(eid, pw): return update_engineer(eid, {"password":pw})
def update_engineer_availability(eid, avail): return update_engineer(eid, {"availability":avail})

def delete_engineer(eid):
    k = eid.upper()
    for lv in (1,2):
        key = f"l{lv}_engineers"; d = _load(key)
        if k in d: del d[k]; _save(key,d); return True
    return False

def get_all_engineers(level): return _load(f"l{level}_engineers")

def get_available_engineer(level):
    """Round-robin: fewest active tickets among available engineers."""
    data = _load(f"l{level}_engineers")
    if not data: return None
    now = datetime.now(); day = now.strftime("%A"); cur = now.strftime("%H:%M")
    avail = [e for e in data.values()
             if (a:=e.get("availability",{}).get(day,{}))
             and a.get("enabled") and a.get("from","00:00")<=cur<=a.get("to","23:59")]
    pool = avail if avail else list(data.values())
    if not pool: return None
    pool.sort(key=lambda e: e.get("created_at",""))
    tickets = _load("tickets")
    counts  = {e["id"]:sum(1 for t in tickets.values()
                           if t.get("assigned_to","")==e["id"] and t.get("status")!="resolved")
               for e in pool}
    return min(pool, key=lambda e: counts.get(e["id"],0))

# ── Tickets ───────────────────────────────────────────────────────────────────
def create_ticket(info):
    tid = Ticket.generate_id(_next("ticket"))
    t   = Ticket(ticket_id=tid, user_id=info["user_id"], user_name=info["user_name"],
                 category=info["category"], subcategory=info["subcategory"],
                 issue_type=info["issue_type"], sub_issue=info.get("sub_issue",""),
                 description=info["description"], assigned_to=info["assigned_to"],
                 assigned_to_name=info["assigned_to_name"],
                 assigned_level=info.get("assigned_level",1))
    d = _load("tickets"); d[tid] = t.to_dict(); _save("tickets",d)
    add_notification(info["assigned_to"], f"New ticket {tid} assigned: {info['description'][:60]}", tid)
    return tid

def get_ticket(tid):
    return _load("tickets").get(tid.upper())

def update_ticket(tid, info):
    d = _load("tickets"); k = tid.upper()
    if k in d: d[k].update(info); _save("tickets",d); return True
    return False

def resolve_ticket(tid, resolver_id, resolver_name, note=""):
    """Resolve a ticket and record EXACTLY who resolved it."""
    d = _load("tickets"); k = tid.upper()
    if k not in d: return False
    t = Ticket.from_dict(d[k])
    t.resolve(resolver_id, resolver_name, note)
    d[k] = t.to_dict(); _save("tickets",d)
    # Notify the ticket owner (user)
    add_notification(t.user_id,
        f"Your ticket {tid} has been RESOLVED by {resolver_name}.", tid)
    return True

def add_work_note(tid, author_id, author_name, note):
    if not note.strip(): return False
    d = _load("tickets"); k = tid.upper()
    if k not in d: return False
    t = Ticket.from_dict(d[k]); t.add_work_note(author_id, author_name, note)
    d[k] = t.to_dict(); _save("tickets",d); return True

def escalate_ticket(tid, from_id, from_name, reason, to_id, to_name):
    d = _load("tickets"); k = tid.upper()
    if k not in d: return False
    t = Ticket.from_dict(d[k])
    t.add_escalation(from_id, from_name, to_id, to_name, reason)
    d[k] = t.to_dict(); _save("tickets",d)
    add_notification(to_id, f"Ticket {tid} escalated to you from {from_name}. Reason: {reason[:60]}", tid)
    return True

def get_all_tickets():              return _load("tickets")
def get_tickets_by_user(uid):       return {k:v for k,v in _load("tickets").items() if v.get("user_id","").upper()==uid.upper()}
def get_tickets_by_engineer(eid):   return {k:v for k,v in _load("tickets").items() if v.get("assigned_to","").upper()==eid.upper()}


# ── ASSET REGISTRY ────────────────────────────────────────────────────────────
def build_asset_registry():
    """
    Build a searchable asset registry from all accounts.
    Returns list of dicts:
      {serial, device_type, owner_name, owner_id, owner_role}
    Both PC serial and mobile serial are included.
    """
    assets = []

    def _add(serial, device_type, owner_name, owner_id, owner_role):
        if serial and serial.strip():
            assets.append({
                "serial":     serial.strip().upper(),
                "device_type":device_type,
                "owner_name": owner_name,
                "owner_id":   owner_id,
                "owner_role": owner_role,
            })

    for uid, u in get_all_users().items():
        name = f"{u.get('first_name','')} {u.get('last_name','')}".strip()
        _add(u.get("computer_serial",""), "Laptop/Desktop (User PC)", name, uid, "User")
        _add(u.get("mobile_serial",""),   "Mobile Device (User Phone)", name, uid, "User")

    for lv in (1,2):
        for eid, e in get_all_engineers(lv).items():
            name = f"{e.get('first_name','')} {e.get('last_name','')}".strip()
            role = f"L{lv} Engineer"
            _add(e.get("computer_serial",""), f"Laptop/Desktop ({role} PC)", name, eid, role)
            _add(e.get("mobile_serial",""),   f"Mobile Device ({role} Phone)", name, eid, role)

    for mid, m in get_all_managers().items():
        name = f"{m.get('first_name','')} {m.get('last_name','')}".strip()
        _add(m.get("computer_serial",""), "Laptop/Desktop (Manager PC)", name, mid, "Manager")
        _add(m.get("mobile_serial",""),   "Mobile Device (Manager Phone)", name, mid, "Manager")

    return assets


def search_asset(query):
    """
    Search assets by serial number (partial, case-insensitive).
    Returns list of matching asset dicts.
    """
    q = query.strip().upper()
    if not q: return []
    return [a for a in build_asset_registry() if q in a["serial"]]


# ── Engineer stats ────────────────────────────────────────────────────────────
def get_engineer_stats(eid):
    """
    Return dashboard statistics for an engineer.
    {total, open, pending, escalated, resolved, escalated_by_me}
    """
    all_t = get_all_tickets()
    # All tickets currently assigned to this engineer
    mine  = [t for t in all_t.values() if t.get("assigned_to","").upper()==eid.upper()]
    # Tickets this engineer escalated to the next level
    esc_by_me = [t for t in all_t.values()
                 if any(e.get("from_id","").upper()==eid.upper()
                        for e in t.get("escalation_history",[]))]
    # Tickets resolved BY this engineer (regardless of current assignment)
    resolved_by_me = [t for t in all_t.values()
                      if t.get("resolved_by_id","").upper()==eid.upper()]
    return {
        "total":          len(mine),
        "open":           sum(1 for t in mine if t.get("status")=="open"),
        "pending":        sum(1 for t in mine if t.get("status")=="pending"),
        "escalated":      sum(1 for t in mine if t.get("status")=="escalated"),
        "resolved":       len(resolved_by_me),
        "escalated_by_me":len(esc_by_me),
    }


# ── Authentication ────────────────────────────────────────────────────────────
def authenticate(uid, pw):
    k = uid.upper()
    m = get_manager(k)
    if m and m.get("password")==pw: return "manager", m

    otp = get_otp(k)
    if otp and otp==pw:
        u = get_user(k)
        if u: return "otp_user", u
        e = get_engineer(k)
        if e: return f"otp_l{e['level']}_engineer", e
        return None, None

    u = get_user(k)
    if u and u.get("password")==pw: return "user", u

    e = get_engineer(k)
    if e and e.get("password")==pw: return f"l{e['level']}_engineer", e

    return None, None


def get_account_by_id(any_id):
    k = any_id.upper()
    m = get_manager(k)
    if m: return "manager", m
    u = get_user(k)
    if u: return "user", u
    e = get_engineer(k)
    if e: return f"l{e['level']}_engineer", e
    return None, None
