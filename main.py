from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, Updater
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
admin_id = 0

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f"{user.username} начал общение с ботом")
    welcome_message = f"Привет, {user.first_name}! Я бот, предназначенный для игры в Бункер. По кнопкам ниже ты можешь осуществлять навигацию"
    # Создание кнопок
    keyboard = [
        ["Создать комнату", "Присоединиться к комнате"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,one_time_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Обработчик команды "Создать комнату"
async def create_room(update: Update, context: CallbackContext) -> None:
    global game_active, player_number, admin_id
    user = update.message.from_user
    # Проверка, активна ли уже игра
    if game_active:
        await update.message.reply_text("Игра уже запущена. Присоединяйтесь!")
        logger.info(f"Пользователь {user.first_name} попытался безуспешно создать игру")
        return
    
    # Запуск игры и добавление первого игрока
    game_active = True
    admin_id = update.message.from_user
    logger.info(f"Пользователь {user.first_name} создал комнату для игры")
    player_id = user.id
    players[player_id] = Player(user.first_name, player_number, player_id)
    logger.info(players[player_id])
    
    keyboard = [ ["Начать игру"] ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(f"Игра скоро начнётся! Чтобы начать игру с текущим количеством игроков нажмите кнопку ниже", reply_markup=reply_markup)
    await update.message.reply_text("Другие игроки могут присоединиться к игре с помощью команды /join_game.")
    player_number+=1
    
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

async def my_info(update: Update, context: CallbackContext) -> None:
    global game_active
    user = update.message.from_user
    
    if not game_active:
        await update.message.reply_text("Игра ещё не началась. Используйте /start_game для запуска.")
        logger.info(f"Пользователь {user.first_name} попытался присоединится к несуществующей игре")
        return

    await update.message.reply_text(f"{players[user.id].return_info()}")
    logger.info(f"Пользователь {user.first_name} написал /my_info")

# async def my_info(update: Update, context: CallbackContext) -> None:
#     global game_active
#     user = update.message.from_user
    
#     if not game_active:
#         await update.message.reply_text("Игра ещё не началась. Используйте /start_game для запуска.")
#         logger.info(f"Пользователь {user.first_name} попытался присоединится к несуществующей игре")
#         return

#     for player in players.values():
#         await update.message.reply_text(f"{player.return_info()}")
#         logger.info(f"Пользователь {user.first_name} написал /my_info")


# Регистрация команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("Создать комнату", create_room))
app.add_handler(CommandHandler("join_game", join_game))
app.add_handler(CommandHandler("my_info", my_info))

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен")
    app.run_polling()