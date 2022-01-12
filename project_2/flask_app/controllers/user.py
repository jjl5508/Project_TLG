from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def asd():
    data = {
        'id':session['user_id']
    }
    loggeduser = User.get_user_by_id(data)
    return render_template('dashboard.html', user = loggeduser)
    
@app.route('/register', methods = ['POST'])
def register():
    print(request.form['username'])
    if not User.validate_registration(request.form):
        return redirect('/')

    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_password, "testhash")
    data = {
        "username": request.form["username"],
        "password":hashed_password,
        "email": request.form["email"]
    }

    session['user_id'] = User.save(data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    login_validation = User.validate_login(request.form)
    # print(login_validation, "======")
    if not login_validation:
        redirect('/')
    print(request.form['password'], "////////////")
    if not bcrypt.check_password_hash(login_validation['password'],request.form['password']):
        flash("Invalid email/password", "login_email")
        return redirect("/")
    session['user_id'] = login_validation['id']
    return redirect('/dashboard')