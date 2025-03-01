from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
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
        th { background: #f4f4f4; }
    </style>
</head>
<body>
    <h1>Task Manager</h1>
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
        <tbody>
            <!-- Data rows will be inserted here -->
        </tbody>
    </table>
</body>
</html>""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
