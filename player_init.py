import random
from random import randint
import pygame

# Константы
PLAYER_SIZE = 100
PLAYER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
CPERCENT = 50
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

        # Drawing the name
        y_offset += draw_text(self.name, 200, 10 + y_offset, 350, font, TEXT_COLOR) + 5

        # Drawing the characteristics
        for characteristic in self.characteristics:
            y_offset += draw_text(characteristic, 1200, 10 + y_offset, 400, font, TEXT_COLOR) + 5

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

def create_player(x, y):
    profile = []
    profile.append('КАРТОЧКА ИГРОКА')
    profile.append('Био-характеристика: '+choose_rare("data/gender/common_gender.txt","data/gender/unusual_gender.txt","data/gender/rare_gender.txt")+' / Возраст '+choose_rare("data/age/common_age.txt","data/age/unusual_age.txt","data/age/rare_age.txt"))
    profile.append('Состояние здоровья: '+choose_rare("data/health/common_health.txt","data/health/unusual_health.txt","data/health/rare_health.txt"))
    profile.append('Черта характера: '+random.choice(load_array("data/personality.txt")))
    profile.append('Карта условия: '+random.choice(load_array("data/condition.txt")))
    if __name__ == "__main__": print(profile)
    return Player(x, y, "Player", profile)

if __name__ == "__main__":
    create_player(100, 100)