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
users_number = 0 # Количество пользователей в сессии
players_number = 0 # Количество игроков в сессии
users = {} # Словарь пользователей
players = {} # Словарь игроков
session_active = False # Активна ли сессия
game_active = False # Активна ли игра
admin = 0 # Админ сессии

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.debug(f"{user.username} начал общение с ботом")

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
        await join_session(update, context)
    elif text == "участники":
        await members(update, context)
    elif text == "отключиться":
        await disconnect(update, context)
    elif text == "главное меню":
        await menu(update, context)
    elif text == "начать игру":
        await create_game(update, context)
    else:
        logger.warning(f"{user.first_name}: {text}")
        await update.message.reply_text("Неизвестная команда. Пожалуйста, выберите действие на клавиатуре.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, users
    user = update.message.from_user
    if session_active and user.id in users.keys():
        update.message.reply_text("Сначала покиньте активную сессию")
        logger.warning(f"Пользователь {user.username} попытался вызвать главное меню")
        return
    keyboard = [
        ["Создать сессию", "Присоединиться к сессии"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,one_time_keyboard=False)
    await update.message.reply_text("Главное меню", reply_markup=reply_markup)

async def session_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    global session_active
    if (not session_active):
        update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
        logger.warning(f"Пользователь {user.username} попытался вызвать меню несуществующей сессии")
        return
    keyboard = [
        ["Начать игру", "Участники"],
        ["Отключиться"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Меню сессии", reply_markup=reply_markup)

async def game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_active
    user = update.message.from_user

    if not game_active:
        if session_active:
            await update.message.reply_text("Начать игру может только администратор сессии")
            await session_menu(update, context)
            logger.warning(f"Пользователь {user.username} попытался вызвать меню игры")
            return
        else:
            await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
            await menu(update, context)
            logger.warning(f"Пользователь {user.username} попытался вызвать меню игры")
            return

    keyboard = [
        ["Профиль"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Меню игры", reply_markup=reply_markup)

async def notify_all_players(message_text, context: ContextTypes.DEFAULT_TYPE):
    global players
    logger.debug("Уведомление всех пользователей сессии")
    for player_id, player_info in players.items():
        logger.debug(f"id: {player_id}")
        try:
            await context.bot.send_message(chat_id= player_id, text=message_text)
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение пользователью {e}",exc_info=True)

# Функция для обработки "Создать сессию"
async def create_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin, session_active, users_number
    user = update.message.from_user
    # Проверка не создана ли сессия ранеее
    if (session_active):
        if user.id == admin.id:
            await update.message.reply_text("Вы уже создали сессию!")
            logger.warning(f"Пользователь {user.username} попытался заново создать сессию")
            return
        await update.message.reply_text("Сессия уже начата! Присоединяйся!")
        logger.warning(f"Пользователь {user.username} попытался создать сессию")
        return

    # Создание сессии
    session_active = True
    users_number = 1
    admin = user
    logger.info(f"Пользователь {user.username} создал сессию и является её админом")
    users[user.id] = [user.id, user.first_name, user.username]

    await session_menu(update, context)

async def members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active

    user = update.message.from_user

    if session_active:
        if(user.id in users.keys()):
            await update.message.reply_text("Список участников сессии:")
            for player_info in users.values():
                await update.message.reply_text(f"{player_info[1]}")
            return
        else:
            await update.message.reply_text("Вы не присоединены к сессии")
    await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")

async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, users_number

    user = update.message.from_user
    if session_active:
        if user.id in users.keys():
            if (admin.id == user.id):
                logger.info(f"{admin.username} завершил сессию:")
                users_number = 0
                session_active = False
                for user_id, user_info in list(users.items()):
                    logger.info(f"{user_info[2]} покинул сессию")
                    users.pop(user_id, None)
                await update.message.reply_text("Вы завершили сессию")
                users_number-=1
                await menu(update, context) 
                return
            else:
                logger.info(f"{user.username} покинул сессию")
                users.pop(user.id, None)
                await update.message.reply_text("Вы покинули сессию")
                await menu(update, context) 
                return
        else:
            await update.message.reply_text("Вы не подключены к сессии")
            await menu(update, context) 
            return
    await update.message.reply_text("Вы не подключены к сессии")
    await menu(update, context)   

async def join_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active
    user = update.message.from_user

    if(session_active):
        users[user.id] = [user.id, user.first_name, user.username]
        await session_menu(update, context)
    else:
        await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")

async def create_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_active, admin, users_number
    user = update.message.from_user
    try:
        if admin.id == user.id:
            game_active = True
            for user_id, user_info in users.items():
                logger.debug(f"{user_info}")
                players[user_id] = Player(*user_info, users_number)
                users_number+=1
            await notify_all_players("Игра начинается! Желаю приятной игры и веселья!", context)
            await game_menu(update, context)
        else:
            await update.message.reply_text("Сессию может начать только администратор сессии")
            return
    except Exception as e:
        logger.error(f"{e}", exc_info=True)
        await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
        return


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен")
    app.run_polling()