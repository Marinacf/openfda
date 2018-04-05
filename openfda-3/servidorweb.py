import http.server
import socketserver
import http.client
import json

PORT = 8080
headers = {'User-Agent': 'http-client'}

conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json?limit=10", None, headers)

r1 = conexion.getresponse()
if r1.status == 404:
    print("ERROR, recurso no encontrado")
    exit(1)
print(r1.status, r1.reason)
info_raw = r1.read().decode("utf-8")
conexion.close()
medicamentos = []
info = json.loads(info_raw)
for elemento in range(len(info['results'])):
    if (info['results'][elemento]['openfda']):
        medicamentos.append(info['results'][elemento]['openfda']['generic_name'][0])

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = """<html>
        <body>
        <ol>
        """
        message +="<h2>Los 10 medicamentos son:</h2>"
        for medicina in medicamentos:
            message += "<li>"+medicina+"</li>"
        message += """</ol>
        </body>
        </html>
        """
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return

Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Servidor interrumpido por el usuario")
    exit(1)
print("")
print("Servidor parado")
httpd.close()
