from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import send_from_directory, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from datetime import datetime
import os

load_dotenv()
# # name of the application module
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Dummy users
# users = {
#     "admin_user": {"password": "admin123", "role": "admin"},
#     "maintainer_user": {"password": "maintain123", "role": "maintainer"},
#     "normal_user": {"password": "user123", "role": "user"}
# }
users = {
    "admin_user": {"password": "admin123", "role": "admin"},
    "maintainer_user": {"password": "maintain123", "role": "maintainer"},
    "normal_user": {"password": "user123", "role": "user"}
}



class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(100), nullable=False)  # Store the user who created the todo

    def __repr__(self) -> str:
        return f"Todo('{self.sno}', '{self.title}', '{self.date_created}', '{self.username}')"



# Home page: show TODOs for the logged-in user only

# Serve static index.html for home page
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to get todos for logged-in user
@app.route('/api/todos', methods=['GET'])
@jwt_required()
def api_todos():
    claims = get_jwt()
    username = claims['sub']
    todos = Todo.query.filter_by(username=username).order_by(Todo.date_created.desc()).all()
    return jsonify([
        {
            'sno': todo.sno,
            'title': todo.title,
            'desc': todo.desc,
            'date_created': todo.date_created.strftime('%Y-%m-%d %H:%M:%S')
        } for todo in todos
    ])

@app.route('/login-page')
def login_page():
    return render_template('login.html')


@app.route('/show')
def projects():
    allTodo = Todo.query.all()
    print(allTodo)
    return "The Todo's Page page"

@app.route('/about/')
def about():
    return 'The about page'

# Create Todo (for logged-in user)
@app.route('/add', methods=['POST'])
@jwt_required()
def add_todo():
    claims = get_jwt()
    username = claims['sub']
    title = request.form['title']
    desc = request.form['desc']
    todo = Todo(title=title, desc=desc, username=username)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('home'))

# Update Todo (only if owner)
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
@jwt_required()
def update_todo(sno):
    claims = get_jwt()
    username = claims['sub']
    todo = Todo.query.get_or_404(sno)
    if todo.username != username:
        return "Unauthorized", 403
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('update.html', todo=todo)

# Delete Todo (only if owner)
@app.route('/delete/<int:sno>')
@jwt_required()
def delete_todo(sno):
    claims = get_jwt()
    username = claims['sub']
    todo = Todo.query.get_or_404(sno)
    if todo.username != username:
        return "Unauthorized", 403
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/download')
def download_pdf():
    return send_from_directory('static', 'res.pdf', as_attachment=True)

# Login Route
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username not in users or users[username]["password"] != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    role = users[username]["role"]
    token = create_access_token(identity=username, additional_claims={"role": role})
    return jsonify(access_token=token)

# Role-based Protected Route
@app.route("/admin-only", methods=["GET"])
@jwt_required()
def admin_only():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"msg": "Admins only!"}), 403
    return jsonify(msg="Welcome, Admin!")

@app.route("/maintainer-only", methods=["GET"])
@jwt_required()
def maintainer_only():
    claims = get_jwt()
    if claims.get("role") not in ["maintainer", "admin"]:
        return jsonify({"msg": "Maintainers only!"}), 403
    return jsonify(msg="Welcome, Maintainer!")

@app.route("/general", methods=["GET"])
@jwt_required()
def general():
    return jsonify(msg="Welcome, any logged-in user!")

if __name__ == "__main__":
    app.run(debug=True)
