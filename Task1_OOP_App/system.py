# system.py
# Main system class for IT Support Ticket System

class TicketSystem:
    def __init__(self, company_name):
        self.company_name = company_name
        self.tickets = []
        self.users = []
    
    def create_ticket(self, title, priority, user):
        # Will add logic later
        print(f"Ticket created: {title}")
        
    def __str__(self):
        return f"Ticket System for {self.company_name}"

print("system.py loaded")
