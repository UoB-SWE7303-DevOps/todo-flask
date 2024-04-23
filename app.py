
from flask import Flask, render_template, request, url_for, redirect 
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


# Create client and db
client = MongoClient('localhost', 27017)
db = client.task_database 
todos = db.todos 


# Get and Post 
@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == "POST":  
        task = request.form['task']
        degree = request.form['degree']
        todos.insert_one({'task': task, 'degree': degree, 'complete': False})
        return redirect(url_for('index')) 
    all_todos = todos.find()   
    
    return render_template('index.html', todos = all_todos)

@app.route("/<id>/edit/", methods=('GET', 'POST'))
def edit(id):
    todo = todos.find_one({"_id": ObjectId(id)})
    
    if request.method == 'POST':
        new_task = request.form['task']
        new_degree = request.form['degree']
        todos.update_one({"_id": ObjectId(id)}, {"$set": {'task': new_task, 'degree': new_degree}})
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)
#Delete 
@app.post("/<id>/delete/")
def delete(id): 
    todos.delete_one({"_id":ObjectId(id)}) 
    return redirect(url_for('index')) 


# Complete
@app.route("/<id>/complete/", methods=['GET'])
def complete(id):
    todo = todos.find_one({"_id": ObjectId(id)})
    todos.update_one({"_id": ObjectId(id)}, {"$set": {'complete': not todo['complete']}})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)# the server will automatically reload for code changes and show a debugger in case an exception happened.