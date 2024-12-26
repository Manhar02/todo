from datetime import datetime
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def Hello_world():
    if request.method == 'POST':
        title_0 = request.form['title']
        desc_0 = request.form["desc"]

        todo = Todo(title = title_0,desc = desc_0)
        db.session.add(todo)
        db.session.commit()

    all_todo = Todo.query.all()
    return render_template("index.html",allTodo=all_todo)
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title_0 = request.form['title']
        desc_0 = request.form["desc"]

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title_0
        todo.desc = desc_0
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno = sno).first()
    return render_template("update.html" , Todo = todo)

@app.route('/delete/<int:sno>', methods=['GET','POST'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/About')
def About():
    return render_template("About.html" )

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = False,port =1000)