import random
from logger import logger

class Session:
    def __init__(self, admin_id):
        self.name = None
        self.users_amount = 1
        self.players_amount = 0
        self.users = {}
        self.players = {}
        self.votes = {}
        self.bunker = None
        self.admin_id = admin_id
        self.session_active = True
        self.game_active = True

    def assign_name(self):
        number = random.randint(10000, 99999)
        logger.info(f"Для сессии присвоено имя {number}")
        self.name = number

    def add_user(self, user):
        if user.id in self.users.keys():
            logger.warning(f"Пользователь {user.id} уже в сессии")
            return
        self.users[user.id] = user
        self.players_amount+=1
        logger.debug(f"Пользователь {user.id} добавлен к сессии пользователя {self.admin_id}")

    def remove_user(self, user_id):
        if user_id in self.users.keys():
            self.users.pop(user_id)
            self.users_amount-=1
            logger.debug(f"Пользователь {user_id} был удалён из сессии пользователя {self.admin_id}")
            if user_id == self.admin_id:
                self.assign_new_admin()
        else:
            logger.debug(f"Пользователя {user_id} не найден в сессии пользователя {self.admin_id}")
    
    def assign_new_admin(self):
        if self.users.keys():
            self.admin_id = next(iter(self.users.keys()))
            logger.debug(f"Новый пользователь сессии - {self.admin_id}")
        else:
            self.admin_id = None
            self.session_active = False
            logger.debug(f"Сессия {self.name} завершена, так как пользователей больше нет")



if __name__ == "__main__":
    session = Session()
    session.assign_name()

