from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MaliciousOnionHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Extract the server's address
        host, port = self.server.server_address
        # Extract the client's IP address from client_address tuple
        client_ip = self.client_address[0]
        # Construct a JSON response with name and address
        response_content = {
            "name": "Malicious Onion",
            "address": f"{host}:{port}",
            "client_ip": client_ip
        }

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_content).encode('utf-8'))

def run_server(port=8001):
    server = HTTPServer(('', port), MaliciousOnionHandler)
    print(f"Malicious Onion running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server(8001)
