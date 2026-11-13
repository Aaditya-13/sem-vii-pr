from flask import Flask, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "Amit", "course": "Computer Science"},
    {"id": 2, "name": "Priya", "course": "Information Technology"},
    {"id": 3, "name": "Rahul", "course": "Electronics"}
]


@app.route("/")
def home():
    return """
    <html>
      <body>
        <h1>Student Information Service</h1>
        <p>Open <a href="/students">/students</a> to view the JSON API.</p>
      </body>
    </html>
    """


@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
