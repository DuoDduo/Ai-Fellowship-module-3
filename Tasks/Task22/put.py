from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Add the data
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

    def do_PUT(self):
        content_size = int(self.headers.get("Content-length", 0))
        parsed_data = self.rfile.read(content_size)

        put_data = json.loads(parsed_data)

        if data:
            data[0] =put_data
            self.send_data({
            "Message": "Data replaced",
            "data": data[0]
            })
        else:
            data.append(put_data)
            self.send_data({
            "Message": "Data added successfully",
            "data": put_data
            })

def run():
    HTTPServer(("localhost", 5000), BasicAPI).serve_forever()

print("Application is running smoothly")
run()