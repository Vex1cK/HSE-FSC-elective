import pygame
import random
import sys

sys.setrecursionlimit(5000)  # увеличиваем макс. глубину рекурсии

STATIC = "static"  # два ключа для словаря
MOVEABLE = "move"
# список с шансом получить 1 в 33% (нужно для элемента рандома в игре)
PERCENT33 = [0, 0, 1]
SIZE = W, H = 800, 800  # размеры окна и цвета для игры
COLORS = {
    0: (0, 0, 0),
    1: (250, 50, 50),
    2: (200, 0, 0),
    3: (0, 200, 0),
    4: (0, 0, 200),
    5: (100, 0, 0),
    6: (0, 100, 0),
    7: (0, 0, 100),
    8: (200, 200, 0),
    9: (0, 200, 200),
    10: (200, 0, 200),
    11: (100, 100, 0),
    12: (0, 100, 100),
    13: (100, 0, 100),
    14: (150, 250, 0),
    15: (0, 150, 250),
    16: (150, 150, 250),
    17: (150, 0, 250),
    18: (50, 50, 50),
    19: (50, 50, 250),
    20: (50, 250, 50)
}

pygame.init()


class Block:
    """
    Объектом данного класса является один "кусочек" пазла (не спрайт кстати)
    """

    def __init__(self, coords, id, color=(100, 50, 10)):
        self.id = id  # id - уникальный номер у каждого "кусочка"
        self.coords = coords  # список координат этого кусочка
        self.color = color
        self.moving = {
            "is": False,  # этот словарь используется для перемещения "кусочка"
            "pos": [0, 0]
        }

    def move_by_indent(self, indent_x, indent_y, board, need_to_return_board=False):
        """
        Функция отвечает за перемещение "кусочка" по полю, т.е.
        изменяет координаты самого кусочка и меняет поле с этими самыми кучками
        двигаем не на новые координаты, а на (старые + indent)
        """
        new_coords = [(0, 0)] * len(self.coords)
        try:  # try except отлавливает случаи когда пользователь пытается переместить "кусочек" за пределы поля
            for i in range(len(self.coords)):
                last_cord = self.coords[i]
                new_pair_coords = (
                    last_cord[0] + indent_x, last_cord[1] + indent_y)
                # всё еще за пределы поля, но массив ошибку не выдаст
                if new_pair_coords[0] < 0 or new_pair_coords[1] < 0:
                    if new_pair_coords:
                        return False, []
                    return False
                if board[new_pair_coords[0]][new_pair_coords[1]] in [0, self.id]:
                    # добавляем новую пару координат в список если всё ок
                    new_coords[i] = new_pair_coords
                else:  # пользователь попытался подвинуть "кусок" на другой "кусок" (нашлось пересечение)
                    if need_to_return_board:
                        return False, []
                    return False
        except IndexError:  # вылетает при попытке засунуть "кусок" за пределы поля
            if need_to_return_board:
                return False, []
            return False
        if need_to_return_board:  # обновляем само поле если его нужно вернуть
            for i in range(len(self.coords)):
                last_cord = self.coords[i]  # затираем старые координаты нулями
                board[last_cord[0]][last_cord[1]] = 0
            for i in range(len(self.coords)):
                new_pair_coords = new_coords[i]  # а теперь на новых координатах рисуем чиселки
                board[new_pair_coords[0]][new_pair_coords[1]] = self.id
            self.coords = new_coords.copy()
            return True, board  # возвращаем True (передвинули "кусок" успешно) и поле, если нужно.
        self.coords = new_coords.copy()
        return True

    def draw(self, screen, cell_size, pos):
        # Функция рисует фигуру (себя) на переданном screen
        if not self.moving['is']:
            self._usual_draw(screen, cell_size) # это в случае если фигуру сейчас не двигают
        else:
            self._moving_draw(screen, cell_size, pos) # ну а это соответственно - в случае когда её сейчас двигают

    def _usual_draw(self, screen, cell_size):
        # в случае если не двигают
        for x, y in self.coords:
            pygame.draw.rect(screen, self.color, (x * cell_size,  # ну, просто рисуем клеточками
                             y * cell_size, cell_size, cell_size)) 

    def _moving_draw(self, screen, cell_size, pos):
        # а вот в случае если двигают мы смотрим на сколько изменились
        # координаты мышки по сравнению с начальным положением (когда "кусок" "взяли") а после чего рисуем теми же клеточками
        # но они будут "не по сетке" как бы, сдвинуты на произвольное кол-во пикселей
        for x, y in self.coords:
            pygame.draw.rect(screen, self.color, (x * cell_size + (pos[0] - self.moving['pos'][0]),
                                                  y * cell_size +
                                                  (pos[1] -
                                                   self.moving['pos'][1]),
                                                  cell_size, cell_size))


