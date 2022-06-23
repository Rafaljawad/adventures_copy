from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models import user,adventure


@app.route('/dashboard')
def show_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={'id':session['user_id']}
        all_user_adventures=user.User.get_user_by_id(data)
        return render_template('dashboard.html',all_user_adventures=all_user_adventures)


@app.route('/adventure/new',methods=['POST','GET'])
def show_advnture_page():
    if request.method=='GET':
        if 'user_id' in session:
            return render_template('new_adventure.html')
    if request.method=='POST':
        if 'user_id' not in session:
            return redirect('/')
        if adventure.Adventure.create_new_adventure(request.form):
            return redirect('/dashboard')
        else:
            return render_template('new_adventure.html')#this if the validation came flase so go to same page and flash error message.


#show_all_adventures by user--->joining two tables
@app.route('/show/all/adventures')
def show_all_adventures():
    if 'user_id' not in session:
            return redirect('/')

    all_adventures=adventure.Adventure.get_all_adventures()
    return render_template('show_all_adventutres.html',all_adventures=all_adventures)

#show adventures by the user who is not login in
@app.route('/show/adventure/<int:id>')
def get_user_who_not_lgin(id):
    this_adventure=adventure.Adventure.get_adventure_by_id(id)
    return render_template('show_with_no_delete.html',this_adventure=this_adventure)


#edit adventure
@app.route('/adventure/edit/<int:id>',methods=['POST','GET'])
def edit_adventure(id):
    if request.method=='GET':
        if 'user_id' not in session:
            return redirect('/')
        this_adventure=adventure.Adventure.get_adventure_by_id(id)
        return render_template('edit_adventure.html',this_adventure=this_adventure)
    data={
            'id':id,
            'title':request.form['title'],
            'place':request.form['place'],
            'date':request.form['date'],
            'description':request.form['description']
        }
    if adventure.Adventure.update_adventur_by_id(data)==None:
        return redirect('/dashboard')
    return render_template('edit_adventure.html')



@app.route('/adventure/delete/<int:id>')
def destroy_adventure(id):
    this_adventure=adventure.Adventure.get_adventure_by_id(id)
    if this_adventure.user_id==session['user_id']:#this condition for protecting our route(if user_id inside this_adventure == session[user_id])just in this case , delete .otherwise just return that you can not delete it 
        adventure.Adventure.delete_adventure_by_id(id)
        return redirect('/dashboard')
    else:
        return "you do not have the permision to delete"

