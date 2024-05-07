import pygame
import sys

# константы и переменные
cell_size = 20
width = 1000
height = 600
rows = height // cell_size
cols = width // cell_size
rule = 1  # id current правила
RULES = {
    1: {
        'survive': [2, 3],
        'birth': [3]
    },
    2: {
        'survive': [3, 4],
        'birth': [4]
    },
    3: {
        'survive': [1, 2],
        'birth': [2]
    }
}
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (23, 22, 21)
TEXT_COLOR = (255, 255, 255)
TEXT_COLOR2 = (20, 50, 20)
ERROR_COLOR = (200, 0, 0)
BORDER_COLOR = (150, 150, 150)
CELL_COLOR = (20, 180, 20)
FPS = 10

# Инициализация PyGame
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Игра Жизнь")

# Создание поля и шрифта для текста
field = [[0 for _ in range(cols)] for _ in range(rows)]
font = pygame.font.Font(None, 36)

def count_neighbors(x, y, field):
    """
    Эта функция считает кол-во соседей рядом с клеткой координаты которой подаются на вход
    """
    neighbors = 0  # Счетчик
    for dx in [-1, 0, 1]:  # отступы во все стороны
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:  # Себя не считаем
                continue
            if 0 <= x + dx < cols and 0 <= y + dy < rows and field[y + dy][x + dx]:
                neighbors += 1  # нашли соседа
    return neighbors

def update_field(field):
    """
    Эта функция переводит данное ей поле "на следующий ход"
    в соответствии с действующим правилом, номер которого хранится в rule
    """
    global rule
    survive, birth = RULES[rule]['survive'], RULES[rule]['birth']  # достаём правило 
    new_field = [[0 for _ in range(cols)] for _ in range(rows)]  # делаем новое поле

    for y, row in enumerate(field):
        for x, cell in enumerate(row):

            neighbors = count_neighbors(x, y, field)  # считаем соседей

            if cell:
                if neighbors in survive:
                    new_field[y][x] = 1  # клетка выжила
            else:
                if neighbors in birth:
                    new_field[y][x] = 1  # клетка родилась
            # В остальных случаях клетка мертва - оставляем ноль
            
    return new_field

def draw_field(field):
    """
    Эта функция полностью отрисовывает поле
    """
    screen.fill((220, 220, 220))
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell: # если клетка жива то рисуем её зелёненьким
                pygame.draw.rect(screen, CELL_COLOR, (x * cell_size, y * cell_size, cell_size, cell_size))

