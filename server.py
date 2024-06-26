from flask import Flask, render_template, redirect, url_for, request, session
from player import Player
import os

app = Flask(__name__, template_folder='data/templates', static_folder='static')
app.secret_key = 'supersecretkey'  # Для сессий

def load_player_data(player_id):
    filename = f'data/players/player_{player_id}.txt'
    return Player.load_player_data(filename)

def load_player_hidden_characteristics():
    # Здесь можно реализовать загрузку из БД или любого другого источника
    # В данном примере используется просто пустой словарь
    return {}

@app.route('/')
def index():
    player_files = sorted([f for f in os.listdir('data/players') if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    players = [load_player_data(f.split('_')[1].split('.')[0]) for f in player_files]
    return render_template('index.html', players=players)

@app.route('/choose_player', methods=['GET', 'POST'])
def choose_player():
    if request.method == 'POST':
        player_number = request.form.get('player_number')
        session['player_number'] = player_number
        return redirect(url_for('player', name=f'player_{player_number}'))

    player_files = sorted([f for f in os.listdir('data/players') if f.endswith('.txt')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    player_numbers = [f.split('_')[1].split('.')[0] for f in player_files]
    return render_template('choose_player.html', player_numbers=player_numbers)

@app.route('/player/<name>')
def player(name):
    player_id = name.split("_")[1]
    player = load_player_data(player_id)
    players = [load_player_data(f.split('_')[1].split('.')[0]) for f in os.listdir('data/players') if f.endswith('.txt')]

    player_hidden_characteristics = session.get('player_hidden_characteristics', {}).get(player_id, [])

    return render_template('player.html', player=player, players=players, player_hidden_characteristics=player_hidden_characteristics)

@app.route('/toggle_characteristic/<int:index>', methods=['POST'])
def toggle_characteristic(index):
    player_id = session['player_number']
    player_hidden_characteristics = session.setdefault('player_hidden_characteristics', {}).setdefault(player_id, [])

    if index in player_hidden_characteristics:
        player_hidden_characteristics.remove(index)
    else:
        player_hidden_characteristics.append(index)

    session.modified = True

    return redirect(url_for('player', name=f'player_{player_id}'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
