import random
from random import randint
import pygame
from const import PLAYER_SIZE, PLAYER_COLOR, WHITE_COLOR, CPERCENT, UPERCENT, load_all_data, font

# Класс игрока
class Player:
    def __init__(self, x, y, name, characteristics):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.name = name
        self.characteristics = characteristics
        self.avatar = pygame.image.load("data/avatar.png")  # Загрузка изображения аватара
        self.avatar = pygame.transform.scale(self.avatar, (PLAYER_SIZE, PLAYER_SIZE))  # Масштабирование до нужного размера
        self.avatar_pick = pygame.image.load("data/avatar_pick.png")  # Загрузка изображения для состояния наведения
        self.avatar_pick = pygame.transform.scale(self.avatar_pick, (PLAYER_SIZE, PLAYER_SIZE))  # Масштабирование до нужного размера


    def draw(self, screen):
        # Проверка, находится ли курсор над аватаром
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.avatar_pick, self.rect.topleft)  # Отрисовка изображения при наведении
        else:
            screen.blit(self.avatar, self.rect.topleft)  # Отрисовка обычного изображения

        # Отрисовка имени игрока
        name_surface = font.render(self.name, True, WHITE_COLOR)
        name_rect = name_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
        screen.blit(name_surface, name_rect.topleft)

    def draw_characteristics(self, screen, font):
        y_offset = 0

        def draw_text(text, x, y, width, font, color):
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            for line in lines:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (x, y))
                y += font.get_linesize()

            return len(lines) * font.get_linesize()  # Возвращает количество пикселей, занятых текстом

        # Drawing the characteristics
        for characteristic in self.characteristics:
            y_offset += draw_text(characteristic, 1095, 90 + y_offset, 490, font, WHITE_COLOR) + 5

def choose_rare(common, unusual, rare):
    i = randint(1, 100)
    if i <= CPERCENT:
        if common:
            value = random.choice(common)
            common.remove(value)
        else:
            value = "No common value available"
    elif i <= CPERCENT + UPERCENT:
        if unusual:
            value = random.choice(unusual)
            unusual.remove(value)
        else:
            value = "No unusual value available"
    else:
        if rare:
            value = random.choice(rare)
            rare.remove(value)
        else:
            value = "No rare value available"
    return value

def choose_non_unique(choices):
    if choices:
        return random.choice(choices)
    else:
        return "No value available"

def create_player(x, y, n, data):
    profile = []
    profile.append('КАРТОЧКА ИГРОКА ' + str(n))
    profile.append('Био-характеристика: ' + choose_non_unique(data["common_sex"]) + ' / Возраст ' + choose_non_unique(data["common_age"]))
    profile.append('Ориентация: ' + choose_non_unique(data["common_gender"]))
    profile.append('Род деятельности: ' + choose_rare(data["common_job"], data["unusual_job"], data["rare_job"]))
    profile.append('Состояние здоровья: ' + choose_rare(data["common_health"], data["unusual_health"], data["rare_health"]))
    profile.append('Хобби: ' + choose_rare(data["common_hobby"], data["unusual_hobby"], data["rare_hobby"]))
    
    fobia = random.choice(data["fobia"])
    profile.append('Фобия :'+ fobia)
    if fobia in data["fobia"]:
        data["fobia"].remove(fobia)

    # Выбор черты характера
    characteristic = random.choice(data["personality"])
    profile.append('Черта характера: ' + characteristic)
    if characteristic in data["personality"]:
        data["personality"].remove(characteristic)  # Удаление элемента из списка
    

    profile.append('Доп. информация: ' + choose_rare(data["common_fact"], data["unusual_fact"], data["rare_fact"]))
    profile.append('Багаж: ' + choose_rare(data["common_bagage"], data["unusual_bagage"], data["rare_bagage"]))
    
    # Выбор карты условия
    condition = random.choice(data["condition"])
    profile.append('Карта условия: ' + condition)
    if condition in data["condition"]:
        data["condition"].remove(condition)  # Удаление элемента из списка
    
    if __name__ == "__main__":
        print(profile)
    return Player(x, y, f"Игрок {n}", profile)

if __name__ == "__main__":
    data = load_all_data()
    create_player(100, 100, 1, data)
