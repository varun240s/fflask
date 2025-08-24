from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory, request, redirect, url_for
from datetime import datetime


# # name of the application module
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Todo('{self.sno}', '{self.title}', '{self.date_created}')"

@app.route('/')
def hello_world():
    all_Todo = Todo.query.all()
    return render_template('index.html', allTodo=all_Todo)

@app.route('/show')
def projects():
    allTodo = Todo.query.all()
    print(allTodo)
    return "The Todo's Page page"

@app.route('/about/')
def about():
    return 'The about page'

# Create Todo
@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    desc = request.form['desc']
    todo = Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

# Update Todo
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update_todo(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('update.html', todo=todo)

# Delete Todo
@app.route('/delete/<int:sno>')
def delete_todo(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))
    
@app.route('/download')
def download_pdf():
    return send_from_directory('static', 'res.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
 