from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.user import recipe

@app.route('/dashboard')
def dashboard():
    
    data = {
        'id': session['user_id']
    }
    
    user = User.get_user(data)

    
    return render_template('dashboard.html', user = user)