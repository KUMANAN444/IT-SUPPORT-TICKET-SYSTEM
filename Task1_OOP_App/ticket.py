# ticket.py
# Ticket class for IT Support Ticket System

class Ticket:
    def __init__(self, title, priority, created_by):
        self.title = title
        self.priority = priority  # P1, P2, P3, P4
        self.created_by = created_by
        self.status = "Open"
        self.ticket_id = None
    
    def __str__(self):
        return f"Ticket #{self.ticket_id}: {self.title} ({self.priority})"

print("ticket.py loaded")
