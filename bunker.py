from logger import logger
import random

class Bunker:
    def __init__(self, number_of_players):
        self.numb_of_players = number_of_players

        self.characteristic_index = {
            "disaster": 0,
            "duration": 1,
            "rooms": 2,
            "size": 3
        }

        self.available_characteristics = self.load_characteristics()
        self.characteristics = {}
        self.set_characteristics()

    # Метод для загрузки характеристик из текстового файла
    def load_characteristics(self, filename="bunker_characteristics.txt"):
        characteristics = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    key, values = line.split(">")
                    items = values.split(";")
                    characteristics[key] = []
                    for item in items:
                        characteristics[key].append(item)
        return characteristics
    
    def set_characteristic(self, characteristic):
        options = [value for value in self.available_characteristics[characteristic]]

        if options:
            # Случайный выбор значения
            self.characteristics[characteristic] = random.choice(options)
            logger.info(f"{characteristic.capitalize()} установлена как: {self.characteristics[characteristic]}")
        else: logger.info(f"Характеристика {characteristic} не найдена")
            
    def set_characteristics(self):
        for key in self.characteristic_index:
            self.set_characteristic(key)
    
    def return_info(self):
        print(self.characteristics)
        return self.characteristics

if __name__ == "__main__":
    bunker = Bunker(10)
    bunker.return_info()