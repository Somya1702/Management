from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

tasks = []  # In-memory storage for tasks

def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%b-%Y")
    return ""

@app.route("/", methods=["GET"])
def home():
    return render_template_string("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 5%; }
        table { width: 80%; margin: auto; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
        th { background: #f4f4f4; cursor: pointer; }
        #taskForm { display: none; flex-direction: column; align-items: center; margin-top: 20px; }
    </style>
    <script>
        function toggleTaskForm() {
            let form = document.getElementById("taskForm");
            form.style.display = (form.style.display === "none" || form.style.display === "") ? "flex" : "none";
        }
        
        function addTask() {
            const litigation = document.getElementById("litigation").value;
            const name = document.getElementById("name").value;
            const entity = document.getElementById("entity").value;
            const task = document.getElementById("task").value;
            const status = document.getElementById("status").value;
            const dueDate = document.getElementById("due_date").value;
            const pendingFrom = document.getElementById("pending_from").value;
            
            if (!litigation || !name || !entity || !task || !status || !dueDate || !pendingFrom) {
                alert("All fields are required! Please fill in all details.");
                return;
            }
            
            fetch("/add_task", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ litigation, name, entity, task, status, dueDate, pendingFrom })
            }).then(response => response.json()).then(() => {
                loadTasks();
                document.getElementById("litigation").value = "";
                document.getElementById("name").value = "";
                document.getElementById("entity").value = "";
                document.getElementById("task").value = "";
                document.getElementById("status").value = "";
                document.getElementById("due_date").value = "";
                document.getElementById("pending_from").value = "";
            });
        }
        
        function loadTasks() {
            fetch("/tasks").then(response => response.json()).then(data => {
                let tableBody = document.getElementById("taskTableBody");
                tableBody.innerHTML = "";
                data.forEach((task, index) => {
                    let row = `<tr>
                        <td>${index + 1}</td>
                        <td>${task.litigation}</td>
                        <td>${task.name}</td>
                        <td>${task.entity}</td>
                        <td>${task.task}</td>
                        <td>${task.status}</td>
                        <td>${task.dueDate}</td>
                        <td>${task.pendingFrom}</td>
                    </tr>`;
                    tableBody.innerHTML += row;
                });
            });
        }
        window.onload = loadTasks;
    </script>
</head>
<body>
    <h1>Task Manager</h1>
    <button onclick="toggleTaskForm()">Add New Task</button>
    
    <div id="taskForm">
        <input type="text" id="litigation" placeholder="Litigation">
        <input type="text" id="name" placeholder="Name">
        <input type="text" id="entity" placeholder="Entity">
        <input type="text" id="task" placeholder="Task">
        <input type="text" id="status" placeholder="Status">
        <input type="date" id="due_date" placeholder="Due Date">
        <input type="text" id="pending_from" placeholder="Pending From">
        <button onclick="addTask()">Save Task</button>
    </div>
    
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
            </tr>
        </thead>
        <tbody id="taskTableBody">
            <!-- Data rows will be inserted here dynamically -->
        </tbody>
    </table>
</body>
</html>""")

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    data["dueDate"] = format_date(data["dueDate"])
    tasks.append(data)
    return jsonify({"message": "Task added successfully!"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
