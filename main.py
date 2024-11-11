from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import random
from logger import logger
import os
from player import Player

# Подключаем токен из файла
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Запускаем приложение
app = Application.builder().token(TOKEN).build()

# Списки для хранения информации о количестве игроков, игроках, их характеристиках и информация о сессии
player_number = 1
players = {}
game_active = False

# Обработчик команды /start_game
async def start_game(update: Update, context: CallbackContext) -> None:
    global game_active, player_number
    user = update.message.from_user
    # Проверка, активна ли уже игра
    if game_active:
        await update.message.reply_text("Игра уже запущена. Присоединяйтесь!")
        logger.info(f"Пользователь {user.first_name} попытался безуспешно создать игру")
        return
    
    # Запуск игры и добавление первого игрока
    game_active = True
    logger.info(f"Пользователь {user.first_name} начал игру")
    player_id = user.id
    players[player_id] = Player(user.first_name ,player_number, player_id)
    player_number+=1
    logger.info(players[player_id])
    
    await update.message.reply_text(f"Игра началась! Игрок {user.first_name} начал игру!")
    
    # Добавляем ещё игроков через команду /join_game (её можно прописать отдельно)
    await update.message.reply_text("Другие игроки могут присоединиться к игре с помощью команды /join_game.")
    
    # После регистрации всех игроков можно начать игру или первый ход

# Обработчик команды /join_game
async def join_game(update: Update, context: CallbackContext) -> None:
    global game_active, player_number
    user = update.message.from_user
    
    if not game_active:
        await update.message.reply_text("Игра ещё не началась. Используйте /start_game для запуска.")
        logger.info(f"Пользователь {user.first_name} попытался присоединится к несуществующей игре")
        return
    
    player_id = user.id
    
    if player_id in players:
        await update.message.reply_text("Вы уже зарегистрированы в игре!")
        logger.info(f"Пользователь {user.first_name} попытался присоединится к уже присоединенной игре")
        return
    
    players[player_id] = Player(user.first_name ,player_number, player_id)
    player_number+=1
    await update.message.reply_text(f"{user.first_name} присоединился к игре!")
    logger.info(f"Пользователь {user.first_name} присоединился к игре")

async def player_info(update: Update, context: CallbackContext) -> None:
    global game_active
    user = update.message.from_user
    
    if not game_active:
        await update.message.reply_text("Игра ещё не началась. Используйте /start_game для запуска.")
        logger.info(f"Пользователь {user.first_name} попытался присоединится к несуществующей игре")
        return

    for player in players.values():
        await update.message.reply_text(f"{player.return_info()}")
        logger.info(f"Пользователь {user.first_name} написал /player_info")

# Регистрация команд
app.add_handler(CommandHandler("start_game", start_game))
app.add_handler(CommandHandler("join_game", join_game))
app.add_handler(CommandHandler("player_info", player_info))

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен")
    app.run_polling()