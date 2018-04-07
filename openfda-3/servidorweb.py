import http.server # Importamos aquellos módulos que utilizaremos posteriormente.
import socketserver
import http.client
import json

PORT = 8000 # Puerto donde lanzar el servidor
# Creamos en primer lugar un código que funcione como cliente.
headers = {'User-Agent': 'http-client'}
try:
    conexion = http.client.HTTPSConnection("api.fda.gov")
    conexion.request("GET", "/drug/label.json?limit=10", None, headers)
except Exception:
    print("Error al solicitar el nombre del servidor.")
    exit(1)

r1 = conexion.getresponse()
if r1.status == 404:
    print("ERROR, recurso no encontrado")
    exit(1)
print(r1.status, r1.reason)
info_raw = r1.read().decode("utf-8")
conexion.close()
medicamentos = [] # Creamos una lista donde introduciré los diez medicamentos, para la petición del cliente.
info = json.loads(info_raw)
for elemento in range(len(info['results'])):
    if (info['results'][elemento]['openfda']):
        medicamentos.append(info['results'][elemento]['openfda']['generic_name'][0])
    else:
        medicamentos.append('El medicamento no tiene informacion asignada')
# Para introducir los medicamentos en la lista, itero sobre la la longitud de los 10 resultados que obtenemos por el limit, y
# en el caso de que exista el apartado 'openfda', y por tanto, su información, incluiremos a la lista medicamentos,
# los nombres genéricos de cada producto. En el caso de que no existiera dicha información, mediante un else
# incluiriamos a la lista medicamentos una frase indicando que no existe la información buscada.
#Realizamos una clase con nuestro manejador, aplicando herencia de BaseHTTPRequestHandler.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self): # Realizamos un metodo que se invoca automaticamente cada vez que haya una peticion GET por HTTP.
        # El recurso que nos solicitan se encuentra en self.path.
        self.send_response(200) # mensaje de respuesta: primera linea = status (OK)
        self.send_header('Content-type', 'text/html') # cabeceras para que el cliente sepa que el contenido se trata de un HTML.
        self.end_headers()
        # A continuación, el mensaje que le mandamos al cliente: un texto junto con el recurso solicitado.
        message = """<html>
        <body style="background-color:#F6CEF5;">
        <ul>
        """
        message +="<h2><font color='#CC2EFA'>Los 10 medicamentos son:</font></h2>"
        for medicina in medicamentos: # Iteramos sobre la lista de medicamentos, obteniendo cada uno en concreto.
            message += "<li type='square'>"+medicina+"</li>"
        message += """</ul>
        </body>
        </html>
        """
        self.wfile.write(bytes(message, "utf8")) # Enviamos el mensaje completo.
        print("File served!")
        return

# El servidor comienza aquí:
Handler = testHTTPRequestHandler #Establecemos como manejador nuestra propia clase, llamada Handler (objeto).
httpd = socketserver.TCPServer(("", PORT), Handler) # Configuramos el socket del servidor, esperando conexiones
# de clientes.
print("serving at port", PORT)

# Entramos en el bucle principal, atendiendo las peticiones desde nuestro manejador (cada vez que ocurra un 'GET'
# se invocará nuestro método do_GET)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Servidor interrumpido por el usuario")
    exit(1) # Salimos del código si el usuario interrumpe el server.
print("")
print("Servidor parado")
httpd.close()
