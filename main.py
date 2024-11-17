from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters, MessageHandler, ContextTypes, PollAnswerHandler
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
admin_id = None # ID админа сессии
players = {} # Словарь игроков
votes = {}
bunker = None # Object
session_active = False # Активна ли сессия
game_active = False # Активна ли игра

# Отправка сообщения text пользователю member_id
async def reply_message_to_member(context: ContextTypes.DEFAULT_TYPE, member_id, text, reply_markup=""):
    try:
        await context.bot.send_message(chat_id=member_id, text=text, reply_markup=reply_markup)
        logger.debug(f"Сообщение {text[:15]} успешно отправлено {member_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения {text[:15]} {member_id}. {e}", exc_info=True)

# Отправка сообщения text пользователям members
async def reply_message_to_members(context: ContextTypes.DEFAULT_TYPE, members, text, reply_markup=""):
    for member_id in members.keys():
        try:
            await context.bot.send_message(chat_id=member_id, text=text, reply_markup=reply_markup)
            logger.debug(f"Сообщение {text} успешно отправлено {member_id}")
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение пользователью {member_id}, {e}",exc_info=True)
            return
    logger.debug(f"Сообщение {text} успешно отправлено всем {members.keys()}")

# Отправка сообщения о некорректности команды
async def wrong_comand(update: Update, context: ContextTypes.DEFAULT_TYPE, text, message="Неизвестная команда. Пожалуйста, выберите действие на клавиатуре."):
    user = update.message.from_user
    logger.warning(f"Пользователь {user.id} ввёл неизвестную команду '{text}'")
    await reply_message_to_member(context, user.id, message)

# Выполнение команды /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f"{user.id} ({user.username}) начал общение с ботом")

    welcome_message = f"Привет, {user.first_name}! Я бот, предназначенный для игры в Бункер. По кнопкам ниже ты можешь осуществлять навигацию."
    await reply_message_to_member(context, user.id, welcome_message, main_menu_reply_markup)

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
        elif text == "игроки":
            await print_all_players_info(update, context)
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
            await back_to_profile(update, context, admin_id)
            return
        elif text == "меню игры":
            if user.id == admin_id:
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
            await vote_menu(update, context)
            return
        elif text == "провести голосование":
            await vote_for_kick(update, context)
            return
        elif text == "выгнать игрока":
            await kick_voted_player(update, context)
            return
        else:
            # Проверяем, содержится ли текст в key_mapping
            for key, value in Player.return_key_mapping().items():
                if text == value.lower():  # Сравниваем на совпадение с русским значением
                    await reveal_atribute(update, context, key)
                    return
            
            await wrong_comand(update, context, text)
            return
    else:
        await wrong_comand(update, context, text)

# Вызов главного меню
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in players.keys():
        await reply_message_to_member(context, user.id, "Чтобы вызвать главное меню, вы должны покинуть игру")
        logger.warning(f"Пользователь {user.id} попытался вызвать в главное меню из игры")
        return
    if user.id in users.keys():
        update.message.reply_text("Чтобы вызвать главное меню, вы должны покинуть сессию")
        logger.warning(f"Пользователь {user.id} попытался вызвать в главное меню из сессии")
        return
    
    logger.debug(f"Вызов главного меню пользователем {user.id}")
    await call_main_menu(update, context)

# Вызов главного меню для всех участников группы members
async def main_menu_for_all_members(context: ContextTypes.DEFAULT_TYPE, members):
    await reply_message_to_members(context, members, "Главное меню:", reply_markup=main_menu_reply_markup)

# Вызов меню сессии
async def session_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in players.keys():
        reply_message_to_member(context, user.id, "Чтобы вызвать меню сессии, вы должны покинуть игру")
        logger.warning(f"Пользователь {user.id} попытался вызвать меню сессии из игры")
        return
    if user.id not in users.keys():
        reply_message_to_member(context, user.id, "Чтобы вызвать меню сессии вы должны находиться в ней")
        logger.warning(f"Пользователь {user.id} попытался вызвать меню сессии вне сессии")
        return
    
    logger.debug(f"Вызов меню сессии пользователем {user.id}")
    if user.id == admin_id: await call_admin_session_menu(update, context)
    else: await call_user_session_menu(update, context)

