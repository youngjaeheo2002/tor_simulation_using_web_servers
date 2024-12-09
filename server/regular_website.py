from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class RegularWebsiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract the server's address
        host, port = self.server.server_address
        # Construct a JSON response with name and address
        response_content = {
            "name": "Regular Website",
            "address": f"{host}:{port}"
        }

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_content).encode('utf-8'))

def run_server(port=8000):
    server = HTTPServer(('', port), RegularWebsiteHandler)
    print(f"Regular Website running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server(8000)
