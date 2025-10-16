from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data= [{"name":"Sam Larry"},
       {"track":"AI Developer"}]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status = 200):
        self.send_response(status)
        self.send_header("Content_Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    def do_POST(self):
        content_size = int(self.headers.get("Content_Length",0 )) 
        parsed_data = self.rfile.read(content_size)
        
        self.rfile.read()
        
        
        
 
def run():       
    HTTPServer(("localhost",8000),BasicAPI).serve_forever()          
    
print("Application is running")
run()    