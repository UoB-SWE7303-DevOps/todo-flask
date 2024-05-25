import os
from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

#THERE IS NO REQUIREMENTS FILE hange

app = Flask(__name__)

# Create client and db
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.task_database 
todos_collection = db.todos 
users = db.users

app.secret_key = 'mysecret'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
            users.insert_one({'username': request.form['username'], 'password': hashpass})
            return redirect(url_for('login'))
        
        return 'You are already logged in'
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                session['user_id'] = str(login_user['_id'])
                return redirect(url_for('todos'))

        return 'Invalid username/password combination'

    return render_template('login.html')


# Get and Post 
@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['task']
            degree = request.form['degree']
            todos_collection.insert_one({'task': title, 'degree': degree, 'complete': False, 'user_id': session['user_id']})
            return redirect(url_for('todos'))

        user_todos = todos_collection.find({'user_id': session['user_id']})
        return render_template('index.html', todos=user_todos)
    else:
        return redirect(url_for('login'))

@app.route("/<id>/edit/", methods=('GET', 'POST'))
def edit(id):
    todo = todos_collection.find_one({"_id": ObjectId(id)})
    
    if request.method == 'POST':
        new_task = request.form['task']
        new_degree = request.form['degree']
        todos_collection.update_one({"_id": ObjectId(id)}, {"$set": {'task': new_task, 'degree': new_degree}})
        return redirect(url_for('todos'))
    
    return render_template('edit.html', todo=todo)
#Delete 
@app.post("/<id>/delete/")
def delete(id): 
    todos_collection.delete_one({"_id":ObjectId(id)}) 
    return redirect(url_for('todos')) 


# Complete
@app.route("/<id>/complete/", methods=['GET'])
def complete(id):
    todo = todos_collection.find_one({"_id": ObjectId(id)})
    new_status = not todo['complete']
    todos_collection.update_one({"_id": ObjectId(id)}, {"$set": {'complete': not todo['complete']}})
    return redirect(url_for('todos'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the session
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))