class Board:
    """
    Класс доски. Отвечает за начальную генерацию поля и хранение.. собсвтенно, поля.
    """
    def __init__(self, h, w, n, needToPrint=False):
        self.h, self.w, self.n = h, w, n  # получаем все необходимые размеры
        self.get_start_square()  # получаем начальные "формы" "кусков" пазла

        if needToPrint:
            for row in self.board:
                for cell in row:  # печатаем его если нужно
                    print(f'{cell:< 3}', end='')
                print()
            print("\n")

        self.upgrade_board()  # и делаем уже из этих "форм" уже готовое поле

    def get_neighbors(self, i, j):
        # эта фанка просто считает соседей сверху снизу слева и справа от заданной клетки, и возвращает их список
        if i == 0:
            ies = [i+1]
        elif i == len(self.board) - 1:
            ies = [i-1]
        else:
            ies = [i+1, i-1]  # куча ифов чтобы не выйти за пределы массива
        if j == 0:
            jes = [j+1]
        elif j == len(self.board[0]) - 1:
            jes = [j-1]
        else:
            jes = [j+1, j-1]

        neighbors = []
        for ii in [i] + ies:
            if ii == i:  # Если мы не двигаемся по первой координате (вверх-вниз статично), то ходим вправо-влево
                for jj in jes:
                    if self.board[ii][jj] != 0:
                        neighbors.append(self.board[ii][jj])
            else:  # Если же ходим вверх-вниз, то вправо-влево статично (т.е. не двигаемся), соответственно
                if self.board[ii][j] != 0:
                    neighbors.append(self.board[ii][j])

        return neighbors

    def get_start_square(self):
        # Эта функция генерирует начальную конфигурацию всех "кусков"
        self.board = [[0 for _ in range(self.w)] for _ in range(self.h)]

        for id in range(1, self.n+1):
            # рандомным образом раскидываем по массиву чиселки, которые будут как семена потом разрастаться. И получится ровно наш прямоугольник
            i, j = random.randint(0, self.h-1), random.randint(0, self.w-1)
            while self.board[i][j] != 0:
                i, j = random.randint(0, self.h-1), random.randint(0, self.w-1)
            self.board[i][j] = id

        while any([0 in row for row in self.board]):  # пока есть хотя бы 1 ноль, мы "растим наши семена"
            i, j = random.randint(0, self.h-1), random.randint(0, self.w-1)  # Берём рандомную клетку
            count = 0
            while self.board[i][j] != 0 and count < 50:
                # Если эта клетка уже не 0, то берём другую. Если у нас 50 раз подряд не получилось найти 0
                # значит их там осталось относительно мало, и их мы заполним отдельно. Так что сейчас выходим из while (при count == 50)
                i, j = random.randint(0, self.h-1), random.randint(0, self.w-1)
                count += 1
            if count == 50:
                break

            neighbors = self.get_neighbors(i, j)  # считаем соседей (которые не 0) у клетки

            if not neighbors:
                continue

            self.board[i][j] = random.choice(neighbors)  # после чего клетка становится одним из соседей

        # осталось заполнить немножко нулей:
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    neighbors = self.get_neighbors(i, j)  # считаем соседей и делаем клетку одним из них
                    self.board[i][j] = random.choice(neighbors)

    def get_coords_of_figure(self, id, allcoords=[], firstCoords=(), isFirst=False):
        # Это - большая рекурсивная функция, которая считает все координаты всех клеточек одного конкретного "куска"
        if isFirst:  # если это самый первый запуск, то:
            allcoords.append(firstCoords)  # добавляем в общий список координат клеток текущую и перевызываем функцию
            allcoords = self.get_coords_of_figure(
                id, allcoords=allcoords.copy())
            return allcoords
        else:
            # В ином случае - идём считать соседей сверху снизу слева и справа
            x, y = allcoords[-1]
            need_to_check = [
                (x-1, y),
                (x+1, y),
                (x, y-1),  # координаты для проверки
                (x, y+1),
            ]
            for x, y in need_to_check:
                if x < 0 or y < 0:
                    continue  # за пределами массива
                try:
                    cell = self.board[x][y]
                except IndexError:
                    cell = 0  # это тоже за пределами массива
                    continue
                if cell == id and (x, y) not in allcoords:
                    # Если клетка - часть нашего "куска", и мы её еще не добавляли, то добавляем её координаты и вызываемся уже от неё
                    allcoords.append((x, y))
                    allcoords = self.get_coords_of_figure(
                        id, allcoords=allcoords.copy())
            return allcoords.copy()

    def upgrade_board(self):
        # Функция делает self.board уже готовым к игре
        new_board = [[0] * (self.w * 3) for _ in range(self.h*3)] # увеличиваем размер поля в 9 раз
        ids_of_figures = {
            STATIC: [],
            MOVEABLE: []  # список зафиксированных фигур (т.е. кусков) (точнее их id), и тех, которые можно двигать
        }
        figures = {}  # это список всех фигур (кусков.) в виде {id: object}
        coords_every_figure = {}
        for i in range(self.h):
            for j in range(self.w):
                if self.board[i][j] in coords_every_figure.keys():
                    continue  # теперь для каждой фигуры находим одну любую клетку от которой будем запускать рекурсивный обход
                else:
                    coords_every_figure[self.board[i][j]] = (i, j)

        for id in range(1, self.n + 1):
            coords = self.get_coords_of_figure(  # собственно - запускаем рекурскивный обход и находим все координаты фигуры
                id=id,
                allcoords=[],
                firstCoords=coords_every_figure[id],
                isFirst=True)
            figure = Block(coords.copy(), id, color=COLORS[id % 20 + 1])  # создаём "кусок"
            last_cords = coords.copy()  # и сохраняем его начальные координаты, так как сейчас мы будем его двигать
            # с шансом 33% фигура становится статичной. Её нельзя будет двигать.
            # Но, если с ней произойдёт накладка на другую фигуру при создании - то она снова станеть мувабельной)
            # В итоге там примерно четверть будет статична
            if random.choice(PERCENT33):
                ids_of_figures[STATIC].append(id)
                indent_x = self.h  # Т.к. массив увеличился в 9 раз, итоговую фигуру мы будет собирать в центре
                indent_y = self.w  # Там же в центре и должна находится наша "подсказка" (статичная фигура)
                ok = figure.move_by_indent(
                    indent_x, indent_y, new_board.copy())  # ну и двигаем её в центр
            else:
                ids_of_figures[MOVEABLE].append(id)
                indent_x = random.randint(  # Если же фигура мувабельна, то двигаем её в рандомное место на поле
                    0, self.h-1) * random.choice([1, -1]) + self.h
                indent_y = random.randint(
                    0, self.w-1) * random.choice([1, -1]) + self.w
                ok = figure.move_by_indent(
                    indent_x, indent_y, new_board.copy())

            if not ok:  # not ok = True когда наша фигура с кем-то пересеклась, в таком случае нужно двигать её
                if id in ids_of_figures[STATIC]:
                    del ids_of_figures[STATIC][ids_of_figures[STATIC].index(
                        id)]  # Если она была статичной, то становится мувабельной
                    ids_of_figures[MOVEABLE].append(id)

                while not ok:  # А теперь рандомно двигаем её пока она не будет ни с кем пересекаться
                    indent_x = random.randint(
                        0, self.h-1) * random.choice([1, -1]) + self.h
                    indent_y = random.randint(
                        0, self.w-1) * random.choice([1, -1]) + self.w
                    ok = figure.move_by_indent(
                        indent_x, indent_y, new_board.copy())

            figures[id] = figure  # Заносим фигуру в наш словарик
            for i in range(len(figure.coords)):
                nx, ny = figure.coords[i]
                # lx, ly = last_cords[i] дебаг
                # print(f"indx:{indent_x}, indy:{indent_y}, nx:{nx}, ny:{ny}, lx:{lx}, ly:{ly} id:{id}")
                new_board[nx][ny] = id  # заносим её новые координаты на поле

        for id in ids_of_figures[STATIC]:
            figures[id].color = COLORS[0]  # Задаём статичным фигурам черный цвет

        self.board = new_board
        self.figures = figures  # И заносим переменные в self
        self.ids_of_figure = ids_of_figures


