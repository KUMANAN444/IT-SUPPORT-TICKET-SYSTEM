# heap_demo.py
# Preliminary code for Heap data structure

class Heap:
    def __init__(self):
        self.items = []
    
    def insert(self, value):
        self.items.append(value)
        print(f"Inserted: {value}")
    
    def __str__(self):
        return f"Heap: {self.items}"

# Simple test
if __name__ == "__main__":
    h = Heap()
    h.insert(10)
    h.insert(5)
    h.insert(20)
    print(h)
