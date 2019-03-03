class Slide:
    def __init__(self, d):
        self.d = d

    def __getitem__(self, y):
        return self.d[y]

    def __len__(self):
        return len(self.d['tags'])
    
    def __lt__(self, value):
        a = self['num']
        b = self['num']
        a, b = [min(x) if x.__class__ == set else x for x in (a, b)]
        return a >= b
        # return len(self) >= len(value)
