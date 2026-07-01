class GemStash:
    MAX_SIZE = 9
    
    def __init__(self, origin_x, origin_y, slot_size=55):
        self.tokens = []
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.slot_size = slot_size
        
    def add(self, gem_token):
        if len(self.tokens) < self.MAX_SIZE:
            self.tokens.append(gem_token)
            return True
        return False
    
    def remove(self, gem_token):
        self.tokens.remove(gem_token)
            
    def is_full(self):
        return len(self.tokens) >= self.MAX_SIZE
    
    def draw(self, surf):
        for i, token in enumerate(self.tokens):
            pos = self._get_slot_pos(i)
            surf.blit(token.icon, pos)

    def _get_slot_pos(self, index):
        col = index % 3
        row = index // 3
        return (self.origin_x + col * self.slot_size, 
                self.origin_y + row * self.slot_size)