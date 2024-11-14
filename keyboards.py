from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Основное меню
main_menu = [
    ["Создать сессию", "Присоединиться к сессии"]
]

main_menu_reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Главное меню:"):
    await update.message.reply_text(message, reply_markup=main_menu_reply_markup)

# Меню сессии админа
admin_session_menu = [
    ["Начать игру", "Участники"],
    ["Завершить сессию"]
]

admin_session_menu_reply_markup = ReplyKeyboardMarkup(admin_session_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_admin_session_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Меню сессии:"):
    await update.message.reply_text(message,reply_markup=admin_session_menu_reply_markup)

# Меню сессии пользователя
user_session_menu = [
    ["Участники"],
    ["Завершить сессию"]
]

user_session_menu_reply_markup = ReplyKeyboardMarkup(user_session_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_user_session_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Меню сессии:"):
    await update.message.reply_text(message,reply_markup=user_session_menu_reply_markup)

# Меню игры админа
admin_game_menu = [
    ["Игроки", "Профиль"],
    ["Голосование", "Бункер"],
    ["Прочее"]
]

admin_game_menu_reply_markup = ReplyKeyboardMarkup(admin_game_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_admin_game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Меню игры:"):
    await update.message.reply_text(message, reply_markup=admin_game_menu_reply_markup)

# Меню игры
player_game_menu = [
    ["Игроки", "Бункер"],
    ["Профиль"],
    ["Прочее"]
]

player_game_menu_reply_markup = ReplyKeyboardMarkup(player_game_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Меню игры:"):
    await update.message.reply_text(message, reply_markup=player_game_menu_reply_markup)

# Меню профиля
profile_menu = [
    ["Раскрыть характеристику"],
    ["Назад"]
]

profile_menu_reply_markup = ReplyKeyboardMarkup(profile_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message=""):
    await update.message.reply_text(message, reply_markup=profile_menu_reply_markup)

# Меню раскрытия характеристики
reveal_atribute_menu = [
    ["Деятельность", "Деятельность"],
    ["Возраст", "Здоровье"],
    ["Пол", "Ориентация"],
    ["Хобби", "Знание"],
    ["Фобия", "Факт"],
    ["Черта", "Багаж"],
    ["Карта действия", "Карта условия"],
    ["Назад"]
]

reveal_atribute_menu_reply_markup = ReplyKeyboardMarkup(reveal_atribute_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_reveal_atribute_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message=""):
    await update.message.reply_text(message, reply_markup=reveal_atribute_menu_reply_markup)

# Меню голосования
vote_menu = [
    ["Провести голосование"],
    ["Выгнать игрока"],
    ["Назад"]
]

vote_menu_reply_markup = ReplyKeyboardMarkup(vote_menu, resize_keyboard=True, one_time_keyboard=False)

async def call_vote_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Меню голосования:"):
    await update.message.reply_text(message, vote_menu_reply_markup)