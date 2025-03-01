from flask import Flask, request, jsonify, render_template_string
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

# Serve Frontend (HTML Page)
@app.route("/", methods=["GET"])
def home():
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: auto; text-align: center; }
        input, button { padding: 10px; margin: 5px; font-size: 16px; }
        .task { padding: 10px; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }
        .completed { text-decoration: line-through; color: gray; }
        .buttons { display: flex; gap: 10px; }
    </style>
</head>
<body>
    <h1>Task Manager</h1>
    <input type="text" id="taskTitle" placeholder="Task title">
    <input type="text" id="taskDesc" placeholder="Task description">
    <button onclick="addTask()">Add Task</button>
    <h2>Tasks</h2>
    <div id="taskList"></div>
    <script>
        const API_URL = "/tasks"; // API calls will go directly to Flask server

        async function fetchTasks() {
            try {
                const response = await fetch(API_URL);
                const tasks = await response.json();
                document.getElementById("taskList").innerHTML = tasks.map(task => `
                    <div class="task ${task.completed ? 'completed' : ''}">
                        <span>${task.title}: ${task.description}</span>
                        <div class="buttons">
                            <button onclick="toggleTask(${task.id}, ${task.completed})">
                                ${task.completed ? 'Undo' : 'Complete'}
                            </button>
                            <button onclick="deleteTask(${task.id})">Delete</button>
                        </div>
                    </div>
                `).join("");
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        }

        async function addTask() {
            const title = document.getElementById("taskTitle").value;
            const description = document.getElementById("taskDesc").value;

            if (!title.trim()) {
                alert("Task title is required!");
                return;
            }

            try {
                await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title, description })
                });
                fetchTasks();
            } catch (error) {
                console.error("Error adding task:", error);
            }
        }

        async function toggleTask(id, completed) {
            try {
                await fetch(`${API_URL}/${id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ completed: !completed })
                });
                fetchTasks();
            } catch (error) {
                console.error("Error updating task:", error);
            }
        }

        async function deleteTask(id) {
            try {
                await fetch(`${API_URL}/${id}`, { method: "DELETE" });
                fetchTasks();
            } catch (error) {
                console.error("Error deleting task:", error);
            }
        }

        fetchTasks();
    </script>
</body>
</html>''')

# Get All Tasks (API)
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": task.id, 
        "title": task.title, 
        "description": task.description, 
        "completed": task.completed
    } for task in tasks])

# Add a New Task (API)
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

# Update a Task (API)
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

# Delete a Task (API)
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found!"}), 404

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"message": "Task deleted!"})

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
