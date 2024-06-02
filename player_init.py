import random
from random import randint
import pygame

# Константы
PLAYER_SIZE = 150
PLAYER_COLOR = (90, 90, 90)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
CPERCENT = 60
UPERCENT = 30

# Класс игрока
class Player:
    def __init__(self, x, y, name, characteristics):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.name = name
        self.characteristics = characteristics

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

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
            y_offset += draw_text(characteristic, 1095,  90 + y_offset, 490, font, TEXT_COLOR) + 5

def load_array(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except:
        print("Error!")
        return []

def choose_rare(filename1,filename2,filename3):
    common = load_array(filename1)
    unusual = load_array(filename2)
    rare = load_array(filename3)

    i = randint(1, 100)
    if (i <= CPERCENT): value = random.choice(common)
    elif (i <= CPERCENT+UPERCENT): value = random.choice(unusual)
    else: value = random.choice(rare)

    return value if value else "No available value"

def create_player(x, y, n):
    profile = []
    profile.append('КАРТОЧКА ИГРОКА '+str(n))
    profile.append('Био-характеристика: '+choose_rare("data/sex/common_sex.txt","data/sex/unusual_sex.txt","data/sex/rare_sex.txt")+' / Возраст '+choose_rare("data/age/common_age.txt","data/age/unusual_age.txt","data/age/rare_age.txt"))
    profile.append('Ориентация: '+choose_rare("data/gender/common_gender.txt","data/gender/unusual_gender.txt","data/gender/rare_gender.txt"))
    profile.append('Род деятельности: '+choose_rare("data/job/common_job.txt","data/job/unusual_job.txt","data/job/rare_job.txt"))
    profile.append('Состояние здоровья: '+choose_rare("data/health/common_health.txt","data/health/unusual_health.txt","data/health/rare_health.txt"))
    profile.append('Хобби: '+choose_rare("data/hobby/common_hobby.txt","data/hobby/unusual_hobby.txt","data/hobby/rare_hobby.txt"))
    profile.append('Черта характера: '+random.choice(load_array("data/personality.txt")))
    profile.append('Факт: '+choose_rare("data/fact/common_fact.txt","data/fact/unusual_fact.txt","data/fact/rare_fact.txt"))
    profile.append('Багаж: '+choose_rare("data/bagage/common_bagage.txt","data/bagage/unusual_bagage.txt","data/bagage/rare_bagage.txt"))
    profile.append('Карта условия: '+random.choice(load_array("data/condition.txt")))
    if __name__ == "__main__": print(profile)
    return Player(x, y, "Player", profile)

if __name__ == "__main__":
    create_player(100, 100, 1)