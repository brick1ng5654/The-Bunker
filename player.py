from logger import logger
import random

class Player:
    def __init__(self, user_id, user_firstname, user_username, player_number):
        self.user_name = user_firstname
        self.player_number = player_number
        self.user_username = user_username
        self.user_id = user_id
        # Словарь для работы с индексами харакетристик
        self.characteristic_index= {
            "action": 0,
            "age": 1,
            "bagage": 2,
            "condition": 3,
            "fact": 4,
            "fobia": 5,
            "gender": 6,
            "health": 7,
            "hobby": 8,
            "job": 9,
            "knowledge": 10,
            "sex": 11,
            "personality": 12,
        }
        # Загрузка характеристик из файла
        self.available_characteristics = self.load_characteristics()
        self.characteristics = {}
        self.set_characteristics()
        self.visible = [0]*13

        logger.info(f"Экземпляр класса Player для {user_username} создан")

    def return_visibility(self):
        # print(self.visible)
        return self.visible
    
    def return_info(self):
        print(self.user_username, self.player_number, self.characteristics)
        return [self.user_username, self.player_number, self.characteristics]
    
    # Метод для установки видимости характеристики
    def set_visibility(self, characteristic, is_visible):
        if characteristic in self.characteristic_index:
            index = self.characteristic_index[characteristic]
            self.visible[index] = 1 if is_visible else 0
        else:
            logger.info(f"Характеристику {characteristic} не удалось найти")

    # Метод для получения видимости характеристики
    def is_visible(self, characteristic):
        if characteristic in self.characteristic_index:
            index = self.characteristic_index[characteristic]
            return bool(self.visible[index])
        else:
            logger.info(f"Характеристику {characteristic} не удалось найти")
            return False
        
    # Метод для загрузки характеристик из текстового файла
    def load_characteristics(self, filename="player_characteristics.txt"):
        characteristics = {}
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        key, values = line.split(":")
                        items = values.split(",")
                        characteristics[key] = []
                        for item in items:
                            if "=" in item:
                                rarity, value = item.split("=")
                                characteristics[key].append((rarity, value))
                            else:
                                logger.info(f"Некорректный формат строки: {item}")
            logger.debug("Метод load_characteristics был выполнен")
            return characteristics
        except Exception as e:
            logger.warning("Не удалось выполнить метод load_characteristics")
            logger.error(e, exc_info=True)


    # Метод для получения редкости характеристики на основе случайного числа
    def get_rarity(self):
        random_number = random.randint(1, 100)
        if random_number > 85:
            return "epic"  # Редкая характеристика
        elif random_number > 50:
            return "rare"  # Средняя редкость
        else:
            return "common"  # Обычная характеристика

    # Метод для установки характеристики с учетом её редкости
    def set_characteristic(self, characteristic):
        rarity_level = self.get_rarity()
        # logger.info(f"Для характеристики {characteristic} выбрана редкость: {rarity_level}")
        
        if characteristic in self.available_characteristics:
            # Получаем все возможные значения для данной характеристики и её редкости
            options = [
                value for rarity, value in self.available_characteristics[characteristic]
                if rarity == rarity_level
            ]
            if options:
                # Случайный выбор значения
                self.characteristics[characteristic] = random.choice(options)
                logger.debug(f"Для пользователя {self.user_id} ({self.user_username}){characteristic.capitalize()} установлена как: {self.characteristics[characteristic]}")
            else:
                logger.info(f"Нет доступных опций для редкости {rarity_level} у {characteristic}")
        else:
            logger.info(f"Характеристика {characteristic} не найдена")

    def set_characteristics(self):
        # Устанавливаем все характеристики
        for key in self.characteristic_index:
            self.set_characteristic(key)
    
if __name__ == "__main__":
    player = Player("еблан", 1, 1)
    player.return_info()