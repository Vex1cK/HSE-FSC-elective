from copy import deepcopy

# Переменная с игровым полем
N = 3 # Кол-во строк поля
M = 3 # Кол-во столбцов у поля
board = [[" " for _ in range(M)] for _ in range(N)] # Поле 3х3 | " " - пусто; "x" - крестик; "o" - нолик
# немножко других переменных и констант
MAIN = 'main'  
NEXT = 'next'
letters = ['A', "B", "C"]
numbers = ['1', '2', '3']
allFlags = ['g1', 'g2', 'g3', 'v1', 'v2', 'v3', 'd1', 'd2']
lettersToIndex = {
    "A": 0,
    "B": 1,
    "C": 2
}
varsOfPositionToCheck = {
    '00': ['g1', 'v1', 'd1'],
    '01': ['g1', 'v2'],
    '02': ['g1', 'v3', 'd2'],

    '10': ['g2', 'v1'],
    '11': ['g2', 'v2', 'd1', 'd2'],
    '12': ['g2', 'v3'],

    '20': ['v1', 'g3', 'd2'],
    '21': ['v2', 'g3'],
    '22': ['v3', 'g3', 'd1'],
}
cords = {
    'g1': [(0, 0), (0, 1), (0, 2)],
    'g2': [(1, 0), (1, 1), (1, 2)],
    'g3': [(2, 0), (2, 1), (2, 2)],

    'v1': [(0, 0), (1, 0), (2, 0)],
    'v2': [(0, 1), (1, 1), (2, 1)],
    'v3': [(0, 2), (1, 2), (2, 2)],

    'd1': [(0, 0), (1, 1), (2, 2)],
    'd2': [(0, 2), (1, 1), (2, 0)],
}
manualMain = {
    1: [  # Структура такая, т.к. иструкция выводится справа от поля
        '',  # И только такой порядок строк в списках позволяет удобно выводить
        # Инструкцию в цикле вместе с полем
        'Первые ходят крестики | Регистр неважен',
        'Примеры ввода команды:'
       ],
    2: [
        '',
        'Введите "{Буква} {Цифра}" для совершения хода, через пробел или слитно,',
        'Ваш ход: B 3'
       ],
    3: [
        'Инструкция к игре в обычном режиме:',
        'на указанную вами клетку | Введите "-v" или "выход" для завершения игры',
        'Ваш ход: выход'
       ]
}
manualNext = {
    1: [  # Такая же инструкция но для второго режима игры
        'Инструкция для настройки поля:',
        'Крестик - "х" - может быть как из латинского алфафита, так и из кирилицы',
        '"del {Буква} {Цифра}"'
       ],
    2: [
        'Чтобы поставить крестик/нолик в клетку введите:',
        'Нолик - "о" - может быть как из латинского алфафита, так и из кирилицы, а также цифрой 0',
        'Буква цифра и знак обязательно должны вводиться через пробел.'
       ],
    3: [
        '"{Буква} {Цифра} {Знак (нолик или крестик)}"',
        'Чтобы убрать крестик/нолик из клетки введите:',
        'Для завершения настройки введите: "done", а для выхода: "выход" или "-v"'
       ]
}

def printBoard(board, mode):
    # Если поменять размер поля, вывод будет кривой)
    # Функция расчитана на вывод стандартного поля 3х3
    if mode == MAIN:  # Выводится поле игры и инструкция справа от поля
        # Рабоает - не трогай
        # Выглядит страшновато, то ничего кроме красивого вывода здесь нет
        manual = manualMain
    elif mode == NEXT:
        manual = manualNext
    print("\n\n       " + "1" + " " * 7 + "2" + " " * 7 + "3" + " " * 7)
    print("   ", "_" * 25, sep='')
    for i in range(3):
        print("   |" + "       |" * 3 + (" " * 10 + manual[1][i]))
        print(f" {letters[i]} |", end='')
        for j in range(3):
            print(f"   {board[i][j]}   |", end='')
        print(f"{(' ' * 10 + manual[2][i])}")
        print("   |" + "_______|" * 3 + " " * 10 + manual[3][i])
    print()

