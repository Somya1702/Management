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
        let sortOrder = {};
        function sortTable(columnIndex) {
            let table = document.querySelector("table tbody");
            let rows = Array.from(table.querySelectorAll("tr"));
            
            sortOrder[columnIndex] = !sortOrder[columnIndex];
            rows.sort((a, b) => {
                let cellA = a.children[columnIndex].innerText.trim().toLowerCase();
                let cellB = b.children[columnIndex].innerText.trim().toLowerCase();
                return sortOrder[columnIndex] ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
            });
            
            table.innerHTML = "";
            rows.forEach(row => table.appendChild(row));
        }
    </script>
</head>
<body>
    <h1>Task Manager</h1>
    <button onclick="showTaskForm()">Add New Task</button>
    
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
                <th onclick="sortTable(0)">S.No. ⇅</th>
                <th onclick="sortTable(1)">Litigation ⇅</th>
                <th onclick="sortTable(2)">Name ⇅</th>
                <th onclick="sortTable(3)">Entity ⇅</th>
                <th onclick="sortTable(4)">Task ⇅</th>
                <th onclick="sortTable(5)">Status ⇅</th>
                <th onclick="sortTable(6)">Due Date ⇅</th>
                <th onclick="sortTable(7)">Pending From ⇅</th>
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
