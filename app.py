from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import cProfile


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(100))




@app.route("/")
def index():
    todoList = Todo.query.all()
    print(todoList)
    return render_template('base.html', todoList=todoList)

@app.route("/addItems", methods=["POST"])
def add():
    item = request.form.get("title")
    newTodo = Todo(item=item)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/remove", methods=["POST"])
def remove():
    num = int(request.form.get("del")) 
    todo = Todo.query.filter_by(id=num).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

def runApp():
    app.run(debug=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    runApp()
    