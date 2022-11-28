class Category:
    def __init__(self, name, priority=None):
        self.name = name
        self.priority = priority

    def get_priority(self):
        return self.priority
    
    def set_priority(self, priority):
        self.priority = priority