def correctInput1(move):
    """
    Данная функция проверяет корректность введённой команды
    для обычного режима игры (функция main)
    условия правильного ввода выводятся пользователю на экран при игре
    """
    if move[0].upper() in letters:  
        if move[1] in numbers:
            move[0] = move[0].upper()
            move = (lettersToIndex[move[0]], int(move[1]) - 1)
            if board[move[0]][move[1]] == " ":
                return move, True
            else:
                print("Это место уже занято! выберите другую клетку для хода")
        else:
            print("Некорректный ввод числа!")
    else:
        print("Некорректный ввод буквы!")
    return [], False

def correctInput2(got):
    # Цель та же что и у correctInput1, только работает для функции boardSetup, а не main
    if got[0] == 'del':
        l = 1
        n = 2
        s = None
    else:
        l = 0
        n = 1
        s = 2
    if got[l].upper() in letters:  
        if got[n] in numbers:
            got[l] = lettersToIndex[got[l].upper()]
            got[n] = int(got[n]) - 1
            if s:
                got[s] = 'x' if got[s] in ['x', 'х'] else 'o'
            if board[got[l]][got[n]] == " " and s:
                return got, True
            elif board[got[l]][got[n]] != " " and not s:
                return got, True
            else:
                if s:
                    print(f'На этом месте уже стоит {"крестик" if got[s] == "o" else "крестик"}.')
                else:
                    print("на этой клетке ничего нет, нечего удалять")
        else:
            print("Некорректный ввод числа!")
    else:
        print("Некорректный ввод буквы!")
    return [], False

def isBoardOk(board):
    # Эта функция проверяем конфигурацию доски, которую настраивает пользователь, на правильность
    # т.е. если ситуация которая получилась у пользователя не может возникнуть в реальной игре - вернётся False. И наоборот
    nolikCount = 0
    krestikCount = 0
    noneCount = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'o':
                nolikCount += 1
            elif board[i][j] == 'x':
                krestikCount += 1
            elif board[i][j] == ' ':
                noneCount += 1
    if abs(nolikCount - krestikCount) >= 2:  # разница в кол-ве знаков
        print("Неверное кол-во крестиков и ноликов на поле (разница в их кол-ве больше двух),")
        print('Такого случая в игре возникнуть не может!')
        return False, 0, 0
    if nolikCount - krestikCount > 0:  # такое может быть только если нолики ходят первые. А у нас крестики - это прописано в иструкции к игре
        print("Ноликов на поле больше чем крестиков,")
        print('Такого случая в игре возникнуть не может!')
        return False, 0, 0
    if noneCount == 0:  # Не осталось пустых клеток
        print("на поле не осталось свободных клеток! Нужно чтобы было хотя бы одно свободное место")
        return False, 0, 0
    return True, krestikCount - nolikCount, noneCount

def didSmOneWin(board, flags, needChar=False):
    # Функция проверяет есть ли победитель на поле, верёнт True если да, False в остальных случаях.
    # Также при переданном needChar - True - вернёт знак победителя ("x" или "o"), в остальных случаях вернёт пустую строку
    for flag in flags:
        cordsNeedToCheck = cords[flag]
        ok = True
        char = board[cordsNeedToCheck[0][0]][cordsNeedToCheck[0][1]]
        if char == ' ':
            continue
        for x, y in cordsNeedToCheck:
            if board[x][y] == char:
                continue
            ok = False
            break
        if ok:
            if needChar:
                return True, char
            return True
    if needChar:
        return False, ""
    return False

