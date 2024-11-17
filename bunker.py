from logger import logger
import random

class Bunker:
    def __init__(self, number_of_players):
        self.numb_of_players = number_of_players
        self.attributes = {}
        logger.info("Экземпляр класса Bunker создан")

    def assign_attributes_to_bunker(self):
        self.available_attributes = self.load_attributes()
        self.set_attributes()

    attribute_index = {
            "disaster": 0,
            "duration": 1,
            "rooms": 2,
            "size": 3
        }

    key_mapping = {
        "disaster": "Катастрофа",
        "duration": "Длительность прибывания",
        "rooms": "Комнаты",
        "size": "Размер бункера"
    }

    # Метод для загрузки характеристик из текстового файла
    def load_attributes(self, filename="bunker_attributes.txt"):
        attributes = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    key, values = line.split(">")
                    items = values.split(";")
                    attributes[key] = []
                    for item in items:
                        attributes[key].append(item)
        return attributes
    
    def set_attribute(self, attribute):
        options = [value for value in self.available_attributes[attribute]]

        if options:
            if attribute == "rooms":
                # Для "rooms" выбираем случайное количество значений от 1 до 5
                num_values = random.randint(1, 5)
                self.attributes[attribute] = random.sample(options, min(num_values, len(options)))
                logger.debug(f"{attribute.capitalize()} установлена как: {', '.join(self.attributes[attribute])}")
            else:
                # Для остальных характеристик выбираем одно значение
                self.attributes[attribute] = random.choice(options)
                logger.debug(f"{attribute.capitalize()} установлена как: {self.attributes[attribute]}")
        else:
            logger.warning(f"Характеристика {attribute} не найдена")


    def set_attributes(self):
        for key in self.attribute_index:
            self.set_attribute(key)

    def return_info(self):
        message = "Информация о бункере:\n"
        for key, value in self.attributes.items():
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
    bunker.assign_attributes_to_bunker()
    print(bunker.return_info())