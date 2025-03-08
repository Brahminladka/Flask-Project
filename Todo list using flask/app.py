from flask import Flask, render_template, redirect, url_for
from models import db, Todo  # Import models after defining the app
from forms import TodoForm

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)  # Initialize database with the app

@app.route("/", methods=["GET", "POST"])
def index():
    form = TodoForm()
    if form.validate_on_submit():
        new_task = Todo(task=form.task.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    
    tasks = Todo.query.all()
    return render_template("index.html", form=form, tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Todo.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route("/complete/<int:task_id>")
def complete(task_id):
    task = Todo.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ Now this will work correctly!
    app.run(debug=True)
