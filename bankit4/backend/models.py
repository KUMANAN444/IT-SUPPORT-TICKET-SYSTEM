"""backend/models.py — OOP domain models for BankIT v4"""
from datetime import datetime
from abc import ABC, abstractmethod
import random, string


class Person(ABC):
    def __init__(self, person_id, first_name, last_name, phone,
                 computer_serial, mobile_serial, dob, password=""):
        self.__id = person_id.upper()
        self.__pw = password
        self._first = first_name;   self._last  = last_name
        self._phone = phone;        self._pc    = computer_serial
        self._mob   = mobile_serial;self._dob   = dob
        self._created = datetime.now().isoformat()

    @property
    def person_id(self):    return self.__id
    @property
    def full_name(self):    return f"{self._first} {self._last}"
    @property
    def first_name(self):   return self._first
    @property
    def last_name(self):    return self._last
    @property
    def phone(self):        return self._phone
    @property
    def computer_serial(self): return self._pc
    @property
    def mobile_serial(self):   return self._mob
    @property
    def dob(self):          return self._dob
    @property
    def created_at(self):   return self._created

    @first_name.setter
    def first_name(self, v): self._first = v.strip()
    @last_name.setter
    def last_name(self, v):  self._last  = v.strip()
    @phone.setter
    def phone(self, v):      self._phone = v.strip()
    @computer_serial.setter
    def computer_serial(self, v): self._pc = v.strip()
    @mobile_serial.setter
    def mobile_serial(self, v):   self._mob= v.strip()

    def check_password(self, pw): return self.__pw == pw
    def set_password(self, pw):   self.__pw = pw
    def get_password_raw(self):   return self.__pw

    @abstractmethod
    def get_display_role(self): pass
    @abstractmethod
    def get_role_key(self):     pass

    def __str__(self):  return f"{self.get_display_role()}: {self.full_name} ({self.person_id})"
    def __repr__(self): return f"<{self.__class__.__name__} id={self.person_id}>"
    def __eq__(self, o):return isinstance(o, Person) and self.person_id == o.person_id

    def to_dict(self):
        return {"id": self.person_id, "first_name": self._first, "last_name": self._last,
                "phone": self._phone, "computer_serial": self._pc, "mobile_serial": self._mob,
                "dob": self._dob, "password": self.__pw, "created_at": self._created,
                "role": self.get_role_key()}

    @classmethod
    def _base(cls, d):
        return dict(person_id=d.get("id",""), first_name=d.get("first_name",""),
                    last_name=d.get("last_name",""), phone=d.get("phone",""),
                    computer_serial=d.get("computer_serial",""),
                    mobile_serial=d.get("mobile_serial",""),
                    dob=d.get("dob",""), password=d.get("password",""))


class User(Person):
    def get_display_role(self): return "User"
    def get_role_key(self):     return "user"
    @classmethod
    def from_dict(cls, d):
        o = cls(**cls._base(d)); o._created = d.get("created_at", o._created); return o


class Engineer(Person):
    def __init__(self, level, **kw):
        super().__init__(**kw)
        if level not in (1,2): raise ValueError("level 1 or 2")
        self._level = level; self._avail = {}
    @property
    def level(self): return self._level
    @property
    def availability(self): return self._avail
    @availability.setter
    def availability(self, v): self._avail = v

    def is_available_now(self):
        now = datetime.now(); day = now.strftime("%A"); cur = now.strftime("%H:%M")
        info = self._avail.get(day, {})
        if not info.get("enabled", False): return False
        return info.get("from","00:00") <= cur <= info.get("to","23:59")

    def get_display_role(self): return f"L{self._level} Engineer"
    def get_role_key(self):     return f"l{self._level}_engineer"

    def to_dict(self):
        d = super().to_dict(); d["level"] = self._level; d["availability"] = self._avail
        return d

    @classmethod
    def from_dict(cls, d, level):
        o = cls(level=level, **cls._base(d))
        o._created = d.get("created_at", o._created)
        o._avail   = d.get("availability", {})
        return o


class Manager(Person):
    def get_display_role(self): return "Project Manager"
    def get_role_key(self):     return "manager"
    @classmethod
    def from_dict(cls, d):
        o = cls(**cls._base(d)); o._created = d.get("created_at", o._created); return o


class WorkNote:
    def __init__(self, author_id, author_name, note, timestamp=None):
        self.author_id = author_id; self.author_name = author_name
        self.note = note; self.timestamp = timestamp or datetime.now().isoformat()
    def to_dict(self):
        return {"author_id":self.author_id,"author_name":self.author_name,
                "note":self.note,"timestamp":self.timestamp}
    @classmethod
    def from_dict(cls, d):
        return cls(d.get("author_id",""),d.get("author_name",""),d.get("note",""),d.get("timestamp"))
    def __str__(self): return f"[{self.timestamp[:16]}] {self.author_name}: {self.note}"


class EscalationRecord:
    def __init__(self, from_id, from_name, to_id, to_name, reason, timestamp=None):
        self.from_id=from_id; self.from_name=from_name
        self.to_id=to_id;     self.to_name=to_name
        self.reason=reason;   self.timestamp=timestamp or datetime.now().isoformat()
    def to_dict(self):
        return {"from_id":self.from_id,"from_name":self.from_name,"to_id":self.to_id,
                "to_name":self.to_name,"reason":self.reason,"timestamp":self.timestamp}
    @classmethod
    def from_dict(cls, d):
        return cls(d.get("from_id",""),d.get("from_name",""),d.get("to_id",""),
                   d.get("to_name",""),d.get("reason",""),d.get("timestamp"))
    def __str__(self): return f"[{self.timestamp[:16]}] {self.from_name} → {self.to_name}: {self.reason}"


