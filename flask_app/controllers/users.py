

from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models import user,adventure

#our home page route
@app.route('/')
def home():
    return render_template('reg_form.html')

#route for creating user and it has to match form action route
@app.route('/users/regestration',methods=['POST'])
def user_sign_up():
    #first check if create method came false so redirct to route / which has the form with flash messaeges
    if not user.User.create_new_user(request.form):
        return redirect('/')
    else:# if create user function came true so will redirect to route that displays user on profile
        return redirect('/dashboard')

#login route
@app.route('/users/login',methods=['POST'])
def log_in():
    if user.User.login(request.form):
        return redirect('/dashboard')
    #otherwise
    return redirect('/')

#log out from our page 
@app.route('/users/logout')
def log_out():
    session.clear()#it will clear user_id from session
    return redirect('/')

