from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def register(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, `password`) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('recipes_p2').query_db(query, data)
        return result

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recipes_p2').query_db(query, data)
        return cls(result[0])

    @classmethod
    def check_combination(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recipes_p2').query_db(query, data)
        if len(result) < 1:
            return False
        elif len(result) == 1:
            user = cls(result[0])
        
        return user
        
    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("first name needs to be at least 2 characters long", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("last name needs to be at least 2 characters long", 'register')
            is_valid = False    
        if len(user['email']) < 1:
            flash("email field is required", 'register')
            is_valid = False
        if len(user['password']) < 1:
            flash("password field is required", 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email", 'register')
            is_valid = False

        if user['password'] != user['pass_confirm']:
            flash("Passwords not matching", 'register')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True

        if len(user['email']) < 1:
            flash('email field is required', 'login')
            is_valid = False
        if len(user['password']) < 8:
            flash('password field needs to be 8 characters long', 'login')

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email", 'login')
            is_valid = False

        return is_valid
