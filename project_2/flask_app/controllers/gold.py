from flask_app import app
from flask import render_template, request, redirect, session
from random import randrange
from datetime import datetime

@app.route('/dashboard')
def indexPage():
    if "gold" not in session:
        session["gold"] = 0
        session["activities"] = []
        session["count"] = 0
    return render_template('dashboard.html')


@app.route('/reset', methods=["POST"])
def reset():
    session['gold'] = 0
    session["activities"] = []
    session["count"] = 0
    return redirect('/dashboard')


@app.route('/process', methods=["POST"])
def submitForm():
    human = request.form['human']
    if human == 'guard':
        gold = randrange(10, 21)
    if human == 'farmer':
        gold = randrange(5, 11)
    if human == 'man':
        gold = randrange(2, 6)
    if human == 'casino':
        gold = randrange(-50, 51)
    session["gold"] += gold
    session["count"] += 1
    now = datetime.now()
    current_time = now.strftime("%D %H: %M: %S")

    if gold > 0:
        session["activities"].insert(0, {"gold": gold, "human": human, "time": current_time, "earn": "true"})
    else:
        session["activities"].insert(0, {"gold": abs(gold), "human": human, "time": current_time, "earn": "false"})

    return redirect('/dashboard')
