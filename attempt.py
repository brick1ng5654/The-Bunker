from player import *
import os

def clear_players_data():
    file_path = 'players/player_{n}'
    for i in range(1, 13):
        try:
            os.remove(f'players/player_{i}.txt')
        except:
            break
        
clear_players_data()
n = int(input('Введите количество игроков: '))
data = load_array()
players = []

for i in range(1, n + 1):
    sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition = pick_value(data)
    player = create_player(i, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition)
    players.append(player)
    player.save_player_data()

def new_game(n):
    data = load_array()
    players = []
    for i in range(1, n + 1):
        sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition = pick_value(data)
        player = create_player(i, sex, age, gender, job, health, fobia, personality, hobby, knowledge, fact, bagage, action, condition)
        players.append(player)
        player.save_player_data()