def printManualNext():
    # просто печатаем иструкцию к режиму с определением следующего наилучшего хода
    print('================================================================================================')
    print("Хорошо, вот полная инструкция к режиму:")
    print("Dам нужно будет настроить поле, т.е. определить")
    print("Начальное состояние всех клеток, например на а1 будет нолик, на а2 крестик")
    print("И нужно будет найти лучший следующих ход из этого положения.")
    print("Для настройки поля, справа от него будет инструкция по использованию команд, ")
    print("Вы сможете ставить крестики и нолики на поле в любом порядке, а также удалять их с поля")
    print('После завершения настройки нужно будет ввести специальную команду,')
    print("И если поле настроенно корректно, то программа напишет для вас следующий оптимальный ход")
    print("В случае, если на поле есть ошибки, например все поля заполнены, или на поле только крестики,")
    print("То программа сообщит об этом. Конец инструкции.")
    print("Считается, что первыми ходили крестики. Т.е. ноликов не может быть больше чем крестиков на поле.")
    print('================================================================================================')

def boardSetup():
    # эта функция - первая часть режима с определением лучшего следующего хода
    # здесь происходит настройка пользователем конфигурации доски
    # Вывод иструкции к режиму если нужно
    print('Нужно ли вывести для вас полную иструкцию к этому режиму?')
    print('Введите "да" или "1" если нужно и "нет" или "0" если не нужно')
    needManual = input("Ввод: ")
    print()
    while needManual.lower() not in ['да', 'нет', '0', "1"]:
        print("Некорректный ввод, попробуйте еще раз")
        print('Введите "да" или "1" если нужно и "нет" или "0" если не нужно')
        needManual = input("Ввод: ")
        print()
    if needManual in ['да', "1"]:
        print()
        printManualNext()
        input("Нажмите Enter чтобы продолжить ")
        print()
    
    printBoard(board, NEXT)  # печатаем доску
    print('Определим начальную конфигурацию поля')
    print('Инструкция по настройке находится справа от поля')
    WhoIsMoving = True # Кто ходит первый (всегда крестики)
    while True:  # Цикл с настройкой поля
        got = input("\nВвод: ").split()  # Получаем ввод от пользователя
        # Проверяем корректность введённой команды:
        if len(got) == 1:  # длиной в одно слово может быть только команда на выход или на завершение настройки
            if got[0].lower() in ['выход', '-v']:
                exit()
            if got[0].lower() == 'done':
                ok, diff, noneCount = isBoardOk(board)  #  после заверешения настройки проверяем поле на правильность. 
                if not ok:
                    print("Поменяйте конфигурацию.")
                    continue
                break
        if len(got) == 3:  # В три слова уже могут быть команды добавления или удаления символа с поля
            ok = False
            # проверяем корректность команды:
            if got[0].upper() in letters and \
                got[1] in numbers and \
                got[2] in ['o', 'о', "0", "х", "x"]:
                ok = True
            elif got[0] == 'del' and \
                got[1].upper() in letters and \
                got[2] in numbers:
                ok = True
            if not ok:
                print("Некорректный ввод | см. инструкцию")
                continue
            got, ok = correctInput2(got)
            if not ok:  # непрошли проверку
                print("Попробуйте заного")
                continue
            if got[0] == 'del':  
                board[got[1]][got[2]] = ' '  # Удаляем символ
            else:  
                board[got[0]][got[1]] = got[2]  # добавляем символ
        else:
            print("Некорректный ввод | см. инструкцию")
            continue
        printBoard(board, NEXT)  # выводим обновлённую доску на экран
    if diff == 1: # Если крестиков на 1 больше чем ноликов - ходят нолики
        WhoIsMoving = False
    elif diff == 0: # и наоборот соответственно
        WhoIsMoving = True
    return WhoIsMoving, noneCount # Возвращаем кто ходит и кол-во пустых клеток, чтобы потом еще раз их не считать

