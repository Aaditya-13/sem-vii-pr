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
