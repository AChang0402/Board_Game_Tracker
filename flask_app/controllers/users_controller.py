from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login_register')
def login_reg():
    return render_template("login_reg.html")

@app.route('/register', methods=['post'])
def register_user():
    if not User.validate(request.form):
        return redirect('/login_register')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        **request.form,
        'password': pw_hash
    }
    id = User.create_user(user_data)

    session['id'] = id
    session['username']=request.form['username']
    return redirect('/')


@app.route('/login', methods=['post'])
def login_user():
    user = User.get_one_by_username(request.form)
    if not user:
        flash("Invalid credentials.", "login")
        return redirect('/login_register')
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials.", "login")
        return redirect('/login_register')
    
    session['id'] = user.id
    session['username'] = user.username
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')