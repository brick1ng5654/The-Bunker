from logger import logger
import random

class Player:
    def __init__(self, user, player_number):
        self.user_id = user.id
        self.user_name = user.first_name
        self.user_username = user.username
        self.player_number = player_number
        self.attributes = {key: None for key in Player.attribute_index}
        self.visible = {key: False for key in Player.attribute_index}
        logger.info(f"Экземпляр класса Player для {self.user_id} ({self.user_username}) создан")

    def assign_attributes_to_player(self):
        self.available_attributes = Player.load_attributes()
        self.set_attributes()

    # Общие данные для всех экземпляров класса (Словарь характеристики с индексом и её название на русском) и работа с ними

    _loaded_attributes = None # Хранилище для характеристик из файла

    @staticmethod
    def load_attributes(filename="player_attributes.txt"):
        if Player._loaded_attributes is not None:
            return Player._loaded_attributes
        
        attributes = {}
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        key, values = line.split(":")
                        items = values.split(",")
                        attributes[key] = []
                        for item in items:
                            if "=" in item:
                                rarity, value = item.split("=")
                                attributes[key].append((rarity, value))
                            else:
                                logger.info(f"Некорректный формат строки: {item}")
            logger.debug("Характеристики успешно загружены")
            Player._loaded_attributes = attributes
            return attributes
        except Exception as e:
            logger.warning("Не удалось выполнить загрузить характеристки")
            logger.error(e, exc_info=True)
            return {}

    attribute_index= {
            "job": 0,
            "age": 1,
            "health": 2,
            "sex": 3,
            "gender": 4,
            "hobby": 5,
            "knowledge": 6,
            "fobia": 7,
            "fact": 8,
            "personality": 9,
            "bagage": 10,
            "action": 11,
            "condition": 12,
        }

    key_mapping = {
        "job": "Деятельность",
        "age": "Возраст",
        "health": "Здоровье",
        "sex": "Пол",
        "gender": "Ориентация",
        "hobby": "Хобби",
        "knowledge": "Знание",
        "fobia": "Фобия",
        "fact": "Факт",
        "personality": "Характер",
        "bagage": "Багаж",
        "action": "Карта действия",
        "condition": "Карта условия",
    }

    @classmethod
    def return_attribute_index(cls):
        return cls.attribute_index

    @classmethod
    def return_key_mapping(cls):
        return cls.key_mapping

    def return_visibility(self):
        return self.visible
    
    def return_info(self):
        return [self.user_username, self.player_number, self.attributes]
    
    @classmethod
    def get_attribute_index(cls, attribute):
        index = cls.attribute_index.get(attribute)
        if index is None:
            logger.info(f"Характеристика {attribute} не найдена в attribute_index.")
        return index

    # Метод для установки видимости характеристики
    def set_visibility(self, attribute, is_visible):
        index = self.get_attribute_index(attribute)
        if index is not None:  # Если характеристика найдена
            self.visible[attribute] = is_visible
        else:
            logger.info(f"Не удалось установить видимость для {attribute}.")

    # Метод для получения видимости характеристики
    def is_visible(self, attribute):
        index = self.get_attribute_index(attribute)
        if index is not None:
            return self.visible.get(attribute, False)
        return False
        
    # Метод получения информации о характеристике
    def print_my_profile(self):
        message=""
        message+=f"({self.player_number}) {self.user_name}\n"
        for key, value in self.attributes.items():
            status = "(o)" if self.is_visible(key) else "(-)"
            name = Player.key_mapping.get(key, key)  # Русское название или ключ, если не найден
            message+=f"{status} {name}: {value}\n"
        return ("\n"+message)
    
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
    def set_attribute(self, attribute):
        rarity_level = Player.generate_rarity()
        chosen_value = self.choose_value_by_rarity(attribute, rarity_level)
        if chosen_value:
            self.attributes[attribute] = chosen_value

    def choose_value_by_rarity(self, attribute, rarity_level):
        if attribute not in self.available_attributes:
            logger.info(f"Характеристика {attribute} не найдена")
            return None

        options = [
            value for rarity, value in self.available_attributes[attribute]
            if rarity == rarity_level
        ]

        if not options:
            logger.info(f"Нет доступных опций для редкости {rarity_level} у {attribute}")
            return None

        return random.choice(options)

    @staticmethod
    def generate_rarity():
        random_number = random.randint(1, 100)
        if random_number > 85:
            return "epic"
        elif random_number > 50:
            return "rare"
        else:
            return "common"

    def set_attributes(self):
        # Устанавливаем все характеристики
        for key in Player.attribute_index:
            self.set_attribute(key)
    
class User:
    def __init__(self, user_id, username, firstname):
        self.id = user_id
        self.username = username
        self.first_name = firstname


if __name__ == "__main__":
    user = User(1, "brick1ng5654", "Рафаэль")
    player = Player(user, 1)
    player.assign_attributes_to_player()
    message = player.print_my_profile()
    print(message)