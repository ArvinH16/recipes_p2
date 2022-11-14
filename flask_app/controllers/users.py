from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.user import recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.register(data)
    session['user_id'] = user_id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    
    if not User.validate_login(request.form):
        return redirect('/')
    
    user = User.check_combination(request.form)
    
    if user == False:
        flash("invalid email or password", 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("invalid email or password", 'login')
        return redirect('/')
            
    
    session['user_id'] = user.id
    return redirect('/dashboard')