# Вызов меню сессии для всех участников группы members
async def session_menu_for_all_members(context: ContextTypes.DEFAULT_TYPE, members):
    await reply_message_to_members(context, members, "Меню сессии:", reply_markup=user_session_menu_reply_markup)

# Вызов меню игры
async def game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id not in players.keys():
        reply_message_to_member(context, user.id, "Чтобы вызвать меню игры, вы должны находится в ней")
        logger.warning(f"Пользователь {user.id} попытался вызвать меню игры вне её")
        return

    logger.debug(f"Вызов меню игры пользователем {user.id}")
    
    if user.id == admin_id: await call_admin_game_menu(update, context)
    else: await call_game_menu(update, context)

# Вызов меню игры для всех участников группы members
async def game_menu_for_all_members(context: ContextTypes.DEFAULT_TYPE, members):
    await reply_message_to_members(context, members, "Меню игры:", reply_markup=player_game_menu_reply_markup)

# Выполнение команды "Создать сессию"
async def create_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin_id, session_active, users_number
    user = update.message.from_user

    if user.id in users.keys():
        if user.id == admin_id:
            await reply_message_to_member(context, user.id, "Чтобы создать сессию, вам необходимо завершить текущую")
            logger.warning(f"Администратор {user.id} попытался создать ещё одну сессию")
            return
        await reply_message_to_member(context, user.id, "Чтобы создать сессию, вам необходимо покинуть текущую")
        logger.warning(f"Пользователь {user.id} попытался создать сессию в сессии")
        return
    elif (session_active):
        await reply_message_to_member(context, user.id, "На данный момент нельзя создать более одной сессии")
        return

    logger.info(f"Пользователь {user.id} создал сессию и является её администратором")
    session_active = True
    users_number = 1
    admin_id = user.id
    users[user.id] = user

    await session_menu(update, context)

# Команда подключения к сессии
async def join_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in users.keys():
        await reply_message_to_member(context, user.id, "Чтобы присоединиться к сессии, вы должны выйти из текущей")
        logger.debug(f"Пользователь {user.id} попытался присоединиться к сессии в сессии")
    elif (session_active):
        await reply_message_to_members(context, users, f"Пользователь {user.first_name} присоединился к сессии!")
        logger.info(f"Пользователь {user.id} присоединился к сессии {admin_id}")
        users[user.id] = user
        await session_menu(update, context)
    else:
        await reply_message_to_member(context, user.id, "Активных сессий на данный момент нет")


# Команда вызова вывода списка всех участников сессии
async def members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = ""

    if user.id in users.keys():
        await reply_message_to_member(context, user.id, f"Список участников сессии ({len(users)})")
        logger.debug(f"Вывод списка участников сессии {admin_id} пользователем {user.id}")
        for user_id in users.values():
            message+=f"○ {user_id.first_name}\n"
        await reply_message_to_member(context, user.id, message)
        return
    else:
        await reply_message_to_member(context, user.id, "Чтобы вызвать список участников сессии, вы должны находиться в сессии")
        logger.debug(f"Пользователь {user.id} попытался вызывать список участников сессии вне сессии")
        return

# Команда отключения от сессии
async def disconnect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session_active, users_number, admin_id
    user = update.message.from_user

    if session_active:
        if user.id in users.keys():
            if (admin_id == user.id):
                logger.info(f"{admin_id} завершил сессию:")
                await reply_message_to_members(context, users, f"Администратор сессии завершил её")
                await main_menu_for_all_members(context, users)
                users_number = 0
                session_active = False
                admin_id = None

                for user_id in list(users.keys()):
                    logger.info(f"{user.id} покинул сессию")
                    users.pop(user_id, None)
                return
            else:
                logger.info(f"{user.username} покинул сессию")
                await update.message.reply_text("Вы покинули сессию")
                users.pop(user.id, None)
                users_number-=1
                await reply_message_to_members(context, users, f"{user.first_name} покинул сессию")
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
        if user.id == admin_id:
            logger.debug(f"Адмиринстратор сессии {user.id} покинул игру")
            
            players.pop(user.id)
            await call_user_session_menu(update, context)
            if(players):
                new_admin = next(iter(players.values())) # Первый игрок из словаря
                admin_id = new_admin.user_id
                await reply_message_to_members(context, players, f"Администратор сессии покинул игру игру. Новым администратором сессии назначен {new_admin.user_name}")
                await reply_message_to_member(context, admin_id, "Меню игры:", reply_markup=admin_game_menu_reply_markup)
            else:
                admin_id = None
                logger.info("Все игроки покинули игру. Игра завершена")
                return
        else:
            players.pop(user.id)
            logger.debug(f"{user.id} покинул игру")
            reply_message_to_members(context, players, f"{user.first_name} покинул игру")
            await call_user_session_menu(update, context)
    else:
        await reply_message_to_member(context, user.id, "Чтобы покинуть игру, вы должны находиться в ней")