def waysToWin(needCords=False):
    # Функция возвращает кол-во победных ходов для крестиков и для ноликов (независимо от того, чей ход) и координаты этих ходов
    krestCount = 0
    nolikCount = 0
    krestCords = []
    nolikCords = []

    for flag in cords:
        cells = cords[flag]
        nc = 0
        kc = 0
        nonec = 0
        nonex, noney = 0, 0
        for x, y in cells:
            if board[x][y] == 'x':
                kc += 1
            elif board[x][y] == 'o':
                nc += 1
            elif board[x][y] == ' ':
                nonec += 1
                nonex, noney = x, y
        if nonec == 1:
            if kc == 2:
                krestCount += 1
                krestCords.append((nonex, noney))
            elif nc == 2:
                nolikCount += 1
                nolikCords.append((nonex, noney))
    if needCords:
        return krestCount, nolikCount, krestCords, nolikCords    
    return krestCount, nolikCount

def doMove(board, move, WhoIsMoving):
    # Симулируем ход
    clone = deepcopy(board)
    clone[move[0]][move[1]] = "x" if WhoIsMoving else "o"
    return clone

def posblMoves(board):
    # Функция возвращает все возможные ходы (координаты пустых клеток)
    moves = set()
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == " ":
                moves.add((x,y))
                
    return moves

def terminal(board):
    # Функция похожа на isBoardOk и выполняет похожую задачу
    didWin = didSmOneWin(board, allFlags)
    boardFilled = False
    count  = 0
    for r in board:
        for c in r:
            if c != ' ':
                count +=1
                
    if count == 9:
        boardFilled = True

    if didWin or boardFilled:
        return True  # игра окончена
    
    if not didWin and boardFilled == False:
        return False  # еще играем

def utility(board):
    # только если игра окончена
    if terminal(board):
        _, char = didSmOneWin(board, allFlags, True)
        # переводим победителя в циферку
        if char == "x":
            return 1
        elif char == "o":
            return -1
        else:
            return 0  # ничья

def maxPlayer(board):
    if terminal(board):  # Если игра окончена
        return utility(board), None

    value = float('-inf')
    move = None

    for action in posblMoves(board):
        # сходили крестиком, теперь ходим ноликом, перед этим симулирует этот самый ход крестиком
        res, _ = minPlayer(doMove(board, action, True))

        if res > value: # получилась победа крестиком, вовзращаем
            value = res
            move = action
            if value == 1:
                return value, move

    return value, move

def minPlayer(board):
    if terminal(board):  # Если игра окончена
        return utility(board), None

    value = float('inf')
    move = None

    for action in posblMoves(board):
        # сходили ноликом, теперь ходим крестиком, перед этим симулирует этот самый ход ноликом
        res, _ = maxPlayer(doMove(board, action, False))

        if res < value: # получилась победа ноликом, вовзращаем
            value = res
            move = action
            if value == -1:
                return value, move

    return value, move

def minimax(board, WhoIsMoving):
    if didSmOneWin(board, allFlags):
        return None  # если кто-то уже выйграл

    if WhoIsMoving:  # Ходят крестики:
        _, bestMove = maxPlayer(board)
        return bestMove
    elif not WhoIsMoving:  # Ходят нолики:
        _, bestMove = minPlayer(board)
        return bestMove

