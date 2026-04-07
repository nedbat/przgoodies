from dataclasses import dataclass

@dataclass
class Ball:
    x: int

    def __repr__(self):
        return "├" + "─"*self.x + "⌾" + "─"*(50-self.x) + "┤"

    def __matmul__(self, num): self.x = num     # obj @ num

    def __rshift__(self, num): self.x += num    # obj >> num
    def __lshift__(self, num): self.x -= num    # obj << num
