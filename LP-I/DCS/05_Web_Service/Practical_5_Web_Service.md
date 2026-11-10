# Practical 5: Create and Consume a Web Service

## Aim

To create a simple HTTP web service that returns JSON and write a client
application that requests and displays the response.

## Theory

A web service lets one application request data or an operation from another
application over HTTP. The service in this practical listens for an HTTP GET
request and responds with a JSON message. The client sends a request to the
service URL, reads the HTTP response, and decodes the JSON data.

The server uses Python's built-in `http.server` module. Its request handler
implements `do_GET()` to process GET requests. The client uses the built-in
`urllib.request.urlopen()` function to contact the service. See the Python
documentation for [`http.server`](https://docs.python.org/3/library/http.server.html)
and [`urllib.request`](https://docs.python.org/3/library/urllib.request.html).

This version uses only Python's standard library. The current computer has
Python 3.13.7, and Flask and Requests are not installed, so no package
installation is needed for this version.

## Files and roles

| File | Role |
|---|---|
| `server.py` | Starts the HTTP service and returns a JSON message. |
| `client.py` | Requests the service and prints the returned message. |

## Program

### `server.py`

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class HelloService(BaseHTTPRequestHandler):
    def do_GET(self):
        data = json.dumps({"message": "Hello from the web service"}).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)


server = HTTPServer(("127.0.0.1", 8000), HelloService)
print("Web service running at http://127.0.0.1:8000")
server.serve_forever()
```
| Line(s) | Explanation |
|---|---|
| 1 | Imports the HTTP request handler base class and HTTP server class. |
| 2 | Imports `json` to encode the response as JSON. |
| 5 | Defines the service's request handler by extending `BaseHTTPRequestHandler`. |
| 6 | Defines the method that handles HTTP GET requests. |
| 7 | Creates a JSON message and encodes it as bytes for the HTTP response body. |
| 9 | Sends the HTTP success status `200 OK`. |
| 10 | Sets the response content type to JSON. |
| 11 | Finishes sending the response headers. |
| 12 | Writes the JSON bytes into the response body. |
| 15 | Creates the web server on local address `127.0.0.1`, port `8000`, using `HelloService` to handle requests. |
| 16 | Prints the URL where the service is listening. |
| 17 | Keeps the server running and waiting for client requests. |

### `client.py`

```python
from urllib.request import urlopen
import json


with urlopen("http://127.0.0.1:8000/") as response:
    data = json.loads(response.read().decode())

print("Service response:", data["message"])
```
| Line(s) | Explanation |
|---|---|
| 1 | Imports `urlopen`, which sends an HTTP request to a URL and returns the response. |
| 2 | Imports `json` to decode the service's response. |
| 5 | Sends a GET request to the service URL and opens the response. |
| 6 | Reads the response bytes, decodes them into text, then parses the JSON into a Python dictionary. |
| 8 | Prints the `message` value received from the service. |

## How to run

Open a terminal in this folder. Start the service in the first terminal:

```powershell
python server.py
```

Leave it running. Open a second terminal in the same folder and run the client:

```powershell
python client.py
```

The client should display:

```text
Service response: Hello from the web service
```

Stop the server with Ctrl+C after running the client.

## Execution flow to remember

1. The server creates an HTTP request handler and listens on port `8000`.
2. The client sends a GET request to the server URL.
3. The handler returns a JSON response with status `200 OK`.
4. The client reads and decodes the JSON, then prints its message.

## Viva questions and short answers

1. **What is a web service?**  
   A service that lets applications exchange data or request operations over a
   network using standard protocols such as HTTP.

2. **What is HTTP?**  
   Hypertext Transfer Protocol, used for requests and responses between clients
   and web servers.

3. **What is JSON?**  
   JavaScript Object Notation, a text format for representing structured data.

4. **What is the role of `server.py`?**  
   It listens for HTTP requests and returns the service's JSON response.

5. **What is the role of `client.py`?**  
   It requests the service URL and displays the returned message.

6. **What does `do_GET()` do?**  
   It handles an HTTP GET request received by the server.

7. **What does status code `200` mean?**  
   The HTTP request succeeded.

8. **Why is the response encoded before writing it?**  
   An HTTP response body is written as bytes, so the JSON text is encoded.

9. **Why are two terminals used?**  
   One keeps the server running while the other runs the client that consumes it.

10. **Does this example require Flask or Requests?**  
    No. It uses Python standard-library modules only.
