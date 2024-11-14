import logging

# Создаем и настраиваем логгер
logger = logging.getLogger("game_logger")
logger.setLevel(logging.DEBUG)  # Устанавливаем общий уровень для логгера

# Обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Уровень DEBUG для консоли
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Обработчик для вывода логов в файл
file_handler = logging.FileHandler('game.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)  # Уровень INFO для файла
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)