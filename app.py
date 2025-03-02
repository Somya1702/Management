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
        table { border-collapse: collapse; width: 80%; margin: auto; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #f4f4f4; cursor: pointer; }
        input { width: 95%; padding: 4px; box-sizing: border-box; text-align: center; }
        button { padding: 4px 8px; cursor: pointer; }
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 5%; }
        table { width: 80%; margin: auto; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
        th { background: #f4f4f4; cursor: pointer; }
        input { width: 100%; padding: 5px; }
    </style>
    <script>
        function addTask() {
            const entryDate = new Date().toLocaleDateString('en-GB', {
                day: '2-digit', month: 'short', year: 'numeric'
            }).replace(/ /g, '-');
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
                body: JSON.stringify({ entryDate, litigation, name, entity, task, status, dueDate, pendingFrom })
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
            document.querySelectorAll('#taskTableBody td').forEach(cell => {
                cell.ondblclick = function() {
                    let input = document.createElement('input');
                    input.type = 'text';
                    input.value = this.innerText;
                    input.onblur = function() {
                        cell.innerText = input.value;
                    };
                    this.innerText = '';
                    this.appendChild(input);
                    input.focus();
                };
                    this.innerText = '';
                    this.appendChild(input);
                    input.focus();
                };
            });
            fetch("/tasks").then(response => response.json()).then(data => {
                let tableBody = document.getElementById("taskTableBody");
                tableBody.innerHTML = "";
                data.forEach((task, index) => {
                    if (!task.entryDate) task.entryDate = new Date().toLocaleDateString('en-GB', {
                        day: '2-digit', month: 'short', year: 'numeric'
                    }).replace(/ /g, '-');
                    let row = `<tr>
                        <td>${index + 1}</td>
                        <td>${task.entryDate}</td>
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
            function filterTasks() {
            let filters = {
                litigation: document.getElementById("litigation").value.toLowerCase(),
                name: document.getElementById("name").value.toLowerCase(),
                entity: document.getElementById("entity").value.toLowerCase(),
                task: document.getElementById("task").value.toLowerCase(),
                status: document.getElementById("status").value.toLowerCase(),
                dueDate: document.getElementById("due_date").value,
                pendingFrom: document.getElementById("pending_from").value.toLowerCase()
            };
            
            document.querySelectorAll("#taskTableBody tr").forEach(row => {
                let cells = row.children;
                let show = true;
                if (filters.litigation && !cells[2].innerText.toLowerCase().includes(filters.litigation)) show = false;
                if (filters.name && !cells[3].innerText.toLowerCase().includes(filters.name)) show = false;
                if (filters.entity && !cells[4].innerText.toLowerCase().includes(filters.entity)) show = false;
                if (filters.task && !cells[5].innerText.toLowerCase().includes(filters.task)) show = false;
                if (filters.status && !cells[6].innerText.toLowerCase().includes(filters.status)) show = false;
                if (filters.dueDate && cells[7].innerText !== filters.dueDate) show = false;
                if (filters.pendingFrom && !cells[8].innerText.toLowerCase().includes(filters.pendingFrom)) show = false;
                row.style.display = show ? "" : "none";
            });
        }
            function enableSearch() {
            document.querySelectorAll("thead input").forEach(input => {
                input.addEventListener("input", filterTasks);
            });
        }
        
        function filterTasks() {
            let filters = {
                litigation: document.getElementById("litigation").value.toLowerCase(),
                name: document.getElementById("name").value.toLowerCase(),
                entity: document.getElementById("entity").value.toLowerCase(),
                task: document.getElementById("task").value.toLowerCase(),
                status: document.getElementById("status").value.toLowerCase(),
                dueDate: document.getElementById("due_date").value,
                pendingFrom: document.getElementById("pending_from").value.toLowerCase()
            };
            
            document.querySelectorAll("#taskTableBody tr").forEach(row => {
                let cells = row.children;
                let show = true;
                if (filters.litigation && !cells[2].innerText.toLowerCase().includes(filters.litigation)) show = false;
                if (filters.name && !cells[3].innerText.toLowerCase().includes(filters.name)) show = false;
                if (filters.entity && !cells[4].innerText.toLowerCase().includes(filters.entity)) show = false;
                if (filters.task && !cells[5].innerText.toLowerCase().includes(filters.task)) show = false;
                if (filters.status && !cells[6].innerText.toLowerCase().includes(filters.status)) show = false;
                if (filters.dueDate && cells[7].innerText !== filters.dueDate) show = false;
                if (filters.pendingFrom && !cells[8].innerText.toLowerCase().includes(filters.pendingFrom)) show = false;
                row.style.display = show ? "" : "none";
            });
        }
    </script>
</head>
<body>
    <h1>Task Manager</h1>
    <table>
        <thead>
            <tr>
                <th>S.No.</th>
                <th>Entry Date <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Litigation <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Name <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Entity <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Task <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Status <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Due Date <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Pending From <button onclick='sortByColumn(this)'>⇅</button></th>
                <th>Action</th>
            </tr>
            <tr>
                <td><button onclick='enableSearch()'>Search</button></td>
                <td><input type='date' id='entry_date'></td>
                <td><input type="text" id="litigation"></td>
                <td><input type="text" id="name"></td>
                <td><input type="text" id="entity"></td>
                <td><input type="text" id="task"></td>
                <td><input type="text" id="status"></td>
                <td><input type="date" id="due_date"></td>
                <td><input type="text" id="pending_from"></td>
                <td><button onclick="addTask()">Save</button></td>
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
