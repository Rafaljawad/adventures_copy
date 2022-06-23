from flask_app.config.mysqlconnection import MySQLConnection,connectToMySQL
from flask_app import app
from flask import flash,session
from flask_app.models import user



class Adventure:
    DB='adventure_schema'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.place = data['place']
        self.date = data['date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id=data['user_id']
        self.creator=None

    #CRUD  
    #CREATE___________MODELS________SQL

    @classmethod
    def create_new_adventure(cls,data):
        if not cls.validate_adventure(data):
            # print("I am not valid data ^^^^^^^^^^^^^^^^^^") #refrence to see how my data looks like
            return False
        else:
            query="""
            INSERT INTO adventures (title,place,date,description,user_id)
            VALUES (%(title)s,%(place)s,%(date)s,%(description)s,%(user_id)s)
            ;"""
            result=connectToMySQL(cls.DB).query_db(query,data)
            return result

    #READ___________MODELS________SQL

    @classmethod
    def get_adventure_by_id(cls,id):
        data={'id':id}
        query="""SELECT * FROM adventures WHERE id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        if result:
            result=cls(result[0])
        return result
    #get all adventures in db 
    @classmethod
    def get_all_adventures(cls):
        query="""
        SELECT * FROM adventures
        JOIN users
        ON adventures.user_id=users.id
        ;"""
        result=connectToMySQL(cls.DB).query_db(query)
        print("//////////////////",result)#this will give me list of dictionary which has all users info and their adventurs
        all_adventures=[]#create empty list to append all adventures and users info to it
        if not result:
            return result
        for this_adventure in result:
            new_adventure=cls(this_adventure)#create instance of adventures and it will ignor user thats why we need to create dictionary for users table info
            user_data={
                'id':this_adventure['users.id'],
                'first_name':this_adventure['first_name'],
                'last_name':this_adventure['last_name'],
                'email':this_adventure['email'],
                'password':this_adventure['password'],
                'created_at':this_adventure['users.created_at'],
                'updated_at':this_adventure['users.updated_at'],
            }
            new_adventure.creator=user.User(user_data)#go to user class and pass users data to get instance of user and save it into new_adventure.creator
            all_adventures.append(new_adventure)
        return all_adventures




    #UPDATE___________MODELS________SQL
    @classmethod
    def update_adventur_by_id(cls,data):
        if not cls.validate_adventure(data):
            # print("I am not valid data ^^^^^^^^^^^^^^^^^^") #refrence to see how my data looks like
            return False
        query="""
        UPDATE adventures SET title=%(title)s,place=%(place)s,date=%(date)s,description=%(description)s
        WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    #DELETE___________MODELS________SQL

    @classmethod
    def delete_adventure_by_id(cls,id):
        data={'id':id}
        query="""
        DELETE FROM adventures
        WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    


#static method for valdiation ADVENTURE
    @staticmethod
    def validate_adventure(data):
        is_valid=True
        if len(data['title']) < 3:
            flash("Name must be at least 3 or more characters.")
            is_valid = False

        if len(data['description'])<3:
            flash("description must be at least 3 or more characters")
            is_valid=False
        if not data['place']:
            flash("you must choose a place ")
            is_valid=False
        if  data['date']=="":
            flash("You must select date")
            is_valid=False
        return is_valid