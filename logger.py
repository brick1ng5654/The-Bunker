import logging

# Создаем и настраиваем логгер
logger = logging.getLogger("game_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()  # Для вывода логов в консоль
# handler = logging.FileHandler('game.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
