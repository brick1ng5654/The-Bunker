from random import randint
import random
import os

CPERCENT = 65
UPERCENT = 25

class Player:
    def __init__(self, name, characteristics):
        self.name = name
        self.characteristics = characteristics
        self.num_characteristics = len(characteristics)
        self.number = int(name.split('_')[1])

    def print_characteristics(self):
        print(self.characteristics)

    def save_player_data(self):
        os.makedirs('data/players', exist_ok=True)
        with open(f'data/players/{self.name}.txt', 'w', encoding='utf-8') as f:
            for line in self.characteristics:
                f.write(line + '\n')

    @classmethod
    def load_player_data(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f]
        name = lines[0].replace('КАРТОЧКА ИГРОКА ', 'player_')
        characteristics = lines[1:]
        return cls(name, characteristics)
    
def load_characteristic(filename1, filename2, filename3, multiply):
    if multiply == 0:
        characteristic = [a.strip() for a in open(filename1, 'r', encoding='utf-8')]
        return characteristic
    common = [x.strip() for x in open(filename1, 'r', encoding='utf-8')]
    unusual = [y.strip() for y in open(filename2, 'r', encoding='utf-8')]
    rare = [z.strip() for z in open(filename3, 'r', encoding='utf-8')]
    characteristic = [common, unusual, rare]
    return characteristic

def pick(characteristic, to_delete, multiply):
    if multiply == 1:
        i = randint(1, 100)
        if i <= CPERCENT:
            k = 0
        elif i <= CPERCENT + UPERCENT:
            k = 1
        else:
            k = 2
        value = random.choice(characteristic[k])
        if to_delete == 1:
            characteristic[k].remove(value)
    else:
        value = random.choice(characteristic)
        if to_delete == 1:
            characteristic.remove(value)
    return value

def load_array():
    age_array = load_characteristic("data/age/common_age.txt", "data/age/unusual_age.txt", "data/age/rare_age.txt", 1)
    bagage_array = load_characteristic("data/bagage/common_bagage.txt", "data/bagage/unusual_bagage.txt", "data/bagage/rare_bagage.txt", 1)
    fact_array = load_characteristic("data/fact/common_fact.txt", "data/fact/unusual_fact.txt", "data/fact/rare_fact.txt", 1)
    gender_array = load_characteristic("data/gender/common_gender.txt", "data/gender/unusual_gender.txt", "data/gender/rare_gender.txt", 1)
    health_array = load_characteristic("data/health/common_health.txt", "data/health/unusual_health.txt", "data/health/rare_health.txt", 1)
    hobby_array = load_characteristic("data/hobby/common_hobby.txt", "data/hobby/unusual_hobby.txt", "data/hobby/rare_hobby.txt", 1)
    job_array = load_characteristic("data/job/common_job.txt", "data/job/unusual_job.txt", "data/job/rare_job.txt", 1)
    sex_array = load_characteristic("data/sex/common_sex.txt", "data/sex/unusual_sex.txt", "data/sex/rare_sex.txt", 1)
    action_array = load_characteristic("data/action.txt", "", "", 0)
    condition_array = load_characteristic("data/condition.txt", "", "", 0)
    fobia_array = load_characteristic("data/fobia.txt", "", "", 0)
    knowledge_array = load_characteristic("data/knowledge.txt", "", "", 0)
    personality_array = load_characteristic("data/personality.txt", "", "", 0)
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

def create_player(n, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition):
    profile = [
        f'КАРТОЧКА ИГРОКА {n}',
        f'Био-характеристика: {sex} / Возраст {age}',
        f'Ориентация: {gender}',
        f'Род деятельности: {job}',
        f'Состояние здоровья: {health}',
        f'Фобия: {fobia}',
        f'Черта характера: {personality}',
        f'Хобби: {hobby}',
        f'Знание: {knowledge}',
        f'Доп. информация: {fact}',
        f'Багаж: {bagage}',
        f'Карта действия: {action}',
        f'Карта условия: {condition}'
    ]
    return Player(f"player_{n}", profile)

def new_game(n):
    data = load_array()
    players = []
    for i in range(1, n + 1):
        sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition = pick_value(data)
        player = create_player(i, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition)
        players.append(player)
        player.save_player_data()

if __name__ == "__main__":
    data = load_array()
    sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition = pick_value(data)
    player1 = create_player(1, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition)
    player1.print_characteristics()
    player1.save_player_data()