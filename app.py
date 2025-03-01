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
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 20%; }
    </style>
</head>
<body>
    <h1>Task Manager</h1>
</body>
</html>""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
