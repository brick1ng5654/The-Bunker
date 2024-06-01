import random
from random import randint
import pygame

# Константы
PLAYER_SIZE = 100
PLAYER_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
CPERCENT = 65
UPERCENT = 25

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

    if (value): return value

def create_player():
    profile = []
    profile.append(choose_rare("cgender.txt","ugender.txt","rgender.txt"))
    print(profile)

if __name__ == "__main__":
    create_player()
