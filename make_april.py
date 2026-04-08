from cagedprompt import prompt_session

from dataclasses import dataclass

@dataclass
class Ball:
    x: int

    def __repr__(self):
        return "├" + "─"*self.x + "⌾" + "─"*(50-self.x) + "┤"

    def __matmul__(self, num):
        # obj @ num
        self.x = num

    def __rshift__(self, num):
        # obj >> num
        self.x += num   

    def __lshift__(self, num): 
        # obj << num
        self.x -= num    


print(prompt_session("""\
# one
b = Ball(10)
b

# two
b.x = 20
b

# three
b = Ball(45)
b

b @ 5
b

b @ 30
b
###

# four
b = Ball(10)
b >> 15
b

# five
b = Ball(45)
for dx in range(9):
    b << dx
    print(b)

""",
globals=globals(),
))
