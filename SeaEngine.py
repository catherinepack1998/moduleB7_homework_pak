class Dot:
    """makes dot on game board."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    """makes ship on game board:
     bow get object.Dot;
     length = length of ship, length == ship lives;
     o - give "1" if you want make ship on x axis , or "0" for y axis."""
    def __init__(self, bow, length, o):
        self.bow = bow
        self.length = length
        self.o = o
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shoten(self, shot):
        return shot in self.dots


