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

    key_mapping = {
        "disaster": "Катастрофа",
        "duration": "Длительность прибывания",
        "rooms": "Комнаты",
        "size": "Размер бункера"
    }

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
            if characteristic == "rooms":
                # Для "rooms" выбираем случайное количество значений от 1 до 5
                num_values = random.randint(1, 5)
                self.characteristics[characteristic] = random.sample(options, min(num_values, len(options)))
                logger.info(f"{characteristic.capitalize()} установлена как: {', '.join(self.characteristics[characteristic])}")
            else:
                # Для остальных характеристик выбираем одно значение
                self.characteristics[characteristic] = random.choice(options)
                logger.info(f"{characteristic.capitalize()} установлена как: {self.characteristics[characteristic]}")
        else:
            logger.info(f"Характеристика {characteristic} не найдена")


    def set_characteristics(self):
        for key in self.characteristic_index:
            self.set_characteristic(key)

    def return_info(self):
        message = "Информация о бункере:\n"
        for key, value in self.characteristics.items():
            name = Bunker.key_mapping.get(key, key)  # Получаем русское название характеристики

            # Если значение — это список, форматируем как строку с запятыми
            if isinstance(value, list):
                formatted_value = ", ".join(value)
            else:
                formatted_value = value if value else "Неизвестно"

            # Добавляем характеристику в сообщение
            if key == "disaster":
                message+= f"{formatted_value}\n"
            else:
                message += f"{name}: {formatted_value}\n"

        return message

if __name__ == "__main__":
    bunker = Bunker(10)
    print(bunker.return_info())