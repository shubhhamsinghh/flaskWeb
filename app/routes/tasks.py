from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task
from app.middleware import auth

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@auth
def view_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html',tasks=tasks)

@tasks_bp.route('/add',methods=["POST"])
@auth
def add_tasks():
   if 'user' not in session:
       return redirect(url_for('auth.login'))
   title = request.form.get('title')
   if title:
       new_task = Task(title=title, status="Pending")
       db.session.add(new_task)
       db.session.commit()
       flash('Task Added Successfully','success')

   return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>',methods=['POST'])
@auth
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Done"
        else:
            task.status = "Pending"
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear',methods=['POST'])
@auth
def clear_task():
    Task.query.delete()
    db.session.commit()
    flash('Clear All Tasks','success')
    return redirect(url_for('tasks.view_tasks'))
