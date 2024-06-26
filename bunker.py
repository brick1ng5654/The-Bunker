from player import load_characteristic, pick
import random
import os

def save_data(data):
    with open('data/bunker.txt', 'w', encoding='utf-8') as f:
            for line in data:
                f.write(line + '\n')

def create_bunker(n):
    bunker =[]
    bunker.append('Информация о бункере')
    with open('data/bunker/disaster.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        disaster = random.choice(lines).strip()
        bunker.append(disaster)
        image_path = os.path.join('data/bunker/images', f'{disaster.split(':')[0]}.jpg')
    with open('data/bunker/size.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        size = random.choice(lines).strip()
        bunker.append(size)
    with open('data/bunker/duration.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        duration = random.choice(lines).strip()
        bunker.append(duration)
    if(n<=8):
        with open('data/bunker/rooms.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            room1, room2 = random.choice(lines).strip(), random.choice(lines).strip()
            bunker.append('Комнаты: '+room1+' / '+room2)
    else:
        with open('data/bunker/rooms.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            room1, room2, room3 = random.choice(lines).strip(), random.choice(lines).strip(), random.choice(lines).strip()
            bunker.append('Комнаты: '+room1+' / '+room2+' / '+room3)
    bunker.append('Количество мест: '+str(int(n//2)))
    

    if(__name__ == "__main__"): print(bunker)
    save_data(bunker)
    return bunker, image_path

if __name__ == "__main__":
    create_bunker(10)