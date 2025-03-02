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
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
        }
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ entryDate, litigation, name, entity, task, status, dueDate, pendingFrom })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ entryDate, litigation, name, entity, task, status, dueDate, pendingFrom })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ entryDate, litigation, name, entity, task, status, dueDate, pendingFrom })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
            }).then(response => response.json()).then((data) => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            }).catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
            }).then(response => response.json()).then((data) => {
                if (data.message === "Task added successfully!") {
                    loadTasks();
                    document.querySelectorAll("thead input").forEach(input => input.value = "");
                } else {
                    alert("Failed to save task. Please try again.");
                }
            }).catch(error => {
                console.error("Error saving task:", error);
                alert("Error saving task. Please check console logs.");
            });
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
                    let editButton = `<button onclick='editStatus(this)'>Edit</button>`;
                    let statusCell = `<td id='status-${task.id}'>${task.status}</td>`;
                    let serialNo = data.length - index;
                    let row = `<tr>
                        <td>${serialNo}</td>
                        <td>${task.entry_date}</td>
                        <td>${task.litigation}</td>
                        <td>${task.name}</td>
                        <td>${task.entity}</td>
                        <td>${task.task}</td>
                        ${statusCell}
                        <td>${task.due_date}</td>
                        <td>${calculateDays(task.due_date)}</td>
                        <td>${task.pending_from}</td>
                        <td>${index > 0 ? editButton : ''}</td>
                    </tr>`;
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
            function editStatus(button) {
            let row = button.parentNode.parentNode;
            let statusCell = row.cells[6];
            let currentText = statusCell.innerText;
            
            let input = document.createElement("input");
            input.type = "text";
            input.value = currentText;
            input.onblur = function() {
                statusCell.innerText = input.value;
            };
            
            statusCell.innerText = "";
            statusCell.appendChild(input);
            input.focus();
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