def bestNextStep():
    WhoIsMoving, noneConut = boardSetup()  # Настраиваем начальную конфгурацию поля
    # доска настроена в глобальной переменной board, поэтому boardSetup() не возвращает доску

    didWin, char = didSmOneWin(board, allFlags, True)  # проверяем выйграл ли кто-нибудь уже
    if didWin:
        print(f'Лучшего хода нет, так как {"крестики" if char == "x" else "нолики"} уже победили.')
        exit()

    kc, nc, kcords, ncords = waysToWin(1)
    if WhoIsMoving and kc > 0:  # ход крестиков и у них есть победный ход
        print(f'Лучший ход для крестиков в этой позиции: {letters[kcords[0][0]]}{numbers[kcords[0][1]]}')
        exit()
    elif  not WhoIsMoving and nc > 0:  # ход ноликов и у них есть победный ход
        print(f'Лучший ход для ноликов в этой позиции: {letters[ncords[0][0]]}{numbers[ncords[0][1]]}')
        exit()

    if WhoIsMoving and nc > 1: # ход крестиков и у ноликов 2 или больше победных ходов, а у крестиков нет победного
        print('В данной ситуации любой ход крестиков приводит к победе ноликов.')
        exit()
    elif not WhoIsMoving and kc > 1:  # ход ноликов и у крестиков 2 или больше победных ходов, а у ноликов нет победного
        print('В данной ситуации любой ход ноликов приводит к победе крестиков.')
        exit()

    if noneConut == 1:  # одна пустая клетка на поле
        print("На поле осталась одна единственная клетка. Очевидно крестики ходят туда)")

    else:  # далее вычисляем лучший ход рекурсивной функцией:
        move = minimax(board, WhoIsMoving)
        print(f"Лучшим следующим ходом для {'крестиков' if WhoIsMoving else 'ноликов'} будет ход на клетку {letters[move[0]]}{numbers[move[1]]}")
    
def main():
    game = True  # Правда - играем, Ложь - игра закончилась по той или иной причине
    WhoIsMoving = True  # Кто сейчас ходит - True - крестики, False - нолики
    while game:  # Основной цикл игры
        printBoard(board, MAIN)  # выводим поле и инструкцию на экран
        while True:  # Цикл с проверкой корректности введённых команд
            move = input("\nВаш ход: ").split()  # Получаем ввод от пользователя
            if move:  # команда может быть разной длины (как по кол-ву символов так и по кол-ву строк)
                # поэтому ниже идёт несколько условий с проверкой на корректность введённых данных
                if move[0].lower() in ['выход', '-v']:
                    game = False
                    break
                if len(move) == 2:  # Проверка на корректный ввод
                    move, test = correctInput1(move)
                    if test:
                        break  # Если ввод корректный, завершаем цикл отвечающий за проверку ввода
                else:
                    okLen = False
                    if len(move) == 1:
                        move = move[0]
                        if len(move) == 2:
                            okLen = True
                            move = [move[0], move[1]]
                            move, test = correctInput1(move)
                            if test:
                                break
                    if not okLen:
                        print("Некорректный ввод - неверная длина команды")
            print("Попробуйте ввести команду еще раз")  # цикл с проверкой не завершится, пока не будет получен корректный ввод
        if not game:
            break  # Пользователь введ команду выхода из игры
        board[move[0]][move[1]] = ("x" if WhoIsMoving else "o")  # совеишение хода
        won = didSmOneWin(board, varsOfPositionToCheck[''.join(list(map(lambda x: str(x), move)))])  # Проверяем выйграл ли кто-нибудь
        if won:  # Если есть победитель
            printBoard(board, MAIN)
            print(f'\nПобедили {("крестики" if WhoIsMoving else "нолики")}!\nИгра окончена.')
            print("Нажмите Enter чтобы выйти")
            input()
            exit()
        WhoIsMoving = not WhoIsMoving  # Передаём ход другой стороне, если было True (Крестики) - станет False (нолики) и наоборот

if __name__ == "__main__":
    # Общение с пользователем(ями)
    got = input("Введите название режима в который вы будете играть\n(1 - основной, 2 - поиск лучшего хода)\nВвод: ")
    while got not in ['1', '2']:  # два режима игры
        print()
        print('Некорректный ввод\nПросьба ввести только "1" или "2"\n1 - Это обычный режим игры')
        print('2 - режим поиска оптимального следующего хода')
        got = input("Ввод: ")
    if got == '1':
        main()  # запуск основного режима игры
    elif got == '2':
        bestNextStep()  # Запуск режима игры с поиском наилучшего следующего хода