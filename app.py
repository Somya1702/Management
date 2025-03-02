from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/dbname'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.String(12), nullable=False)
    litigation = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    entity = db.Column(db.String(200), nullable=False)
    task = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.String(12), nullable=False)
    pending_from = db.Column(db.String(200), nullable=False)

def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%b-%Y")
    return ""

with app.app_context():
    db.create_all()

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
                document.querySelectorAll("thead input").forEach(input => input.value = "");
            });
        }
        
        function loadTasks() {
            fetch("/tasks").then(response => response.json()).then(data => {
                let tableBody = document.getElementById("taskTableBody");
                tableBody.innerHTML = "";
                data.forEach((task, index) => {
                    let serialNo = data.length - index;
                    let row = `<tr>
                        <td>${serialNo}</td>
                        <td>${task.entry_date}</td>
                        <td>${task.litigation}</td>
                        <td>${task.name}</td>
                        <td>${task.entity}</td>
                        <td>${task.task}</td>
                        <td>${task.status}</td>
                        <td>${task.due_date}</td>
                        <td>${calculateDays(task.due_date)}</td>
                        <td>${task.pending_from}</td>
                    </tr>`;
                    tableBody.innerHTML += row;
                });
            });
        }
        window.onload = loadTasks;
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
            function calculateDays(dueDate) {
            const today = new Date();
            const due = new Date(dueDate.split('-').reverse().join('-'));
            const diffTime = due - today;
            return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        }
    </script>
</head>
<body>
    <h1>Task Manager</h1>
    <table>
        <thead>
            <tr>
                <th>S.No.</th>
                <th>Entry Date</th>
                <th>Litigation</th>
                <th>Name</th>
                <th>Entity</th>
                <th>Task</th>
                <th>Status</th>
                <th>Due Date</th>
                <th>No. of Days</th>
                <th>Pending From</th>
                <th>Action</th>
            </tr>
            <tr>
                <td><button onclick='enableSearch()'>Search</button></td>
                <td></td>
                <td><input type="text" id="litigation"></td>
                <td><input type="text" id="name"></td>
                <td><input type="text" id="entity"></td>
                <td><input type="text" id="task"></td>
                <td><input type="text" id="status"></td>
                <td><input type="date" id="due_date"></td>
                <td></td>
                <td><input type="text" id="pending_from"></td>
                <td><button onclick="addTask()">Save</button></td>
            </tr>
        </thead>
        <tbody id="taskTableBody">
        </tbody>
    </table>
</body>
</html>""")

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    new_task = Task(
        entry_date=data["entryDate"],
        litigation=data["litigation"],
        name=data["name"],
        entity=data["entity"],
        task=data["task"],
        status=data["status"],
        due_date=format_date(data["dueDate"]),
        pending_from=data["pendingFrom"]
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return jsonify([{ "entry_date": t.entry_date, "litigation": t.litigation, "name": t.name, "entity": t.entity, "task": t.task, "status": t.status, "due_date": t.due_date, "pending_from": t.pending_from } for t in tasks])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
