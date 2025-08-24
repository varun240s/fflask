from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask import send_from_directory
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
def home():
    todo = Todo(title="first Todo", desc = "Start investing in stock market")
    db.session.add(todo)
    db.session.commit()
    return render_template('index.html')

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about/')
def about():
    return 'The about page'
    
@app.route('/download')
def download_pdf():
    return send_from_directory('static', 'res.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
 