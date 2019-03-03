class Slide:
    def __init__(self, d):
        self.d = d

    def __getitem__(self, y):
        return self.d[y]

    def __len__(self):
        return len(self.d['tags'])
    
    def __lt__(self, value):
        return len(self) >= len(value)
