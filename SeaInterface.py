from random import randint

from SeaEngine import *
from Exception import *
class Board:
    """makes game board.
    count - describes sunk ship
    busy - list with created Dot
    ships - list with Ships on board
    """
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")

        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):#makes contour of ship
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongSheepException()

        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен")
                    return False
                else:
                    print("Попадание по кораблю!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} , {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)
            return Dot(x-1, y-1)


class Game:
    def __init__(self):
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, 6), randint(0, 6)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongSheepException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        txt = ""
        txt_2 = "Приветствуем вас"
        txt_3 = "в игре"
        txt_4 = "морской бой"
        txt_5 = "формат ввода: x y"
        txt_6 = " x - номер строки"
        txt_7 = " y - номер столбца"
        print(f"{txt:-^30}\n"
              f"{txt_2:^30}\n"
              f"{txt_3:^30}\n"
              f"{txt_4:^30}\n"
              f"{txt:-^30}\n"
              f"{txt_5:^30}\n"
              f"{txt_6:^30}\n"
              f"{txt_7:^30}")

    def loop(self):
        num = 0
        while True:
            print("-"*30)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*30)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-"*30)

            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()

            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-"*30)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-"*30)
                print("Компьютер выиграл!")
                break
            num += 1
    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    g = Game()
    g.start()
