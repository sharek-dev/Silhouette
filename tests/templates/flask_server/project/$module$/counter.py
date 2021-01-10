
class ViewsCounter:

    def __init__(self):
        self.views = 0
    
    def increment(self):
        self.views += 1
        return self.views