def field_update_after_window(last_field):
    """
    Функция меняет размер поля
    Размер нового может быть либо меньше либо больше начального (ну или равно)

    Если больше исходного (увеличили размер окна / уменьшили размер клетки и т.д.), то старые элементы помещаются
    в центр путём использования отступов от краёв нового (большего) массива
    
    Если меньше исходного (уменьшили размер окна / увеличили размер клетки и т.д.), то остальные элементы "вырезаются", остаются только те,
    что помещаются на экран.

    размерность нового поля будет отличаться когда будут меняться глобальные переменные rows и cols
    """

    global rows, cols
    new_field = [[0 for _ in range(cols)] for _ in range(rows)]  # новое поле
    lastRows = len(last_field)
    lastCols = len(last_field[0])
    newRows = len(new_field)
    newCols = len(new_field[0])

    minCountRows = min(lastRows, newRows)  # Смотрим кто больше, исходное поле или новое
    minCountCols = min(lastCols, newCols)
    maxCountRows = max(lastRows, newRows)
    maxCountCols = max(lastCols, newCols)

    newRowsMore = (newRows > lastRows)  # Булевая переменная 
    newColsMore = (newCols > lastCols)

    indent_i = ((maxCountRows - minCountRows) // 2)  # высчитываем отступ от краёв массива
    indent_j = ((maxCountCols - minCountCols) // 2)

    for i in range(minCountRows):
        for j in range(minCountCols):
            i_new = i + indent_i * newRowsMore
            j_new = j + indent_j * newColsMore  # координаты клеток с учетом отступа и наибольшего поля

            i_last = i + indent_i * (not newRowsMore)
            j_last = j + indent_j * (not newColsMore)

            new_field[i_new][j_new] = last_field[i_last][j_last]  # берём клеточку
    
    return new_field

def manual(field):
    """
    Эта функция - окно.
    Конкретно окно в котором описаны правила (1, 2 и 3)
    """

    global screen, rows, cols, cell_size, width, height
    running = True

    texts1 = ["Правило 1:", "Правило 2:", "Правило 3:"]  #  текст можно отрендерить 1 раз, т.к. он не меняется
    texts2 = ["B3/S23 (Баланс)", "B4/S34 (Быстрое вымирание)", "B2/S12 (Быстрое размножение)"]
    texts3 = ["Чтобы выйти нажмите <Esc>", "B - кол-во соседей при которых клетка рождается", "S - кол-во соседей при которых клетка выживает"]

    texts1 = list(map(lambda x: font.render(x, True, TEXT_COLOR), texts1))
    texts2 = list(map(lambda x: font.render(x, True, TEXT_COLOR), texts2))
    texts3 = list(map(lambda x: font.render(x, True, TEXT_COLOR), texts3))

    rects1 = []
    rects2 = []
    rects3 = []

    rects1.append(texts1[0].get_rect(center=(150, 90)))
    rects1.append(texts1[0].get_rect(center=(150, 240)))
    rects1.append(texts1[0].get_rect(center=(150, 390)))

    rects2.append(texts2[0].get_rect(center=(179, 135)))
    rects2.append(texts2[1].get_rect(center=(258, 285)))
    rects2.append(texts2[2].get_rect(center=(271, 435)))

    rects3.append(texts3[0].get_rect(center=(200, 20)))
    rects3.append(texts3[1].get_rect(center=(680, 70)))
    rects3.append(texts3[2].get_rect(center=(675, 120)))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # выходим
            elif event.type == pygame.VIDEORESIZE:
                """
                поменяли размер окна, а значит потенциально сейчас на экране помещается
                больше/меньше клеток, и размер поля нужно менять, что мы и делаем
                """
                window_size = event.size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                width = window_size[0]
                height = window_size[1]
                rows = height // cell_size
                cols = width // cell_size
                field = field_update_after_window(field)

        screen.fill(BACKGROUND_COLOR)

        for i in range(len(texts1)):
            screen.blit(texts1[i], rects1[i])
        for i in range(len(texts2)):
            screen.blit(texts2[i], rects2[i])
        for i in range(len(texts3)):  # отрисовка текста
            screen.blit(texts3[i], rects3[i])

        pygame.display.flip()

    return field

def get_new_rules(field):
    """
    Эта функция - окно
    Конкретно - окно с выбором правил.
    """
    global rule, screen, rows, cols, cell_size, width, height
    option_active = True
    curr_rule = rule

    while option_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                """
                Проверяем куда нажал пользователь и в соответствии с
                этим меняет curr_rule на новое значение
                """
                mouse_pos = pygame.mouse.get_pos()
                if rule1_rect.collidepoint(mouse_pos):
                    curr_rule = 1
                elif rule2_rect.collidepoint(mouse_pos):
                    curr_rule = 2
                elif rule3_rect.collidepoint(mouse_pos):
                    curr_rule = 3
                elif save_rect.collidepoint(mouse_pos):
                    rule = curr_rule
                    option_active = False
                elif manual_rect.collidepoint(mouse_pos):
                    field = manual(field)  # пользователь открыл окно с описаниями правил
            elif event.type == pygame.VIDEORESIZE:
                """
                поменяли размер окна, а значит потенциально сейчас на экране помещается
                больше/меньше клеток, и размер поля нужно менять, что мы и делаем
                """
                window_size = event.size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                width = window_size[0]
                height = window_size[1]
                rows = height // cell_size
                cols = width // cell_size
                field = field_update_after_window(field)

        screen.fill(BACKGROUND_COLOR)

        text = font.render("Choose an option:", True, TEXT_COLOR)
        rule1_text = font.render("Правило 1", True, TEXT_COLOR)
        rule2_text = font.render("Правило 2", True, TEXT_COLOR)
        rule3_text = font.render("Правило 3", True, TEXT_COLOR)
        manual_text = font.render("Открыть описание правил", True, TEXT_COLOR)
        save_text = font.render("Сохранить", True, TEXT_COLOR)

        rule1_rect = rule1_text.get_rect(center=(450, 150))
        rule2_rect = rule2_text.get_rect(center=(450, 200))
        rule3_rect = rule3_text.get_rect(center=(450, 250))
        manual_rect = manual_text.get_rect(center=(450, 300))
        save_rect = save_text.get_rect(center=(450, 350))
        rect_text = text.get_rect(center=(450, 100))  # отрисовка целой кучи текста

        screen.blit(text, rect_text)
        screen.blit(rule1_text, rule1_rect)
        screen.blit(rule2_text, rule2_rect)
        screen.blit(rule3_text, rule3_rect)
        screen.blit(manual_text, manual_rect)
        screen.blit(save_text, save_rect)

        pygame.draw.rect(screen, WHITE, (350, 140, 20, 20), 2)
        pygame.draw.rect(screen, WHITE, (350, 190, 20, 20), 2)
        pygame.draw.rect(screen, WHITE, (350, 240, 20, 20), 2)
        pygame.draw.rect(screen, WHITE, (354, 94 + (50 * curr_rule), 12, 12))

        pygame.display.flip()
    return field

def get_new_cell_size(field, question="Введите новый размер клетки: ", changeField=True):
    """
    Эта функция - окно
    Конкретно - окно с вводом нового размера клетки
    """
    global screen, rows, cols, cell_size, width, height
    input_active = True
    text = ""
    err = ""
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    input_active = False  # выходим обратно в меню без изменений размера
                    return -1, field
                if event.key == pygame.K_RETURN:
                    if text.isdigit():  # проверяем че там ввел пользователь
                        cell_size_got = int(text)
                        if 5 <= cell_size_got <= 50:
                            input_active = False
                            err = ""
                            if changeField:  # если нужно менять поле - меняем
                                cell_size = cell_size_got
                                rows = height // cell_size
                                cols = width // cell_size
                                field = field_update_after_window(field)
                        elif cell_size_got < 5:
                            err = "Число слишком маленькое! Введите число от 5 до 50."
                        elif cell_size_got > 50:
                            err = "Число слишком большое! Введите число от 5 до 50."
                    else:  # пишем пользователю че не так
                        err = "Это вообще не натуральное число! Введите число от 5 до 50."
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            elif event.type == pygame.VIDEORESIZE:
                """
                поменяли размер окна, а значит потенциально сейчас на экране помещается
                больше/меньше клеток, и размер поля нужно менять, что мы и делаем
                """
                window_size = event.size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                width = window_size[0]
                height = window_size[1]
                rows = height // cell_size
                cols = width // cell_size
                field = field_update_after_window(field)
                

        # Очистка экрана
        screen.fill(BACKGROUND_COLOR)

        # Отрисовка ввода  и текста, если нужно, то сообщения об ошибке
        input_text = font.render(question + text, True, TEXT_COLOR)
        curr_text = font.render(f"Текущий размер клетки: {cell_size}", True, TEXT_COLOR)
        err_text = font.render(err, True, ERROR_COLOR)
        txt = font.render("Чтобы выйти нажмите <Esc>", True, TEXT_COLOR)
        screen.blit(txt, txt.get_rect(center=(200, 20)))
        screen.blit(input_text, (40, 130))
        screen.blit(curr_text, (40, 160))
        screen.blit(err_text, (40, 190))
        pygame.draw.rect(screen, BORDER_COLOR, (35, 125, input_text.get_size()[0] + 16, 30), 2)

        # Обновление экрана
        pygame.display.flip()
    
    return cell_size_got, field

def menu(field):
    """
    Эта функция - окно
    Конкретно - окно меню
    """
    global screen, rows, cols, cell_size, width, height, rule
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                """
                Смотрим куда там пользователь нажал
                """
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    running = False
                elif rules_rect.collidepoint(mouse_pos):
                    field = get_new_rules(field)
                elif size_rect.collidepoint(mouse_pos):
                    res, field = get_new_cell_size(field)
                    if res != -1:  # res = -1 когда пользователь вышел из окна с изменением размера клетки через esc
                        running = False
            elif event.type == pygame.VIDEORESIZE:
                """
                поменяли размер окна, а значит потенциально сейчас на экране помещается
                больше/меньше клеток, и размер поля нужно менять, что мы и делаем
                """
                window_size = event.size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                width = window_size[0]
                height = window_size[1]
                rows = height // cell_size
                cols = width // cell_size
                field = field_update_after_window(field)

        screen.fill(BACKGROUND_COLOR)

        # Отрисовка выборов меню
        play_text = font.render("Играть", True, TEXT_COLOR)
        rules_text = font.render("Настроить правила игры", True, TEXT_COLOR)
        size_text = font.render("Настроить размер клетки", True, TEXT_COLOR)

        # Положение текста
        play_rect = play_text.get_rect(center=(500, 200))
        rules_rect = rules_text.get_rect(center=(500, 250))
        size_rect = size_text.get_rect(center=(500, 300))

        # Отрисовка текста
        screen.blit(play_text, play_rect)
        screen.blit(rules_text, rules_rect)
        screen.blit(size_text, size_rect)

        # Обновление экрана
        pygame.display.flip()
    return field

def config_field(field):
    """
    Эта функция отвечает за режим паузы в игре, когда можно "рисовать клетками"
    """
    global screen, rows, cols, cell_size, width, height

    def change(event, field, coords_changes, mode):
        """
        Эта подфункция меняет клетку на нужное значение
        Если лкм - на 1
        Если пкм - на 0
        И также она учитывает ситуацию, когда пользователь зажал кнопку мыши и как бы рисует
        Эта функция не допускает больше одного изменения одной и той же клетки на время "одного зажима"
        """
        global cell_size
        x, y = event.pos

        if x < 0 or y < 0:
            return field, coords_changes  # пользователь вышел за края экрана
        
        i, j = x // cell_size, y // cell_size

        if (i, j) not in coords_changes:  # Если эту клетку еще не изменяли
            try:
                field[j][i] = mode
                coords_changes.append((i, j))
            except IndexError:  # пользователь вышел за края экрана
                coords_changes.append((i, j))
        return field, coords_changes
    
    coords_changes = []  # тут будем хранить "историю" изменения клеток
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                """
                Тут обрабатывается нажатие как таковое, на кнопку мыши
                """
                if event.button == 1:  # Левая кнопка мыши
                    field, coords_changes = change(event, field, coords_changes, 1)  # рисуем
                elif event.button == 3:  # Правая кнопка мыши
                    field, coords_changes = change(event, field, coords_changes, 0)  # стираем
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Если левая кнопка мыши зажата
                    field, coords_changes = change(event, field, coords_changes, 1)  # рисуем
                elif pygame.mouse.get_pressed()[2]:  # Если правая кнопка мыши зажата
                    field, coords_changes = change(event, field, coords_changes, 0)  # стираем
                else:
                    coords_changes = []  # Если ни лкм ни пкм не ЗАЖАТЫ, то обновляем "историю"
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # кнопку мыши "отжали" (антоним к нажали типа) - очищаем "историю"
                    coords_changes = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # переход обратно в main
                if event.key == pygame.K_ESCAPE:
                    field = menu(field)  # выход в меню
            elif event.type == pygame.VIDEORESIZE:
                """
                поменяли размер окна, а значит потенциально сейчас на экране помещается
                больше/меньше клеток, и размер поля нужно менять, что мы и делаем
                """
                window_size = event.size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                width = window_size[0]
                height = window_size[1]
                rows = height // cell_size
                cols = width // cell_size
                field = field_update_after_window(field)

        draw_field(field)
        
        hint1 = font.render("Для выхода в меню нажмите <Esc>", True, TEXT_COLOR2)
        hint2 = font.render("Для запуска <Return> (Enter)", True, TEXT_COLOR2)  # рисуем подсказки
        screen.blit(hint1, hint1.get_rect(center=(250, 20)))
        screen.blit(hint2, hint2.get_rect(center=(250, 40)))

        pygame.display.flip()
    return field

def main(last_field):
    """
    В этой функции находится основной цикл игры
    """
    global screen, rows, cols, cell_size, width, height

    # Основной игровой цикл
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    last_field = menu(last_field)  # выход в меню
                elif event.key == pygame.K_SPACE:
                    last_field = config_field(last_field)  # пауза
            elif event.type == pygame.VIDEORESIZE:
                """
                поменяли размер окна, а значит потенциально сейчас на экране помещается
                больше/меньше клеток, и размер поля нужно менять, что мы и делаем
                """
                window_size = event.size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                width = window_size[0]
                height = window_size[1]
                rows = height // cell_size
                cols = width // cell_size
                last_field = field_update_after_window(last_field)


        # Обновление и отрисовка поля
        new_field = update_field(last_field)
        draw_field(new_field)
        last_field = new_field

        hint1 = font.render("Для выхода в меню нажмите <Esc>", True, TEXT_COLOR2)
        hint2 = font.render("Для паузы <Space> (пробел)", True, TEXT_COLOR2)
        screen.blit(hint1, hint1.get_rect(center=(250, 20)))  # и отрисовка хинтов
        screen.blit(hint2, hint2.get_rect(center=(250, 40)))

        pygame.display.flip()
        clock.tick(FPS)  # Задержка для контроля скорости обновления


    pygame.quit()
    return 0

if __name__ == "__main__":  # правило хорошего тона
    field = config_field(field)  # в начале настраиваем конфигурацию поля
    main(field)  # а вот теперь уже запускаем main
    pygame.quit()  # выхоооооооооооооодим
    sys.exit()