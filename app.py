from flask import Flask, request, redirect, url_for, render_template, session, flash
from random import randint


app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        session['character'] = {
            'User Name': request.form['username'],
            'Race': request.form['race'],
            'Class': request.form['class'],
            'Attack': randint(1, 6),  
            'HP': randint(1, 10)     
        }
        return redirect(url_for('game_menu'))
    return render_template('create_character.html')

@app.route('/game_menu')
def game_menu():
    if 'character' not in session:
        return redirect(url_for('index'))
    return render_template('game_menu.html', character=session['character'])

@app.route('/logout')
def logout():
    session.pop('character', None)
    return redirect(url_for('index'))

@app.route('/view_character')
def view_character():
    if 'character' not in session:
        return redirect(url_for('index'))
    return render_template('view_character.html', character=session['character'])

@app.route('/inventory')
def inventory():
    if 'character' not in session:
        return redirect(url_for('index'))
    character = session['character']
    inventory = character.get('Inventory', [])
    return render_template('inventory.html', inventory=inventory)

@app.route('/fight')
def fight():
    if 'character' not in session:
        return redirect(url_for('index'))
    # Simple fight logic
    monster_attack = randint(1, 8)
    character_attack = session['character']['Attack']
    if character_attack >= monster_attack:
        session['character'].setdefault('Inventory', []).append('Monster Loot')
        message = "You defeated the monster and found some loot!"
    else:
        message = "You were defeated by the monster but managed to escape."
    return render_template('fight.html', message=message)

@app.route('/heal', methods=['GET', 'POST'])
def heal():
    if 'character' not in session:
        return redirect(url_for('index'))
    session['character']['HP'] += 10  
    flash('You have been healed. +10 HP')
    return redirect(url_for('game_menu'))

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if 'character' not in session:
        return redirect(url_for('index'))
    # Simple buying logic
    session['character'].setdefault('Inventory', []).append('Healing Potion')
    flash('You bought a Healing Potion.')
    return redirect(url_for('game_menu'))

if __name__ == '__main__':
    app.run(debug=True)
