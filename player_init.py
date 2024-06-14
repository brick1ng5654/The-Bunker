import random
import pygame
from random import randint
from const import CPERCENT, UPERCENT, PLAYER_SIZE, WHITE_COLOR, font, LIGHT_GREY, BLACK_COLOR

class Player:
    def __init__(self, x, y, name, characteristics):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.name = name
        self.characteristics = characteristics
        self.characteristics_visible = [False] * len(characteristics)
        self.avatar = pygame.image.load("data/avatar.png")
        self.avatar = pygame.transform.scale(self.avatar, (PLAYER_SIZE, PLAYER_SIZE))
        self.avatar_pick = pygame.image.load("data/avatar_pick.png")
        self.avatar_pick = pygame.transform.scale(self.avatar_pick, (PLAYER_SIZE, PLAYER_SIZE))

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.avatar_pick, self.rect.topleft)
        else:
            screen.blit(self.avatar, self.rect.topleft)

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

            text_height = 0
            for line in lines:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (x, y + text_height))
                text_height += font.get_linesize()

            return text_height

        for i, characteristic in enumerate(self.characteristics):
            btn_rect = pygame.Rect(1095, 90 + y_offset, 30, 30)
            pygame.draw.rect(screen, LIGHT_GREY, btn_rect)
            pygame.draw.rect(screen, BLACK_COLOR, btn_rect, 2)

            if self.characteristics_visible[i]:
                text_height = draw_text(characteristic, 1140, 90 + y_offset, 445, font, WHITE_COLOR) + 5
                y_offset += text_height
                btn_text = "o"
            else:
                btn_text = "-"

            btn_surface = font.render(btn_text, True, BLACK_COLOR)
            btn_text_rect = btn_surface.get_rect(center=btn_rect.center)
            screen.blit(btn_surface, btn_text_rect)

            y_offset += 35

    def handle_event(self, event, font):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            y_offset = 0
            for i in range(len(self.characteristics)):
                btn_rect = pygame.Rect(1095, 90 + y_offset, 30, 30)
                if btn_rect.collidepoint(mouse_pos):
                    self.characteristics_visible[i] = not self.characteristics_visible[i]
                if self.characteristics_visible[i]:
                    words = self.characteristics[i].split()
                    lines = []
                    current_line = ""

                    for word in words:
                        test_line = current_line + word + " "
                        if font.size(test_line)[0] <= 445:
                            current_line = test_line
                        else:
                            lines.append(current_line)
                            current_line = word + " "
                    lines.append(current_line)

                    text_height = len(lines) * font.get_linesize()
                    y_offset += text_height + 5
                y_offset += 35
                
def load_characteristic(filename1, filename2, filename3, multiply):
    if(multiply == 0): 
        characteristic = [a for a in open(filename1, 'r', encoding='utf-8')]
        return characteristic
    common = [x for x in open(filename1, 'r', encoding='utf-8')]
    unusual = [y for y in open(filename2, 'r', encoding='utf-8')]
    rare = [z for z in open(filename3, 'r', encoding='utf-8')]
    characteristic = [common, unusual, rare]
    return characteristic

def pick(characteristic, to_delete, multiply):
    if(multiply == 1):
        i = randint(1,100)
        if(i<=CPERCENT): k = 0
        elif(i<=CPERCENT+UPERCENT): k = 1
        else: k = 2
        value = random.choice(characteristic[k])
        if(to_delete == 1): characteristic[k].remove(value)
    else:
        value = random.choice(characteristic)
        if(to_delete == 1): characteristic.remove(value)
    return value

def load_array():
    age_array = load_characteristic("data/age/common_age.txt","data/age/unusual_age.txt","data/age/rare_age.txt",1)
    bagage_array = load_characteristic("data/bagage/common_bagage.txt","data/bagage/unusual_bagage.txt","data/bagage/rare_bagage.txt",1)
    fact_array = load_characteristic("data/fact/common_fact.txt","data/fact/unusual_fact.txt","data/fact/rare_fact.txt",1)
    gender_array = load_characteristic("data/gender/common_gender.txt","data/gender/unusual_gender.txt","data/gender/rare_gender.txt",1)
    health_array = load_characteristic("data/health/common_health.txt","data/health/unusual_health.txt","data/health/rare_health.txt",1)
    hobby_array = load_characteristic("data/hobby/common_hobby.txt","data/hobby/unusual_hobby.txt","data/hobby/rare_hobby.txt",1)
    job_array = load_characteristic("data/job/common_job.txt","data/job/unusual_job.txt","data/job/rare_job.txt",1)
    sex_array = load_characteristic("data/sex/common_sex.txt","data/sex/unusual_sex.txt","data/sex/rare_sex.txt",1)
    action_array = load_characteristic("data/action.txt","","",0)
    condition_array = load_characteristic("data/condition.txt","","",0)
    fobia_array = load_characteristic("data/fobia.txt","","",0)
    knowledge_array = load_characteristic("data/knowledge.txt","","",0)
    personality_array = load_characteristic("data/personality.txt","","",0)
    return (age_array, bagage_array, fact_array, gender_array, health_array, hobby_array, job_array, sex_array, action_array, condition_array, fobia_array, knowledge_array, personality_array)

def pick_value(data):
    age, bagage, fact, gender, health, hobby, job, sex, action, condition, fobia, knowledge, personality = data
    age = pick(age, 1, 1)
    bagage = pick(bagage, 1, 1)
    fact = pick(fact, 1, 1)
    gender = pick(gender, 0, 1)
    health = pick(health, 0, 1)
    hobby = pick(hobby, 1, 1)
    job = pick(job, 1, 1)
    sex = pick(sex, 0, 1)
    action = pick(action, 1, 0)
    condition = pick(condition, 1, 0)
    fobia = pick(fobia, 1, 0)
    knowledge = pick(knowledge, 1, 0)
    personality = pick(personality, 1, 0)
    return sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition
    
def create_player(x, y, n, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition):
    profile = []
    profile.append('КАРТОЧКА ИГРОКА ' + str(n))
    profile.append('Био-характеристика: '+sex+' / Возраст '+age)
    profile.append('Ориентация: '+gender)
    profile.append('Род деятельности: '+job)
    profile.append('Состояние здоровья: '+health)
    profile.append('Фобия: '+fobia)
    profile.append('Черта характера: '+personality)
    profile.append('Хобби: '+hobby)
    profile.append('Знание: '+knowledge)
    profile.append('Доп. информация: '+fact)
    profile.append('Багаж: '+bagage)
    profile.append('Карта действия: '+action)
    profile.append('Карта условия: '+condition)
    if __name__ == "__main__":
        print(profile)
    return Player(x, y, f"Игрок {n}", profile)

if (__name__ == "__main__"):
    data = load_array()
    sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition = pick_value(data)
    create_player(100, 100, 1, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition)