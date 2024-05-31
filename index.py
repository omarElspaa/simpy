import http.server
import socketserver
import os

# Define the handler to be used by the server
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # Send an OK response
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")  # Response content

# Define the server port
PORT = int(os.environ.get("PORT"))

# Create the server object
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
