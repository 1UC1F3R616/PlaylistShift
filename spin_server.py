import http.server
import socketserver
import urllib.parse

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get('code', None)
        if code is not None:
            print(code)
            print(type(code))
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization code received: %s</h1></body></html>' % code[0].encode())
        else:
            self.send_response(400)
            self.end_headers()

PORT = 8000

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.handle_request()