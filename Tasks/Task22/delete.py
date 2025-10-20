from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Viewing the data
data = [
    {
    "Name": "Ade Mike",
    "Track": "Java",
    "Age": 35
    },

    {
    "Name": "John Welson",
    "Track": "C#",
    "Age": 20
    }
    ]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    
    def do_DELETE(self):
        if data:
            data.clear()
            self.send_data({
            "Message": "Data deleted successfully!",
            "data": []
            })
        else:
            self.send_data({
            "Message": "There is no data to delete!"
            })

def run():
    HTTPServer(("localhost", 5000), BasicAPI).serve_forever()

print("Application running successfully")
run()