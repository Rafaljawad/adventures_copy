
from unittest import result
from flask_app.config.mysqlconnection import MySQLConnection,connectToMySQL
from flask_app import app
from flask_app.models import adventure
from flask import flash,session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 



class User:
    DB='adventure_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.adventures=[]

    #CREATE ----SQL----MODELS
    @classmethod
    def create_new_user(cls,data):

        if not cls.validate_user_reg_data(data):
            # print("I am not valid data ^^^^^^^^^^^^^^^^^^") #refrence to see how my data looks like
            return False
        else:
            data=cls.parse_regestration_data(data)
            query="""INSERT INTO users (first_name,last_name,email,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
            ;"""
            #running this query will give us user id so I called the variable user_id to be more descriptive
            user_id=connectToMySQL(cls.DB).query_db(query,data)
            # print("&&&&&&&&",user_id)
            session['user_id']=user_id
            return user_id
            #after creating new user now its ti,e to go to controller.

    #READ ----SQL----MODELS
    # get_one user by email to make sure if the email already in use or not
    @classmethod
    def get_user_by_email(cls,email):
        data={'email':email}
        query="""
        SELECT * FROM users WHERE email=%(email)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        if result:
            result=cls(result[0])


    #GET USER BY ID WILL HELP US TO DISPLAY THE NAME IN DASHBOARD
    # @classmethod
    # def get_user_by_id(cls,id):
    #     data={'id':id}
    #     query="""
    #     SELECT * FROM users
    #     WHERE id=%(id)s
    #     ;"""
    #     result=connectToMySQL(cls.DB).query_db(query,data)
    #     if result:
    #         result=cls(result[0])
    #     return result


    #get user's adventures
    @classmethod
    def get_user_by_id(cls,data):
        query="""
        SELECT * FROM users 
        LEFT JOIN adventures
        ON users.id=adventures.user_id
        WHERE users.id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        print("&&&&&&&&&&&&&&&&&&&& result",result)
        this_user=cls(result[0])
        print("mmmmmmm",this_user)
        for this_adventure in result:
            data={
                'id':this_adventure['adventures.id'],
                'title':this_adventure['title'],
                'place':this_adventure['place'],
                'date':this_adventure['date'],
                'user_id':this_adventure['user_id'],
                'description':this_adventure['description'],
                'created_at':this_adventure['adventures.created_at'],
                'updated_at':this_adventure['adventures.updated_at']
            }
            this_user.adventures.append(adventure.Adventure(data))
        return this_user





#static method for valdiation USER
    @staticmethod
    def validate_user_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #this regulaer exp for making sure the email must have charecters like letters and @ nd dot ...etc
        PASSWORD_REGEX=re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')#this regular exp for making sure the password must has one uppercase and one lower and one number
        is_valid = True # we assume this is true
        #validate our email to see if its in correct format
        if not EMAIL_REGEX.match(data['email']):
            flash("Use a real email")
            is_valid=False
        #validate email adress again to make sure it is not already used, this is done by using query select * from users where users.email=email
        #will go up and create class methode get_user_by_email()... for selecting users by email if it comes with email we will flash error message here , if it comes empty thats mean no error , go and create email
        # now after creating get _user_by_email method will call it here if the result came true.
        if User.get_user_by_email(data['email'].lower()):#lower function here for preventing duplicate emails if we insert by mistake uppercase and lower case , so in this case all leteeres will converted to uppercase.
            flash("Email already in use, insert another email adress")
            is_valid=False
        #validat first_name to make sure it is more than 3 chareters
        if len(data['first_name']) < 2:
            flash("first_Name must be at least 3 or more characters.")
            is_valid = False
        #validata last_name to make sure it is 3 charecters or more than 3 chareters
        if len(data['last_name']) < 2:
            flash("last_name must be at least 3 or more characters.")
            is_valid = False
        #validate password to make sure its more than 8 charecters
        if len(data['password'])<8:
            flash("your password must contain at least 2 charecters")
            is_valid=False
        #validate password again to make sure it matches the confirm password
        if data['password']!=data['confirm_password']:
            flash("passord do not match")
            is_valid=False
        #validate password to make sure the password must has one uppercase and one lower and one number
        if not PASSWORD_REGEX.match(data['password']):
            flash("password should contains at least one uppercase and one lowercase and one number")
            is_valid=False
        return is_valid

        #after finishing validating all user info now its time to create our user and in this case we need to create class method on the top .


#static method for parsed data to hashed our password (the data coming from form are plain as we inserted and to hash the password before passing it to db ,we need to hash it so, it will appear as a random charecters in db , to do so will create pased function with parsed empty dictionary like below:)
    @staticmethod
    def parse_regestration_data(data):
        parsed_data={}
        parsed_data['email']=data['email'].lower()#the data I give you find the key and set its value
        parsed_data['password']=bcrypt.generate_password_hash(data['password'])
        parsed_data['first_name']=data['first_name']
        parsed_data['last_name']=data['last_name']
        return parsed_data
        #now we have to go to top and call this function to hash password before creating user
        
    #method for login
    @staticmethod
    def login(data):
        # will check if the email came from db so we will check if the password matches 
        user=User.get_user_by_email(data['email'].lower())
        if user :
            if bcrypt.check_password_hash(user.password,data['password']):
                session['user_id']=user.id#store the user id that came with email into session
                session['first_name']=user.first_name
                session['last_name']=user.last_name#we stored both first and last name in session so in this case when go to dashboard or edit page , we do not need to calll get user by id and pass it with render template to display it on the screen.


                return True
        #if no thing back from method get_user_by_email:
        flash("invalid either email adress or password")
        return False