# Команда создания игры
async def create_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game_active, players_number, players, bunker
    user = update.message.from_user

    try:
        if admin_id == user.id and (not game_active):
            game_active = True
            for user_id in users.keys():
                players_number+=1
                players[user_id] = Player(users[user_id], players_number)
                players[user_id].assign_attributes_to_player()
            bunker = Bunker(players_number)
            bunker.assign_attributes_to_bunker()
            logger.info(f"Игра начата. Список игрков: {players.keys()}")
            await reply_message_to_members(context, players, "Игра начинается! Желаю приятной игры и веселья!")
            players_without_admin = {user_id: player for user_id, player in players.items() if user_id != admin_id}
            await game_menu_for_all_members(context, players_without_admin)
            await call_admin_game_menu(update, context)
        elif (admin_id == user.id and game_active):
            await reply_message_to_member(context, user.id, "Чтобы начать игру, вы должны закончить текущую")
        else:
            await reply_message_to_member(context, user.id, "Сессию может начать только администратор сессии")
    except Exception as e:
        logger.error(f"{e}", exc_info=True)
        return

async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in players.keys():
        message = players[user.id].print_my_profile()
        await reply_message_to_member(context, user.id, message)
        logger.debug(f"{user.id} вызвал меню профиля")
        await call_profile_menu(update, context)
    else:
        await reply_message_to_member(context, user.id, "Чтобы вызвать меню профиля, вы должны находиться в игре")
        logger.debug(f"Пользователь {user.id} попытался вызвать меню профиля вне игры")

async def reveal_atribute_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in players.keys():
        logger.debug(f"{user.id} ({user.username}) нажал кнопку 'Раскрыть характеристику'")
        await call_reveal_atribute_menu(update, context)
    else:
        await reply_message_to_member(context, user.id, "Чтобы раскрыть характеристику, вы должны находиться в игре")
        logger.debug(f"Пользователь {user.id} попытался раскрыть характеристику вне игры")

async def reveal_atribute(update: Update, context: ContextTypes.DEFAULT_TYPE, atribute):
    user = update.message.from_user

    if user.id in players.keys():
        if players[user.id].is_visible(atribute):
            await reply_message_to_member(context, user.id, "Характеристика уже раскрыта! Пожалуйста, выберите другую.")
            logger.debug(f"Пользователь {user.id} попытался раскрыть уже раскрытую характеристику")
        else:
            players[user.id].set_visibility(atribute, 1)
            logger.debug(f"Характеристика {atribute} раскрыта у пользователя {user.id}")
            await reply_message_to_member(context, user.id, "Вы раскрыли характеристику!")
    else:
        await reply_message_to_member(context, user.id, "Чтобы раскрыть характеристику, вы должны находиться в игре")
        logger.debug(f"Пользователь {user.id} попытался раскрыть характеристику вне игры")

async def print_all_players_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if(len(players)>0):
        logger.debug(f"Начало вывода информации об игроках {players.keys()}")
        for player in players.values():
            logger.debug(f"Вывод информации о {player.user_id}")
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
            await reply_message_to_member(context, user.id, message)
    else:
        await reply_message_to_member(context, user.id, "Чтобы вызвать ифнормацию об игроках, игра должна быть запущена")
        logger.debug(f"Пользователь {user.id} попытался вызвать информацию об ихгроках вне игры")

