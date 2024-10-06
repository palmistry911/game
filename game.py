import random
import string
import logging

# Настраиваем логирование в файл
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


class TreasureMap:
    def __init__(self, size=10):
        self.size = size
        self.treasure_position = self.generate_treasure_position()

    def generate_treasure_position(self):
        x = random.randint(0, self.size - 1)
        y = random.choice(string.ascii_lowercase[:self.size])
        return (x, y)

    def is_treasure(self, x, y):
        return (x, y) == self.treasure_position

    def give_hint(self, x, y):
        tx, ty = self.treasure_position
        distance = abs(tx - x) + abs(ord(ty) - ord(y))
        if distance == 0:
            return "Поздравляем! Вы нашли сокровище."
        elif distance <= 2:
            return "Вы очень близко к сокровищу!"
        elif distance <= 5:
            return "Вы близко к сокровищу!"
        else:
            return "Вы далеко от сокровища."


class Player:
    def __init__(self, attempts=10):
        self.attempts = attempts
        self.guesses = []

    def make_guess(self, input_coords):
        try:
            x, y = input_coords.split(',')
            x = int(x.strip())
            y = y.strip().lower()
            if x < 0 or x >= 10 or y not in string.ascii_lowercase[:10]:
                raise ValueError
            self.guesses.append((x, y))
            return (x, y)
        except ValueError:
            return None


class Game:
    def __init__(self):
        self.map = TreasureMap()
        self.player = Player()
        self.is_game_over = False

    def start(self):
        print("Добро пожаловать в игру «Поиск сокровища»!")
        print("На игровом поле размером 10x10 спрятано сокровище.")
        print("Ваша задача — найти его за минимальное количество попыток.")
        print("Координаты вводятся в формате «x, y», где x — горизонтальная координата, y — вертикальная координата.")
        print("Удачи!\n")

        logging.info("Игра началась. Сокровище на координатах: %s", self.map.treasure_position)

        while not self.is_game_over and self.player.attempts > 0:
            print(f"Осталось попыток: {self.player.attempts}")
            guess = input("Введите координаты: ").strip()

            coordinates = self.player.make_guess(guess)
            if coordinates is None:
                print("Ошибка! Введите координаты в формате «x, y». Например: 3, а.")
                logging.warning("Неправильный ввод: %s", guess)
                continue

            x, y = coordinates
            logging.info("Игрок сделал ход: %s", coordinates)

            if self.map.is_treasure(x, y):
                print("Поздравляем! Вы нашли сокровище.")
                print(f"Игра завершена. Сокровище найдено. Попыток: {10 - self.player.attempts + 1}.")
                print("Ваш промокод SUPER100")
                logging.info("Сокровище найдено за %d попыток", 10 - self.player.attempts + 1)
                self.is_game_over = True
            else:
                hint = self.map.give_hint(x, y)
                print(hint)
                logging.info("Подсказка: %s", hint)
                self.player.attempts -= 1

        if not self.is_game_over:
            print("Количество попыток исчерпано. Сокровище не найдено.")
            logging.info("Игра завершена. Сокровище не найдено.")


if __name__ == "__main__":
    game = Game()
    game.start()
