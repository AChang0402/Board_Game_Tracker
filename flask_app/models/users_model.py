from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

DATABASE = "board_game_tracker_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, username, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * from users WHERE email=%(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_by_username(cls, data):
        query = "SELECT * from users WHERE username=%(username)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * from users WHERE id=%(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_all_but_one (cls, data):
        query = "SELECT * from users WHERE email != %(email)s ORDER BY first_name asc;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        all_but_one=[]
        for row in results:
            all_but_one.append(cls(row))
        return all_but_one

        
    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['first_name'])<2 or not data['first_name'].isalpha():
            flash("First Name must contain at least 2 characters/can only contain letters.", "reg")
            is_valid=False
        if len(data['last_name'])<2 or not data['last_name'].isalpha():
            flash("Last Name must contain at least 2 characters/can only contain letters.", "reg")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.", "reg")
            is_valid=False
        elif User.get_one_by_email({'email':data['email']}):
            flash("Email address associated with registered account.", "reg")
            is_valid=False
        if len(data['username'])<8:
            flash("Username must contain at least 8 characters.", "reg")
            is_valid=False
        elif User.get_one_by_username({'username':data['username']}):
            flash("Username already taken.", "reg")
            is_valid=False
        if len(data['password'])<8:
            flash("Password must be at least 8 characters.", "reg")
            is_valid=False
        elif not User.contain_numupper(data['password']):
            flash("Password must contain at least 1 uppercase letter and number.", "reg")
            is_valid=False
        elif not data['password'] == data['password_confirm']:
            flash("Confirmed Password does not match.", "reg")
            is_valid=False
        return is_valid
    
    @staticmethod
    def contain_numupper(str):
        num = False
        upper = False
        for i in range(len(str)):
            if str[i].isdigit():
                num = True
            if str[i].isupper():
                upper = True
        return num and upper
