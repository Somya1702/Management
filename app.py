from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration (SQLite)
db_path = os.path.join(os.path.dirname(__file__), "tasks.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Task Model with Updated Columns
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incremented S.No.
    litigation = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    entity = db.Column(db.String(200), nullable=False)
    task = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(100), nullable=False, default="Pending")
    due_date = db.Column(db.String(100), nullable=True)  # Stores as `dd-MMM-yyyy`
    pending_from = db.Column(db.String(200), nullable=True)
    document_link = db.Column(db.String(500), nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()

# Function to Format Date to `dd-MMM-yyyy`
def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%b-%Y")
    return None

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
        body { font-family: Arial, sans-serif; max-width: 90%; margin: auto; text-align: center; }
        input, button { padding: 8px; margin: 5px; font-size: 14px; width: 180px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #f4f4f4; }
        .buttons { display: flex; gap: 10px; justify-content: center; }
        #taskForm { display: none; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Task Manager</h1>

    <button onclick="showTaskForm()">Add New Task</button>

    <div id="taskForm">
        <input type="text" id="litigation" placeholder="Litigation">
        <input type="text" id="name" placeholder="Name">
        <input type="text" id="entity" placeholder="Entity">
        <input type="text" id="task" placeholder="Task">
        <input type="text" id="status" placeholder="Status (Pending/In Progress/Completed)">
        <input type="date" id="due_date" placeholder="Due Date">
        <input type="text" id="pending_from" placeholder="Pending From">
        <input type="text" id="document_link" placeholder="Document Link">
        <button onclick="addTask()">Save Task</button>
    </div>

    <h2>Task List</h2>
    <table>
        <thead>
            <tr>
                <th>S.No.</th>
                <th>Litigation</th>
                <th>Name</th>
                <th>Entity</th>
                <th>Task</th>
                <th>Status</th>
                <th>Due Date</th>
                <th>Pending From</th>
                <th>Document Link</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="taskList"></tbody>
    </table>

    <script>
        const API_URL = "/tasks";

        function showTaskForm() {
            document.getElementById("taskForm").style.display = "block";
        }

        async function fetchTasks() {
            try {
                const response = await fetch(API_URL);
                const tasks = await response.json();
                document.getElementById("taskList").innerHTML = tasks.map((task, index) => `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${task.litigation}</td>
                        <td>${task.name}</td>
                        <td>${task.entity}</td>
                        <td>${task.task}</td>
                        <td>${task.status}</td>
                        <td>${task.due_date || 'N/A'}</td>
                        <td>${task.pending_from || 'N/A'}</td>
                        <td><a href="${task.document_link}" target="_blank">${task.document_link ? 'View' : 'N/A'}</a></td>
                        <td class="buttons">
                            <button onclick="confirmDelete(${task.id})">Delete</button>
                        </td>
                    </tr>
                `).join("");
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        }

        async function addTask() {
            const litigation = document.getElementById("litigation").value;
            const name = document.getElementById("name").value;
            const entity = document.getElementById("entity").value;
            const task = document.getElementById("task").value;
            const status = document.getElementById("status").value || "Pending";
            const due_date = document.getElementById("due_date").value;
            const pending_from = document.getElementById("pending_from").value;
            const document_link = document.getElementById("document_link").value;

            if (!litigation || !name || !entity || !task) {
                alert("Please fill in all required fields!");
                return;
            }

            try {
                await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ litigation, name, entity, task, status, due_date, pending_from, document_link })
                });
                fetchTasks();
                clearFields();
                document.getElementById("taskForm").style.display = "none";
            } catch (error) {
                console.error("Error adding task:", error);
            }
        }

        function clearFields() {
            document.getElementById("litigation").value = "";
            document.getElementById("name").value = "";
            document.getElementById("entity").value = "";
            document.getElementById("task").value = "";
            document.getElementById("status").value = "";
            document.getElementById("due_date").value = "";
            document.getElementById("pending_from").value = "";
            document.getElementById("document_link").value = "";
        }

        function confirmDelete(id) {
            const confirmation = confirm("Are you sure you want to delete this task?");
            if (confirmation) {
                deleteTask(id);
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

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
