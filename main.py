from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, Poll
from telegram.ext import Application, CommandHandler, CallbackContext, filters, MessageHandler, ContextTypes
from logger import logger
import os
from bunker import Bunker
from player import Player
from keyboards import *

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
bunker = None # Object
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
    user = update.message.from_user
    text = update.message.text  # Получаем текст сообщения
    text = text.lower() # Сводим к одному регистру

    if text == "создать сессию":
        await create_session(update, context)
        return
    elif text == "присоединиться к сессии":
        await join_session(update, context)
        return

    elif session_active and not game_active:
        # Сессия активна, но игра не запущена
        if text == "участники":
            await members(update, context)
            return
        elif text in ["отключиться", "завершить сессию"]:
            await disconnect(update, context)
            return
        elif text == "главное меню":
            await main_menu(update, context)
            return
        elif text == "начать игру":
            await create_game(update, context)
            return
        else:
            await wrong_comand(update, context, text)

    elif game_active:
        # Игра запущена
        if text == "профиль":
            await my_profile(update, context)
            return
        elif text == "раскрыть характеристику":
            await reveal_atribute_menu(update, context)
            return
        elif text == "назад":
            await back_to_profile(update, context, admin.id)
            return
        elif text == "меню игры":
            if user.id == admin.id:
                await call_admin_game_menu(update, context)
            else:
                await call_game_menu(update, context)
            return
        elif text == "участники":
            await members(update, context)
            return
        elif text == "игроки":
            await print_all_players_info(update, context)
            return
        elif text == "прочее":
            await call_other_menu(update, context)
            return
        elif text == "покинуть игру":
            await leave_game(update, context)
            return
        elif text == "бункер":
            await print_bunker_info(update, context)
            return
        elif text == "голосование":
            await vote_for_kick(update, context)
            return
        elif text == "выгнанть игрока":
            await handle_poll(update, context)
            return
        else:
            # Проверяем, содержится ли текст в key_mapping
            for key, value in Player.return_key_mapping().items():
                if text == value.lower():  # Сравниваем на совпадение с русским значением
                    await reveal_atribute(update, context, key)
                    return
            
            await wrong_comand(update, context, text)


async def wrong_comand(update: Update, context: ContextTypes.DEFAULT_TYPE, text, message="Неизвестная команда. Пожалуйста, выберите действие на клавиатуре."):
    user = update.message.from_user
    logger.warning(f"Пользователь {user.id} ({user.username}) ввёл неизвестную команду '{text}'")
    await update.message.reply_text(message)

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
    await call_main_menu(update, context)

