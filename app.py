from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration (SQLite)
db_path = os.path.join(os.path.dirname(__file__), "tasks.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Homepage Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Task Management API is Running!"}), 200

# Get All Tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": task.id, 
        "title": task.title, 
        "description": task.description, 
        "completed": task.completed
    } for task in tasks])

# Add a New Task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    if "title" not in data or not data["title"].strip():
        return jsonify({"error": "Title is required"}), 400
    
    new_task = Task(title=data["title"], description=data.get("description", ""))
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"message": "Task added!", "task": {
        "id": new_task.id, 
        "title": new_task.title, 
        "description": new_task.description, 
        "completed": new_task.completed
    }})

# Update a Task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404

    data = request.json
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    
    return jsonify({"message": "Task updated!", "task": {
        "id": task.id, 
        "title": task.title, 
        "description": task.description, 
        "completed": task.completed
    }})

# Delete a Task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"message": "Task deleted!"})

# Run the Flask app on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
