from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl
from flask import render_template, flash, request, redirect, url_for # Added redirect import
from application import db
from application import app
from .forms import TodoForm
from datetime import datetime
from bson import ObjectId

@app.route("/")
def get_todos():
    todos = []
    for todo in db.todo_flask.find().sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("views_todos.html", title="layout page", todos=todos)

@app.route("/add_todo", methods=['POST', 'GET'])  # Fixed route definition
def add_todo():
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo_flask.insert_one({
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", 'success')
        return redirect('/')
    else:
        form = TodoForm()
    return render_template("add_todo.html", form = form)



@app.route("/delete_todo/<id>")
def delete_todo(id):
    result = db.todo_flask.find_one_and_delete({"_id": ObjectId(id)})
    if result:
        flash("Todo successfully deleted", "success")
    else:
        flash("Todo not found", "error")
    return redirect("/")

from flask import abort

@app.route("/update_todo/<id>", methods=['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todo_flask.find_one({"_id": ObjectId(id)})
        if not todo:
            abort(404)

        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)

    return render_template("add_todo.html", form=form)