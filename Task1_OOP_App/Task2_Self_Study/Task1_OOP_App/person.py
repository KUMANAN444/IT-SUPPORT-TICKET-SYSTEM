# person.py
# Base classes for IT Support Ticket System

class Person:
    def __init__(self, name, emp_id):
        self.name = name
        self.emp_id = emp_id
    
    def get_role(self):
        return "Person"

# More classes will be added later
print("person.py loaded")
