from http.server import HTTPServer
from api.index import handler

PORT = 8000

server = HTTPServer(("localhost", PORT), handler)

print(f"India Data Agent: http://localhost:{PORT}")
print("Press Ctrl+C to stop.")

server.serve_forever()