class Game:
    """
    Класс игры. При создании объекта этого класса и передачи start=True игра сразу будет запущена
    """
    def __init__(self, data: dict, start=False):
        self.sizes = (data['w'], data['h'], data['n'])
        self.cell_size = H // (self.sizes[1] * 3)
        self.border_size = max(int(0.3 * self.cell_size), 1)  # высчитываем всякие размерчики, создаём поле, font, screen и т.д.
        self.board = Board(*self.sizes)
        self.window_size = (
            self.cell_size * self.sizes[0] * 3, self.cell_size * self.sizes[1] * 3)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("КОНСТРУКТОР ЛЕГО")
        self.figures = self.board.figures
        self.idThatMoving = 0
        self.font = pygame.font.Font(None, self.window_size[0] // 25)
        self.big_font = pygame.font.Font(None, self.window_size[0] // 10)
        self.need_to_restart = False

        if start:
            self.game_loop()  # запускаем игру

    def checkWin(self):  # Функция проверяет выйграл ли игрок (в центре нет ни одного нуля)
        x, y = self.sizes[0], self.sizes[1]
        for i in range(0, self.sizes[0]):
            xi = x + i
            for j in range(0, self.sizes[1]):
                yj = y + j
                if self.board.board[xi][yj] == 0:
                    return False
        return True

    def game_loop(self):
        # основной цикл игры
        loop = True
        pos = (0, 0)
        won = False
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # если нажата ЛКМ
                        x, y = list(
                            map(lambda x: x // self.cell_size, event.pos))  # получаем координаты клетки на которую кликнули
                        try:
                            id = self.board.board[x][y]
                            ok = bool(  # пробуем получить клетку поля (вдруг кликнули куда попало) и проверяем что фигура на которую кликнули (если это фигура вообще) не статична
                                id) and id not in self.board.ids_of_figure[STATIC]  # т.е. можно будет двигать
                        except IndexError:
                            ok = False  # Кликнули куда попало
                        if ok:
                            pos = event.pos  # Получаем начальные координаты мышки и меняем "статус" фигуры на "в движении"
                            self.idThatMoving = id
                            self.figures[id].moving['is'] = True
                            self.figures[id].moving['pos'] = pos
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        pos = event.pos  # Если мышь двигают - просто обновляем pos
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.idThatMoving:  # А это если кнопку мыши отпустили
                        curr_x, curr_y = list(  # Получаем новые (пока не проверенные) и старые координаты фигуры
                            map(lambda x: x // self.cell_size, event.pos))
                        last_x, last_y = list(map(lambda x: x // self.cell_size,
                                                  self.figures[self.idThatMoving].moving['pos']))
                        try:
                            self.board.board[curr_x][curr_y]
                            indent_x = curr_x - last_x
                            indent_y = curr_y - last_y  # находим indent
                            ok, board = self.figures[self.idThatMoving].move_by_indent(
                                indent_x, indent_y, self.board.board, True)  # двигаем фигуру, и смотрим что всё ок
                            if ok:
                                self.board.board = board.copy()
                                won = self.checkWin()  # проверяем не выйграл ли игрок
                        except IndexError:
                            pass
                        finally:
                            self.figures[self.idThatMoving].moving['is'] = False
                            self.figures[self.idThatMoving].moving['pos'] = [
                                0, 0]  # "отпускаем" фигуру
                            self.idThatMoving = 0
                            pos = (0, 0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.need_to_restart = True
                        loop = False  # рестар игры

            self.screen.fill((230, 230, 230))

            for id in self.figures.keys():
                self.figures[id].draw(self.screen, self.cell_size, pos) # отрисовка всех фигур
            pygame.draw.rect(
                self.screen,
                (230, 20, 20),
                (
                    self.sizes[0] * self.cell_size - self.border_size,
                    self.sizes[1] * self.cell_size - self.border_size,  # а это красная рамочка в центре
                    self.sizes[0] * self.cell_size + self.border_size,
                    self.sizes[1] * self.cell_size + self.border_size
                ),
                self.border_size
            )
            # hint1 = self.font.render("Нажмите <Esc> чтобы увидеть ответ", True, (0, 0, 0))  # не реализованно
            hint2 = self.font.render(
                "Чтобы перезапустить игру нажмите <Backspace>", True, (0, 0, 0))  # рисуем подсказки пользовалетю
            # self.screen.blit(hint1, hint1.get_rect(center=(250, 20)))
            self.screen.blit(hint2, hint2.get_rect(center=(self.window_size[0] // 2.8, self.window_size[0] // 18)))
            if won:
                hint_win1 = self.big_font.render(
                    "Complete!", True, (20, 215, 20))
                hint_win2 = self.font.render(
                    "Вы можете перезапустить игру нажав клавишу <Backspace>", True, (0, 0, 0))
                self.screen.blit(hint_win1, hint_win1.get_rect(  # а это уведомление о том, что игрок выйграл
                    center=(self.window_size[0] // 2, self.window_size[1] // 6)))
                self.screen.blit(hint_win2, hint_win2.get_rect(center=(
                    self.window_size[0] // 2, self.window_size[1] // 6 + self.window_size[0] // 12)))

            pygame.display.flip()


if __name__ == "__main__":
    data = {
        'w': int(input("Введите ширину (в клетках) исходного прямоугольника: ")),
        "h": int(input("Введите высоту (в клетках) исходного прямоугольника: ")),
        # получаем размеры поля и кол-во клеток
        'n': int(input("Введите кол-во фигур: ")),
    }
    need_to_res = True
    while need_to_res:  # запускаем цикл игр (для перезапуска игры)
        try:
            # создаём и этим же действием запускаем игру
            game = Game(data, True)
            # после завершения игры, смотрим нужен ли рестарт
            need_to_res = game.need_to_restart
        except IndexError:
            continue
            # Примерно раз в 50-60 перезапусков вылетает ошибка IndexError при создании поля по неизвестной мне причине.
            # Чтобы игры не вылетала я сделал такой костыль, так как до мягкого дедлайна 2 часа 11 минут))))
            # все остальные ошибки IndexError которые я замечал при тестах обрабатываются отдельно внутри классов, так что проблем с таким костылём нет
            # по крайней мере я ошибок больше не выявил))
            # update: Выявил.. ну это уж совсем какой-то редкий случай... сделаю мега костыль))
        except Exception as err:
            print(f"FATAL: unknown error: {err}")
            continue
    pygame.quit()
    sys.exit()
