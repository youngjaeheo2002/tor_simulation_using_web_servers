from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class TorontoNewsOnionHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Extract the server's address
        host, port = self.server.server_address
        # Construct a JSON response with name and address
        response_content = {
            "name": "Toronto News Onion",
            "address": f"toronto_news_onion:{port}"
        }

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_content).encode('utf-8'))

def run_server(port=8020):
    server = HTTPServer(('', port), TorontoNewsOnionHandler)
    print(f"Toronto News Onion running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
