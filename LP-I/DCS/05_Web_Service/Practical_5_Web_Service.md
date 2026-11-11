# Practical 5: Create and Consume a Web Service

## Aim

To create a simple Flask web service that displays an HTML page and provides
student information as JSON, then consume the JSON service from a Python client.

## Theory

A web service lets one application request information or an operation from
another application over HTTP. This practical uses Flask to define two routes:
`/` returns a simple HTML page, and `/students` returns a list of students as
JSON. The client sends a GET request to `/students`, receives the JSON response,
and prints the student details.

Flask maps URL routes to Python functions. `jsonify` converts Python data into a
JSON HTTP response. The client uses the Requests library to send its HTTP GET
request and decode the JSON response. Flask and Requests are third-party
packages; the [Flask installation guide](https://flask.palletsprojects.com/en/stable/installation/)
and [Requests installation guide](https://requests.readthedocs.io/en/latest/user/install/)
document their installation.

The ZIP uses the same Flask and Requests approach for its student service. This
version keeps the same student-data idea and trims it to one JSON API route,
while retaining a small HTML home page. It leaves out the optional single
student route, POST route, input validation, and background-thread startup.

## Files and roles

| File | Role |
|---|---|
| `server.py` | Runs the Flask service, serves an HTML home page, and returns student records as JSON. |
| `client.py` | Requests `/students` and displays the returned records. |

## Program

### `server.py`

```python
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
```
| Line(s) | Explanation |
|---|---|
| 1 | Imports the Flask application class and `jsonify` helper. |
| 3 | Creates the Flask application object. `__name__` lets Flask identify this Python module. |
| 5-9 | Stores three sample student records in a Python list. |
| 12 | Registers the following function for the home URL `/`. |
| 13 | Defines the function that handles requests to `/`. |
| 14-21 | Returns a small HTML page with a heading and a link to the student JSON route. |
| 24 | Registers the student route and allows HTTP GET requests. |
| 25 | Defines the function that handles requests to `/students`. |
| 26 | Converts the student list to JSON and returns it as the HTTP response. |
| 29 | Checks that this file is being run directly, rather than imported by another Python file. |
| 30 | Starts Flask on the local computer at port `5000`. |

### `client.py`

```python
import requests

url = "http://127.0.0.1:5000/students"
response = requests.get(url)
response.raise_for_status()

for student in response.json():
    print(student["id"], student["name"], student["course"])
```
| Line(s) | Explanation |
|---|---|
| 1 | Imports Requests, the HTTP client library. |
| 3 | Stores the URL for the server's student-list API. |
| 4 | Sends an HTTP GET request to that URL. |
| 5 | Raises an error if the server returned an unsuccessful HTTP status. |
| 7 | Reads and decodes the JSON response as a Python list, then loops through its records. |
| 8 | Prints each student's ID, name, and course. |

## How to run

The current Python setup does not have Flask or Requests installed. Install
both packages once from a terminal in this folder:

```powershell
python -m pip install Flask requests
```

Start the service in the first terminal:

```powershell
python server.py
```

Open `http://127.0.0.1:5000/` in a browser to display the HTML page. The
student JSON is at `http://127.0.0.1:5000/students`.

Leave the server running. In a second terminal in the same folder, run the
client:

```powershell
python client.py
```

The client prints the three student records. Stop the server with Ctrl+C when
finished.

## Execution flow to remember

1. Create the Flask application and student data.
2. Map `/` to an HTML page and `/students` to a JSON response.
3. Start the Flask server.
4. Send a GET request from the client to `/students`.
5. Decode and display the returned student records.

## Viva questions and short answers

1. **What is a web service?**  
   A service that lets applications exchange data or request operations over a
   network using a protocol such as HTTP.

2. **What is Flask?**  
   A Python web framework used here to define routes and run the HTTP service.

3. **What is a route?**  
   A URL path mapped to a function that handles requests to that path.

4. **What does `jsonify` do?**  
   It converts Python data into a JSON HTTP response.

5. **What does HTTP GET do in this practical?**  
   It asks the `/students` service route to return the student records.

6. **What is the role of `client.py`?**  
   It requests the JSON endpoint and displays the records returned by the server.

7. **What does `response.json()` do?**  
   It decodes the response body from JSON into Python data.

8. **What are `/` and `/students`?**  
   They are routes: `/` serves HTML, while `/students` serves JSON data.

9. **Why do we run the server and client separately?**  
   The server must stay active while the client sends its request and receives
   the response.

10. **What packages are needed to run these files?**  
    Flask for the server and Requests for the client.