# Вызов главного меню для всех участников группы members
async def main_menu_for_all_members(members, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Вызывание основного меню для всех пользователей {members.keys()}")
    await notify_all_members(members, context, "Главное меню:", reply_markup=main_menu_reply_markup)

# Вызов меню сессии
async def session_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if (not session_active):
        update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
        logger.warning(f"Пользователь {user.id} ({user.username}) попытался вызвать меню несуществующей сессии")
        return
    
    logger.debug(f"Вызов меню сессии пользователем {user.id} ({user.username})")
    if user.id == admin.id: await call_admin_session_menu(update, context)
    else: await call_user_session_menu(update, context)

# Вызов меню сессии для всех участников группы members
async def session_menu_for_all_members(members, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f"Вызывание меню сессии для всех пользователей {members}") # Возможна проблема с {members}
    notify_all_members(members, context, "Меню сессии:", reply_markup=user_session_menu_reply_markup)

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
    
    if user.id == admin.id: await call_admin_game_menu(update, context)
    else: await call_game_menu(update, context)

# Вызов меню игры для всех участников группы members
async def game_menu_for_all_members(members, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Вызывание игрового меню для всех пользователей")
    await notify_all_members(members, context, "Меню игры:", reply_markup=player_game_menu_reply_markup)

# Вызов текстового сообщения message_text с reply_markup (пустым по умолчанию) для всех участников группы members 
async def notify_all_members(members, context: ContextTypes.DEFAULT_TYPE, message_text, reply_markup=""):
    logger.debug(f"Сообщение '{message_text}' всем пользователям группы {members.keys()}")
    for member_id in members.keys():
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
            await update.message.reply_text(f"Список участников сессии ({len(users)}):")
            for player_info in users.values():
                await update.message.reply_text(f"{player_info[1]}")
            logger.debug(f"Вывод списка участников сессии пользователем {user.id} ({user.username})")
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
                await notify_all_members(users, context, message_text=f"Администратор сессии {admin.username} завершил её")
                await main_menu_for_all_members(users, context)
                users_number = 0
                session_active = False
                for user_id, user_info in list(users.items()):
                    logger.info(f"{user_info[2]} покинул сессию")
                    users.pop(user_id, None)
                return
            else:
                logger.info(f"{user.username} покинул сессию")
                notify_all_members(users, context, message_text=f"{user.username} покинул сессию")
                users.pop(user.id, None)
                users_number-=1
                await update.message.reply_text("Вы покинули сессию")
                await main_menu(update, context) 
                return
        else:
            await update.message.reply_text("Вы не подключены к сессии")
            await main_menu(update, context) 
            return
    logger.warning(f"Пользователь {user.id} ({user.username}) попытался отключиться от неподключенной сессии")
    await update.message.reply_text("Вы не подключены к сессии")
    await main_menu(update, context)   

async def leave_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    if user.id in players.keys():
        if user.id == admin.id:
            logger.debug(f"{user.id} ({user.username}) завершил игру")
            await notify_all_members(players, context, "Администратор сессии завершил игру")
            await main_menu_for_all_members(players, context)
            for player_id in list(players.keys()):
                players.pop(player_id)
        else:
            logger.debug(f"{user.id} ({user.username}) покинул игру")
            players.pop(user.id)
            notify_all_members(players, context, f"{user.first_name} покинул игру")
            await call_user_session_menu(update, context)
    else:
        await update.message.reply_text("Вы не находитесь в игре")

# Команда подключения к сессии
async def join_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if(session_active):
        message = f"Пользователь {user.username} присоединился к сессии!"
        await notify_all_members(users, context, message)
        users[user.id] = [user.id, user.first_name, user.username]
        logger.info(f"{user.id} ({user.username}) присоединился к сессии {admin.id} ({admin.username})")
        await session_menu(update, context)
    else:
        await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")

# Команда создания игры
async def create_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_active, players_number, players, bunker
    user = update.message.from_user
    try:
        if admin.id == user.id:
            game_active = True
            for user_id, user_info in users.items():
                players_number+=1
                players[user_id] = Player(user, players_number)
                players[user_id].assign_attributes_to_player()
            bunker = Bunker(players_number)
            bunker.assign_attributes_to_bunker()
            logger.info(f"Игра начата. Список игрков: {players.keys()}")
            await notify_all_members(players, context, "Игра начинается! Желаю приятной игры и веселья!")
            players_without_admin = {user_id: player for user_id, player in players.items() if user_id != admin.id}
            await game_menu_for_all_members(players_without_admin, context)
            await call_admin_game_menu(update, context)
        else:
            await update.message.reply_text("Сессию может начать только администратор сессии")
            return
    except Exception as e:
        logger.error(f"{e}", exc_info=True)
        await update.message.reply_text("Сессия ещё не начата. Быстрее создавай и приглашай друзей!")
        return

async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # global players
    user = update.message.from_user
    message = players[user.id].print_my_profile()
    await update.message.reply_text(message)
    await call_profile_menu(update, context)

async def reveal_atribute_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.debug(f"{user.id} ({user.username}) нажал кнопку 'Раскрыть характеристику'")
    await call_reveal_atribute_menu(update, context)

async def reveal_atribute(update: Update, context: ContextTypes.DEFAULT_TYPE, atribute):
    user = update.message.from_user
    if not game_active:
        logger.debug(f"{user.id} ({user.username}) попытался раскрыть характеристику вне игры")
        await update.message.reply_text("Вы не находитесь в игре")
    if players[user.id].is_visible(atribute):
        await update.message.reply_text(f"Характеристика уже раскрыта! Пожалуйста, выберите другую.")
    else:
        logger.debug(f"Характеристика {atribute} раскрыта у пользователя {user.id} ({user.username})")
        players[user.id].set_visibility(atribute, 1)
        await update.message.reply_text("Вы раскрыли характеристику!")

async def print_all_players_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Начало вывода информации об игроках")
    for player_id, player in players.items():
        logger.debug(f"Вывод информации о {player.user_id} ({player.user_username})")
        message = f"({player.player_number}) {player.user_name}:\n"
        for key, value in player.attributes.items():
            if player.is_visible(key):
                atribute_name = Player.key_mapping.get(key, key)
                message = message + f"{atribute_name}: {value}\n"
        # Сбор неизвестных характеристик
        unknown_atribute = [
            Player.key_mapping.get(key, key)
            for key in player.attributes.keys()
            if not player.is_visible(key)
        ]
        if unknown_atribute:
            message = message + "\n"
            message = message+("Неизвестные характеристики: " + ", ".join(unknown_atribute))
        await update.message.reply_text(message)

async def print_bunker_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if game_active:
        bunker_info = bunker.return_info()
        await update.message.reply_text(bunker_info)
    else:
        await update.message.reply_text("Игра ещё не начата!")

async def vote_for_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if(user.id != admin.id):
        await update.message.reply_text("Начать голосование может только администратор сессии")
        return
    await notify_all_members(players, context, "Начинается голосование за изгнание игрока!")
    question = "Кого следует выгнать?"
    options = []
    for player in players.values():
        options.append(f"Игрок №{player.player_number}")
    is_anon = False

    await update.message.reply_poll(question, options, is_anonymous=is_anon)

# Обработка завершённого голосования
async def handle_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = update.poll
    results = poll.options  # Результаты голосования
    question = poll.question  # Вопрос голосования
    logger.info(f"{results}")

    # Формируем сообщение с результатами
    results_message = f"Результаты голосования: {question}\n"
    for option in results:
        results_message += f"{option.text}: {option.voter_count} голосов\n"

    # Отправляем результаты
    await context.bot.send_message(chat_id=update.effective_chat.id, text=results_message)

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))


# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен")
    app.run_polling()