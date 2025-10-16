from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data =[
    {
        "name": "Sam Larry",
        "track": "AI Developer"
    }
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data,status= 201):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_PATCH(self):
        content_size = int(self.headers.get("Content-Length",0))
        parsed_data = self.rfile.read(content_size)

        patched_data = json.loads(parsed_data)
        if data:
            data[0].update(patched_data)
            self.send_data({
                "Message": "Data Edited",
                "data": data[0]

            },status=201)
        else:
            self.send_data({
                "Message":"No data to patch"
            }, status=400)


def run():
    HTTPServer(('0.0.0.0',8000),BasicAPI).serve_forever()

print("Application Running")
run()