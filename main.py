from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, filters, MessageHandler, ContextTypes
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
admin = None # Админ сессии / Object like user
players = {} # Словарь игроков
session_active = False # Активна ли сессия
game_active = False # Активна ли игра

# Выполнение команды /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f"{user.id} ({user.username}) начал общение с ботом")

    welcome_message = f"Привет, {user.first_name}! Я бот, предназначенный для игры в Бункер. По кнопкам ниже ты можешь осуществлять навигацию."
    await update.message.reply_text(welcome_message)
    await main_menu(update, context)

# Обработчик текстовых сообщений, реагирующий на команды без "/"
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text  # Получаем текст сообщения
    text = text.lower() # Сводим к одному регистру
    
    if text == "создать сессию":
        await create_session(update, context)
    elif text == "присоединиться к сессии":
        await join_session(update, context)
    elif text == "участники":
        await members(update, context)
    elif text == "отключиться":
        await disconnect(update, context)
    elif text == "главное меню":
        await main_menu(update, context)
    elif text == "начать игру":
        await create_game(update, context)
    else:
        user = update.message.from_user
        logger.warning(f"{user.id} ({user.username}): {text}") # Ввод некорректной команды
        
        await update.message.reply_text("Неизвестная команда. Пожалуйста, выберите действие на клавиатуре.")

# Вызов главного меню
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if game_active and user.id in players.keys():
        update.message.reply_text("Сначала покиньте игру")
        logger.warning(f"Пользователь {user.id} ({user.username}) попытался вызвать главное меню из игры")
        return
    if session_active and user.id in users.keys():
        update.message.reply_text("Сначала покиньте активную сессию")
        logger.warning(f"Пользователь {user.id} ({user.username}) попытался вызвать главное меню из сессии")
        return
    
    logger.debug(f"Вызов главного меню пользователем {user.id} ({user.username})")
    keyboard = [
        ["Создать сессию", "Присоединиться к сессии"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True,one_time_keyboard=False)
    await update.message.reply_text("Главное меню:", reply_markup=reply_markup)

# Вызов главного меню для всех участников группы members
async def main_menu_for_all_members(members, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Вызывание основного меню для всех пользователей {members}")

    keyboard = [
        ["Создать сессию", "Присоединиться к сессии"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await notify_all_members(members, "Главное меню:", context, reply_markup)

# Вызов меню сессии
async def session_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if (not session_active):
        update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
        logger.warning(f"Пользователь {user.id} ({user.username}) попытался вызвать меню несуществующей сессии")
        return
    
    logger.debug(f"Вызов меню сессии пользователем {user.id} ({user.username})")
    keyboard = [
        ["Начать игру", "Участники"],
        ["Отключиться"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Меню сессии:", reply_markup=reply_markup)

# Вызов меню сессии для всех участников группы members
async def session_menu_for_all_members(members, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Вызывание меню сессии для всех пользователей {members}") # Возможна проблема с {members}

    keyboard = [
        ["Начать игру", "Участники"],
        ["Отключиться"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    notify_all_members(members, "Меню сессии:", context, reply_markup=reply_markup)

# Вызов меню игры
async def game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if not game_active:
        if session_active:
            await update.message.reply_text("Игра ещё не начата. Быстрее создавай и приглашай друзей!")
            await session_menu(update, context)
            logger.warning(f"Пользователь {user.id} ({user.username}) попытался вызвать меню не запустившейся игры в активной сессии")
            return
        else:
            await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
            await main_menu(update, context)
            logger.warning(f"Пользователь {user.username} попытался вызвать меню не запустившейся игры в не активной сессии")
            return

    logger.debug(f"Вызов меню игры пользователем {user.id} ({user.username})")
    keyboard = [
        ["Профиль"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Меню игры:", reply_markup=reply_markup)

# Вызов меню игры для всех участников группы members
async def game_menu_for_all_members(members, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Вызывание игрового меню для всех пользователей")

    keyboard = [
        ["Профиль"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await notify_all_members(players, "Меню игры:", context, reply_markup)

# Вызов текстового сообщения message_text с reply_markup (пустым по умолчанию) для всех участников группы members 
async def notify_all_members(members, message_text, context: ContextTypes.DEFAULT_TYPE, reply_markup=""):
    logger.debug(f"Сообщение '{message_text}' всем пользователям группы {members}")
    for member_id, member_info in members.items():
        logger.debug(f"{member_info}")
        try:
            await context.bot.send_message(chat_id=member_id, text=message_text, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение пользователью {member_id}, {e}",exc_info=True)

# Выполнение команды "Создать сессию"
async def create_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin, session_active, users_number
    user = update.message.from_user

    if (session_active):
        if user.id == admin.id:
            await update.message.reply_text("Вы уже создали сессию!")
            logger.warning(f"Пользователь {user.id} ({user.username}) попытался заново создать сессию")
            return
        await update.message.reply_text("Сессия уже начата! Присоединяйся!")
        logger.warning(f"Пользователь {user.username} попытался создать сессию")
        return

    logger.info(f"Пользователь {user.id} ({user.username}) создал сессию и является её админом")
    session_active = True
    users_number = 1
    admin = user
    users[user.id] = [user.id, user.first_name, user.username] #### change to user, that dict has objects

    await session_menu(update, context)

# Команда вызова вывода списка всех участников сессии
async def members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if session_active:
        if(user.id in users.keys()):
            await update.message.reply_text(f"Список участников сессии ({len(players)}):")
            for player_info in users.values():
                await update.message.reply_text(f"{player_info[1]}")
            logger.debug("Вывод списка участников сессии")
            return
        else:
            logger.debug(f"Пользователь {user.id} ({user.username}) не подлкюченный к сессии попытался вывести список участников")
            await update.message.reply_text("Вы не присоединены к сессии")
    logger.debug(f"Пользователь {user.id} ({user.username}) попытался вывести список несуществующей сессии")
    await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")

# Команда отключения от сессии
async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, users_number

    user = update.message.from_user
    if session_active:
        if user.id in users.keys():
            if (admin.id == user.id):
                logger.info(f"{admin.username} завершил сессию:")
                await main_menu_for_all_members(users, context)
                users_number = 0
                session_active = False
                for user_id, user_info in list(users.items()):
                    logger.info(f"{user_info[2]} покинул сессию")
                    users.pop(user_id, None)
                await update.message.reply_text("Вы завершили сессию")
                return
            else:
                logger.info(f"{user.username} покинул сессию")
                users.pop(user.id, None)
                users_number-=1
                await update.message.reply_text("Вы покинули сессию")
                await main_menu(update, context) 
                return
        else:
            await update.message.reply_text("Вы не подключены к сессии")
            await main_menu(update, context) 
            return
    await update.message.reply_text("Вы не подключены к сессии")
    await main_menu(update, context)   

async def join_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, admin
    user = update.message.from_user

    if(session_active):
        users[user.id] = [user.id, user.first_name, user.username]
        logger.info(f"{user.username} присоединился к сессии {admin.username}")
        message = f"Пользователь {user.username} присоединился к сессии!"
        context.bot.send_message(chat_id=admin.id, text=message)
        await session_menu(update, context)
    else:
        await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")

async def create_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_active, admin, users_number, players
    user = update.message.from_user
    try:
        if admin.id == user.id:
            game_active = True
            for user_id, user_info in users.items():
                players[user_id] = Player(*user_info, users_number)
                users_number+=1
            await notify_all_members(players,"Игра начинается! Желаю приятной игры и веселья!", context)
            await game_menu_for_all_members(players, context)
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