async def print_bunker_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in players.keys():
        bunker_info = bunker.return_info()
        await reply_message_to_member(context, user.id, bunker_info)
        logger.debug(f"Игрок {user.id} вызывает информацию о бункере")
    else:
        await reply_message_to_member(context, user.id, "Чтобы узнать ифнормацию о бункере, вы должны находиться в игре")

async def vote_menu(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await call_vote_menu(update, context)

async def vote_for_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in players.keys():
        if(user.id != admin_id):
            await update.message.reply_text("Начать голосование может только администратор сессии")
        else:
            await reply_message_to_members(context, players, "Начинается голосование за изгнание игрока!")

            question = "Кого следует выгнать?"
            options = []
            for player in players.values():
                options.append(f"Игрок №{player.player_number}")
            is_anon = False

            poll_ids = {}  # Хранение poll_id для каждого игрока
            for player_id in players.keys():
                poll_message = await context.bot.send_poll(chat_id=player_id, question=question, options=options, is_anonymous=is_anon)
                poll_ids[player_id] = poll_message.poll.id  # Сохранение poll_id

            # Сохранение всех poll_id для дальнейшего использования
            context.chat_data["poll_ids"] = poll_ids
    else:
        await reply_message_to_member(context, user.id, "Чтобы провести голосование, вы должны находиться в игре")
        logger.debug(f"Пользователь {user.id} попытался провести голосование вне игры")

# Обработка завершённого голосования
async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll_id = update.poll_answer.poll_id  # ID опроса
    user_id = update.poll_answer.user.id  # ID пользователя
    selected_option_ids = update.poll_answer.option_ids  # ID выбранных опций

    # Сохранение голоса
    if poll_id not in votes:
        votes[poll_id] = {}
    votes[poll_id][user_id] = selected_option_ids

    # Логирование
    logger.debug(f"Пользователь {user_id} проголосовал за {selected_option_ids}")

async def define_voted_player(votes, options):
    results = {option: 0 for option in options}  # Инициализация счетчиков для каждого варианта
    for poll in votes.values():  # Для каждого опроса
        for selected_options in poll.values():  # Для каждого ответа
            for option_id in selected_options:
                results[options[option_id]] += 1

    logger.info(f"{results}")

    votes_for_winner = 0

    # Определение победителя
    for player, votes in results.items():
        if votes > votes_for_winner:
            winner = player
            votes_for_winner = votes

    winner = int(winner.replace("Игрок №", ""))
    logger.info(f"{winner} and {votes_for_winner}")
    return winner, votes_for_winner

async def kick_voted_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin_id, game_active, players
    if "poll_ids" not in context.chat_data:
        await update.message.reply_text("Голосование не было начато.")
        return

    options = [f"Игрок №{player.player_number}" for player in players.values()]
    winner, votes_for_winner = await define_voted_player(votes, options)

    for player in list(players.values()):
        if player.player_number == winner:
            winner_id = player.user_id
            await reply_message_to_member(context, winner_id, "Вы были изгнаны")
            players.pop(winner_id)
            await reply_message_to_members(context, players, f"Путём голосования был изгнан {player.user_name} ({votes_for_winner})")

            if(len(players) > bunker.alive_players):
                if winner_id != admin_id:
                    await reply_message_to_member(context, winner_id, "Меню сессии:", reply_markup=user_session_menu)
                else:
                    new_admin = next(iter(players.values())) # Первый игрок из словаря
                    admin_id = new_admin.user_id
                    await reply_message_to_members(context, players, f"Администратор сессии был изгнан из игры. Новым администратором сессии назначен {new_admin.user_name}")
                    await reply_message_to_member(context, admin_id, "Меню игры:", reply_markup=admin_game_menu_reply_markup)
                    await reply_message_to_member(context, winner_id, "Меню игры:", reply_markup=user_session_menu_reply_markup)
            else:
                await reply_message_to_members(context, users, f"Игра окончена! {players.keys()} выжили", reply_markup=user_session_menu_reply_markup)
                await reply_message_to_member(context, admin_id, "Меню сессии:", reply_markup=admin_session_menu_reply_markup)
                players.clear()
                game_active = False

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(PollAnswerHandler(handle_poll_answer))

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен")
    app.run_polling()