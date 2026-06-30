import random

FALLBACK_GEM = "grey"

class GemBag:
    def __init__(self, composition):
        self.composition = composition
        self.bag = []
        self._fill()

    def _fill(self):
        self.bag = []
        for gem_type, count in self.composition["tier_1"].items():
            self.bag.extend([gem_type] * count)
        random.shuffle(self.bag)

    def draw(self):
        if not self.bag:
            return (FALLBACK_GEM, 1, 1)
        return (self.bag.pop(), 1, 1)

    def is_empty(self):
        return len(self.bag) == 0