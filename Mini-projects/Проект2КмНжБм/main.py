import random
import time  # иМпОрТиРуЕм

PAPER = 'бумага'
STONE = 'камень'
SCISSORS = 'ножницы'
PC = 'pc'  # Константы
PLAYER = 'player'
STOP = 'stop'

stratsID = ['1', '2', '3']  # Стратегии описаны в ТЗ
score = {
    PC: 0,  # Счетчик игры
    PLAYER: 0
}

# С помощью этих списков определяется шанс поменять стратегию после каждого хода (ТЗ)
chance20 = [0, 0, 1, 0, 0]  # 20%
chance35 = [0] * 20 + [1] * 7  # 35%
chance50 = [0, 1]  # 50%

start2 = {  # Словарь для второй стратегии компьютера
    PAPER: SCISSORS,
    STONE: PAPER,
    SCISSORS: STONE
}

strat3 = {  # Словарь для третьей стратегии компьютера
    (PAPER, STONE): SCISSORS,
    (STONE, SCISSORS): PAPER,
    (PAPER, SCISSORS): STONE,
    (STONE, STONE): random.choice([PAPER, SCISSORS]),
    (PAPER, PAPER): random.choice([STONE, SCISSORS]),
    (SCISSORS, SCISSORS): random.choice([PAPER, STONE])
}

def changeStrat(chance):
    # возвращает True или False - меняем ли мы стратегию. Определяется с определённым шансом. Это описано в play()
    return bool(random.choice(chance))

def whoWon(player, pc):
    # Функция получает ход игрока и ход компьютера после чего вернёт PLAYER если выйграл игрок, PC - если компьютер или "0" если ничья
    if player == pc:
        return '0'  # ничья
    # если не ничья то я разбиваю на возможные "пары". Чтобы меньше условий в ифах писать)
    if PAPER not in [player, pc]:  # Если никто не ввёл бумагу
        if player == STONE:
            return PLAYER
        return PC
    elif STONE not in [player, pc]:  # Если никто не ввёл камень
        if player == SCISSORS:
            return PLAYER
        return PC
    elif SCISSORS not in [player, pc]:  # Если никто не ввёл ножницы
        if player == PAPER:
            return PLAYER
        return PC

def printScore():
    # просто вывод текущего счета
    print(f"\nТекущий счет:\nКомпьютер: {score[PC]}\nВы(игрок): {score[PLAYER]}\n")

def helpManual():
    # Вывод инструкции к игре
    print()
    print("Иструкция к игре:")
    print()
    print("1) Когда вас просят ввести команду у вас есть только эти варианты:")
    print("-help => вывод иструкции (Только в меню)")
    print("-play => запуск игры с компьютером (Только в меню)")
    print("-score => вывод текущего счета (Только в меню)")
    print("-v => завершение работы программы")
    print('-stop => остановка игры с компьютером, вас перебросит обратно в "меню"')
    print()
    print('2) Игра с компьютером')
    print('После ввода команды "-play" начинается игра с компьютером. Остановить её можно командой "-stop"')
    print('Вам нужно будет вводить слова "камень", "ножницы" или "бумага",')
    print('Также можно вводить только первые буквы, т.е.: "к", "н" или "б". Компьютер вас поймёт')
    print('Компьютер в свою очередь также сделает свой ход.')
    print('После этого программа автоматически определит победителя и выведет счет на экран.')
    print()
    print("Регистр нигде не играет роли, можете вводить в любом регистреn\n")

def doMove(lastPlayer, lastPc, stratID):
    # Функция возвращает ход компьютера в зависимости от стратегии. Они (стратегии) описаны в ТЗ
    if stratID == '1':
        return lastPlayer
    elif stratID == '2':
        won = whoWon(lastPlayer, lastPc)
        if won == PC:
            return lastPc
        return start2[lastPlayer]
    elif stratID == '3':
        return strat3[tuple(sorted([lastPlayer, lastPc]))]