class Ticket:
    VALID_STATUSES = ("open","pending","escalated","resolved")

    def __init__(self, ticket_id, user_id, user_name, category, subcategory,
                 issue_type, sub_issue, description, assigned_to, assigned_to_name,
                 assigned_level, status="open", created_at=None,
                 work_notes=None, escalation_history=None,
                 resolved_by_id="", resolved_by_name=""):
        self._id          = ticket_id.upper()
        self._user_id     = user_id;   self._user_name    = user_name
        self._category    = category;  self._subcategory  = subcategory
        self._issue_type  = issue_type;self._sub_issue    = sub_issue
        self._description = description
        self._assigned_to = assigned_to; self._assigned_name = assigned_to_name
        self._assigned_lvl= assigned_level
        self._status      = status
        self._created     = created_at or datetime.now().isoformat()
        self._notes: list = work_notes or []
        self._escalations: list = escalation_history or []
        # NEW: track who actually clicked Resolve
        self._resolved_by_id   = resolved_by_id
        self._resolved_by_name = resolved_by_name

    @property
    def ticket_id(self):          return self._id
    @property
    def user_id(self):            return self._user_id
    @property
    def user_name(self):          return self._user_name
    @property
    def category(self):           return self._category
    @property
    def subcategory(self):        return self._subcategory
    @property
    def issue_type(self):         return self._issue_type
    @property
    def sub_issue(self):          return self._sub_issue
    @property
    def description(self):        return self._description
    @property
    def assigned_to(self):        return self._assigned_to
    @property
    def assigned_to_name(self):   return self._assigned_name
    @property
    def assigned_level(self):     return self._assigned_lvl
    @property
    def status(self):             return self._status
    @property
    def created_at(self):         return self._created
    @property
    def work_notes(self):         return list(self._notes)
    @property
    def escalation_history(self): return list(self._escalations)
    @property
    def resolved_by_id(self):     return self._resolved_by_id
    @property
    def resolved_by_name(self):   return self._resolved_by_name

    @status.setter
    def status(self, v):
        if v not in self.VALID_STATUSES: raise ValueError(f"Bad status: {v}")
        self._status = v

    def reassign(self, new_id, new_name, new_level):
        self._assigned_to = new_id; self._assigned_name = new_name; self._assigned_lvl = new_level

    def add_work_note(self, author_id, author_name, note):
        if note.strip():
            self._notes.append(WorkNote(author_id, author_name, note.strip()))

    def resolve(self, resolver_id, resolver_name, note=""):
        """Resolve and record EXACTLY who clicked the resolve button."""
        self._status           = "resolved"
        self._resolved_by_id   = resolver_id
        self._resolved_by_name = resolver_name
        if note.strip():
            self.add_work_note(resolver_id, resolver_name, note.strip())

    def add_escalation(self, from_id, from_name, to_id, to_name, reason):
        self._escalations.append(EscalationRecord(from_id, from_name, to_id, to_name, reason))
        self.reassign(to_id, to_name, None)
        self._status = "escalated"

    @staticmethod
    def generate_id(counter): return f"REQ{counter:05d}"

    def __str__(self):  return f"Ticket {self._id} [{self._status.upper()}]"
    def __repr__(self): return f"<Ticket id={self._id} status={self._status}>"
    def __eq__(self, o):return isinstance(o, Ticket) and self._id == o._id

    def to_dict(self):
        return {"id":self._id,"user_id":self._user_id,"user_name":self._user_name,
                "category":self._category,"subcategory":self._subcategory,
                "issue_type":self._issue_type,"sub_issue":self._sub_issue,
                "description":self._description,"assigned_to":self._assigned_to,
                "assigned_to_name":self._assigned_name,"assigned_level":self._assigned_lvl,
                "status":self._status,"created_at":self._created,
                "resolved_by_id":self._resolved_by_id,
                "resolved_by_name":self._resolved_by_name,
                "work_notes":[n.to_dict() for n in self._notes],
                "escalation_history":[e.to_dict() for e in self._escalations]}

    @classmethod
    def from_dict(cls, d):
        return cls(
            ticket_id=d.get("id",""), user_id=d.get("user_id",""),
            user_name=d.get("user_name",""), category=d.get("category",""),
            subcategory=d.get("subcategory",""), issue_type=d.get("issue_type",""),
            sub_issue=d.get("sub_issue",""), description=d.get("description",""),
            assigned_to=d.get("assigned_to",""), assigned_to_name=d.get("assigned_to_name",""),
            assigned_level=d.get("assigned_level",1), status=d.get("status","open"),
            created_at=d.get("created_at"),
            resolved_by_id=d.get("resolved_by_id",""),
            resolved_by_name=d.get("resolved_by_name",""),
            work_notes=[WorkNote.from_dict(n) for n in d.get("work_notes",[])],
            escalation_history=[EscalationRecord.from_dict(e) for e in d.get("escalation_history",[])])
