from random import randint

class BoardExeption(Exception):
    pass

class BoardOutExeption(BoardExeption):

    def __str__(self):
        return "Вы пытались выстрелить за игровое поле!"

class BoartUsedExeption(BoardExeption):

    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardWrongShipExeption(BoardExeption):
    def __str__(self):
        return "Не правильно распологаете корабль!"

class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # метод отвечающий за сравнеие двух объектов
       return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Dot({self.x},{self.y})"


class Ship:

    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property  # Описывает свойства карабля
    def dots(self):

        ship_dots = []

        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):

        return shot in self.dots

class Board:

    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.cound = 0
        self.field = [["0"] * size for _ in range(size)]
        self.busy = []
        self.ship = []

    def __str__(self):

        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"

        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("#", "0")

        return res
    def out(self, d):

        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))
    def contour(self, ship, verb=False):

        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:

            for dx, dy in near:

                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:

                    if verb:
                        self.field[cur.x][cur.y] = "."

                    self.busy.append(cur)
    def add_ship(self, ship):

        for d in ship.dots:

            if self.out(d) or d in self.busy:
                raise BoardWrongShipExeption()

        for d in ship.dots:
            self.field[d.x][d.y] = "#"
            self.busy.append(d)

        self.ship.append(ship)
        self.contour(ship)

    def shot(self, d):

        if self.out(d):
            raise BoardOutExeption()

        if d in self.busy:
            raise BoartUsedExeption()

        self.busy.append(d)

        for ship in self.ship:

            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "x"

                if ship.lives == 0:
                    self.cound += 1
                    self.contour(ship, verb=True)
                    print("Карабль уничтожен!")

                    return False

                else:

                    print("Карабль ранен!")

                    return True

        self.field[d.x][d.y] = "."

        print("Мимо!")

        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.cound == len(self.ship)

class Plyer:

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

            except BoardExeption as e:
                print(e)

class AI(Plyer):

    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"следующий ход делает компьтер:{d.x + 1} {d.y + 1}")
        return d


class User(Plyer):

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

            return Dot(x - 1, y - 1)

class Game:

    def __init__(self, size=6):

        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):

        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0

        for l in lens:

            while True:

                attempts += 1

                if attempts > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))

                try:
                    board.add_ship(ship)
                    break

                except BoardWrongShipExeption:

                    pass
        board.begin()
        return board

    def random_board(self):

        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("____________________________________")
        print("Приветствуем Вас в игре Морской бой!")
        print("____________________________________")
        print("  расположение кораблей по х и у    ")
        print("_х- номер строки и _у-номер столбца ")

    def print_boards(self):
        print("-" * 20)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 20)
        print("Доска комрьютера:")
        print(self.ai.board)
        print("-" * 20)

    @staticmethod
    def hstack(first, second):
        first_sp = first.split("\n")
        second_sp = second.split("\n")
        max_width = max(map(len, first_sp))
        max_len = max(len(first_sp),len(second_sp))
        first_sp += [""] * (max_len - len(first_sp))
        second_sp += [""] * (max_len - len(second_sp))
        text = []
        for f, s in zip(first_sp, second_sp):
            text.append(f"{f: <{max_width}}   |:|   {s: <{max_width}}")

        return "\n".join(text)


    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            user_board = "Доска пользователя:\n\n" + str(self.us.board)
            ai_board = "Доска компьютера:\n\n" + str(self.ai.board)

            print(self.hstack(user_board, ai_board))


            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                print("-" * 20)
                print("Компьютер выиграл!")
                break
                num += 1


    def start(self):
        self.greet()
        self.loop()
ny = Game()
ny.start()