def getMoveFromPlayer():
    # Функция получает, проверяет и возвращает ввод от пользователя
    got = input("\nВаш ход: ").lower()
    while got not in [PAPER, STONE, SCISSORS, PAPER[0], STONE[0], SCISSORS[0], '-v', '-stop']:
        print("\nНекорректный ввод. Можно вводить либо полностью либо слова целиком. Вот примеры:")
        print('"бумага", "б", "камень", "н"\nТакже можно ввести "-v" для выхода из игры или "-stop" для выхода в меню\nПопробуйте еще раз.\n')
        got = input("Ваш ход: ").lower()  # Просим ввести корректный ход или команду
    if got == '-v':
        print('Выход...')
        time.sleep(0.6)  # Завершение работы
        exit()
    if got == '-stop':
        return STOP  # Выход в меню
    if got in [PAPER, STONE, SCISSORS]:
        return got  # Если ввели полное слово - его и возвращаем
    else:
        if got == PAPER[0]:
            return PAPER  # Если только одна буква - то смотрим какое это слово
        elif got == STONE[0]:
            return STONE
        elif got == SCISSORS[0]:
            return SCISSORS

def play():
    # основная функция. Здесь происходит "игра"

    stratID = random.choice(stratsID)  # Выбираем первоначальную стратегию
    count = 0  # счетчик отвечает за кол-во раз, когда changeStrat() вовзращает False.
    # Если это происходит часто, то программа повышает шанс того, что changeStrat() вернёт True

    # первый ход
    move = random.choice([PAPER, STONE, SCISSORS]) # у компьютера рандом (описано в ТЗ)
    playerMove = getMoveFromPlayer()  # Получаем ход от пользователя
    if playerMove == STOP:
        return  # Выходим обратно в меню
    print(f"Ход компьютера: {move}")  # Показываем пользователю ход компьютера
    won = whoWon(playerMove, move)  # Смотрим кто победил
    if won != '0':
        score[won] += 1  # изменяем счет игры
    printScore()  # выводим счет
    chance = chance20  # ставим изначальный шанс того, что changeStrat() вернёт True на 20% - минимум.

    while True:  # основной цикл игры
        move = doMove(playerMove, move, stratID)  # получаем ход компьютера
        playerMove = getMoveFromPlayer()  # ход игрока
        if playerMove == STOP:
            return  # выходим в меню
        print(f"Ход компьютера: {move}")  # Выводим ход компьютера
        won = whoWon(playerMove, move)  # смотрим кто победил
        if won != '0':
            score[won] += 1  # изменяем счет
        printScore()  # Выводим счет

        change = changeStrat(chance)  # Смотрим, будем ли мы менять стратегию
        if not change:
            count += 1  # если нет - увеличиваем count 
        else:
            stratID = random.choice(stratsID)  # тут меняем стратегию
            count = 0  # и обнуляем count и возвращаем count на 20%
            chance = chance20
        
        if count == 5:  # повышаем шанс до 35% если мы уже 5 ходов не меняем стратегию
            chance = chance35
        if count == 7:
            chance = chance50  # Если мы всё еще не поменяли стратегию, а прошло уже 7 ходов, то ставим шанс на 50%

def menu():
    print('\nСупер! Ты попал в меню игры. Для вывода иструкции нужно написать "-help"!')
    print("Если вы первый раз зашли в игру, советую сразу просмотреть иструкцию\n")
    while True:
        got = input("Ввод команды: ").lower()  # получаем ввод от пользователя
        if got[0] == '-':  # смотрим что он там ввёл
            if got[1:] == 'help':
                helpManual()  # выводим инструкцию
            elif got[1:] == 'play':
                play()  # запускаем игру
                print('\nТы в меню. Помощь: "-help"\n')  # это мы вернулись в меню после игры
            elif got[1:] == 'v':  # команда на выход из программы
                print("Выход...")
                time.sleep(0.6)
                exit()
            elif got[1:] == 'score':
                printScore()  # вывод текущего счета
            else:
                print('\nНеизвестная команда. Попробуйте еще раз. Помощь: "-help"\n')
        else:  # говорим что ввод кривой
            print('\nУ меня тут такое дурацкое правило есть, команда должна начинаться с символа "-" =)\n')

if __name__ == "__main__":
    print('\n')
    print("Привет! Ты запустил игру камень-ножницы-бумага!")
    print("Твоим аппонентом будет компьютер. Пока-что ваш счет 0:0")
    print('Начнём игру? Введи "да" или "нет" в любом регистре.\n')
    got = input("Ввод: ").lower()  # Общение с пользователем
    while got not in ['да', 'нет']:
        print('Некорректный ввод. Попробуй еще раз. Можно вводить только "да" или "нет", регистр неважен.')
        got = input("Ввод: ").lower()
    if got == "нет":
        print("\nВыход...", end='')
        time.sleep(0.6)  # ну нет так нет
        exit()
    menu()  # запуск меню