from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, Updater, filters, MessageHandler, ContextTypes
import random
from logger import logger
import os
from player import Player

# Подключаем токен из файла
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Запускаем приложение
app = Application.builder().token(TOKEN).build()

# Глобальные переменные
player_number = 1 # Количество игроков в сессии
players = {} # Словарь игроков
session_active = False # Активна ли игра
admin = 0 # Админ сессии

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f"{user.username} начал общение с ботом")

    welcome_message = f"Привет, {user.first_name}! Я бот, предназначенный для игры в Бункер. По кнопкам ниже ты можешь осуществлять навигацию."
    await update.message.reply_text(welcome_message)
    await menu(update, context)

# Обработчик текстовых сообщений, реагирующий на команды без "/"

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text  # Получаем текст сообщения
    user = update.message.from_user
    text = text.lower()
    
    if text == "создать сессию":
        await create_session(update, context)
    elif text == "присоединиться к сессии":
        await update.message.reply_text("подключение к сессии")
    elif text == "участники":
        await members(update, context)
    elif text == "отключиться":
        await disconnect(update, context)
    elif text == "главное меню":
        await menu(update, context)
    else:
        logger.info(f"{user.first_name}: {text}")
        await update.message.reply_text("Неизвестная команда. Пожалуйста, выберите действие на клавиатуре.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active
    if session_active:
        update.message.reply_text("Сначала покиньте активную сессию")
        return
    keyboard = [
        ["Создать сессию", "Присоединиться к сессии"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,one_time_keyboard=True)
    await update.message.reply_text("Главное меню", reply_markup=reply_markup)

# Функция для обработки "Создать сессию"
async def create_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin, session_active, player_number
    user = update.message.from_user
    # Проверка не создана ли сессия ранеее
    if (session_active):
        if user.id == admin.id:
            await update.message.reply_text("Вы уже создали сессию!")
            logger.info(f"Пользователь {user.username} попытался заново создать сессию")
            return
        await update.message.reply_text("Сессия уже начата! Присоединяйся!")
        logger.info(f"Пользователь {user.username} попытался создать сессию")
        return

    # Создание сессии
    session_active = True
    admin = user
    logger.info(f"Пользователь {user.username} создал сессию и является её админом")
    players[user.id] = [user.id, user.first_name, user.username]

    keyboard = [
        ["Начать игру", "Участники"],
        ["Отключиться"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Вы начали сессию! Другие участники могут к ней присоединиться.", reply_markup=reply_markup)

async def members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active

    user = update.message.from_user

    if session_active:
        if(user.id in players.keys()):
            await update.message.reply_text("Список участников сессии:")
            for player_info in players.values():
                await update.message.reply_text(f"{player_info[1]}")
            return
        else:
            await update.message.reply_text("Вы не присоединены к сессии")
    await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")

async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active

    user = update.message.from_user
    if session_active:
        if user.id in players.keys():
            if (admin.id == user.id):
                logger.info(f"{admin.username} завершил сессию:")
                session_active = False
                for user_id, user_info in list(players.items()):
                    logger.info(f"{user_info[2]} покинул сессию")
                    players.pop(user_id, None)
                await update.message.reply_text("Вы завершили сессию")
                await menu(update, context) 
                return
            else:
                logger.info(f"{user.username} покинул сессию")
                players.pop(user.id, None)
                await update.message.reply_text("Вы покинули сессию")
                await menu(update, context) 
                return
        else:
            await update.message.reply_text("Вы не подключены к сессии")
            await menu(update, context) 
            return
    await update.message.reply_text("Вы не подключены к сессии")   

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("(?i)^Создать сессию$"), create_session))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("(?i)^Участники$"), members))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("(?i)^Отключиться$"), disconnect))

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен")
    app.run_polling()