import http.server #importamos los modulos para usar sus funciones mas adelante.
import http.client
import json
import socketserver

PORT=8000 #Puerto donde lanzar el servidor.

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #Realizamos una clase definiendo nuestro manejador, aplicando herencia de BaseHTTPRequestHandler.

    OPENFDA_URL = "api.fda.gov"
    OPENFDA_EVENTO = "/drug/label.json"
    OPENFDA_DROGA = '&search=active_ingredient:'
    OPENFDA_COMPANIA = '&search=openfda.manufacturer_name:'


    def dame_pag_principal(self): #Construye una pagina html que vera el cliente en forma de formularios
        html = """
            <html>
                <head>
                    <title>Aplicacion OpenFDA</title>
                </head>
                <body style='background-color: #F6CEF5;'>
                    <h1>Bienvenido a la aplicacion de OpenFDA. </h1>
                    <h4>*Para obtener un medicamento por defecto, haga click en 'List Drugs'</h4>
                    <form method="get" action="listDrugs">
                        Si quiere obtener mas de uno, porfavor inserte la cantidad: <input name="limit" type="text">
                        <input type = "submit" value="List Drugs">
                        </input>
                    </form>
                   <h4>*Para buscar un medicamento concreto, introduzcalo a continuacion...</h4>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Search Drug">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <h4>*Para obtener una company por defecto, haga click en 'List Companies'</h4>
                    <form method="get" action="listCompanies">
                        Si quiere obtener mas de uno, porfavor inserte la cantidad: <input name="limit" type="text">
                        <input type = "submit" value="List Companies">
                        </input>
                    </form>
                    <h4>*Para obtener una company concreta, introduzcalo a continuacion...</h4>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Search Companies">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <h4>*List of Warnings*</h4>
                    <form method="get" action="listWarnings">
                        Si quiere obtener mas de un 'warning', porfavor inserte la cantidad concreta: <input name="limit" type="text">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                    *Si se introduce un valor erroneo, o fuera de los valores de 'limit', se tomara el valor por defecto*
                </body>
            </html>
                """
        return html

    def dame_resultados_obtenidos (self, limit=10): #Obtenemos toda la informacion.
        headers = {'User-Agent': 'http-client'}
        conexion = http.client.HTTPSConnection(self.OPENFDA_URL)
        conexion.request("GET", self.OPENFDA_EVENTO + "?limit="+str(limit))
        print (self.OPENFDA_EVENTO + "?limit="+str(limit))
        r1 = conexion.getresponse()
        info_raw = r1.read().decode("utf8")
        info = json.loads(info_raw)
        resultados_obtenidos = info['results']
        return resultados_obtenidos

    def dame_pag_web (self, lista): #metodo que a partir de una lista concreta, realiza la pagina web html (aparecen al
                                    #hacer click en los botones del formulario).
        lista_html = """
                                <html>
                                    <head>
                                        <title>Aplicacion de OpenFDA</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            lista_html += "<li>" + item + "</li>"

        lista_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return lista_html

    def do_GET(self):
        lista_recursos = self.path.split("?") #separamos el recurso por la interrogacion, para estudiar los parametros.
        if len(lista_recursos) > 1: #tendra parametros si cumple el if
            parametros = lista_recursos[1]
        else:
            parametros = ""

        if parametros:
            limit_parametros = parametros.split("=") #De esta forma, nos quedamos con el valor del limit.
            try:
                if limit_parametros[0] == "limit": #limit se encuentra en la posicion 0, y su valor en la 1.
                    limit=int(limit_parametros[1]) #aseguramos que en la 0 esta limit y no otro parametro.
                    if limit>100:                   #si el limite es mayor que 100, le daremos el valor por defecto
                        limit=1
            except Exception: #En caso de introducir un valor de limit erroneo, le daremos el valor por defecto 1.
                limit=1

        if self.path=='/': #No tiene recurso determinado.

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()  # crea el formulario ya que llama al metodo 'dame_pag_principal'.
            html=self.dame_pag_principal()
            self.wfile.write(bytes(html, "utf8"))

        elif 'listDrugs' in self.path: #Pedimos realizar una lista de medicamentos en pag web.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_drogas = []
            resultados_obtenidos = self.dame_resultados_obtenidos(limit) #llamamos a la funcion para obtener los datos.
            for resultado in resultados_obtenidos:
                if ('generic_name' in resultado['openfda']):
                    lista_drogas.append (resultado['openfda']['generic_name'][0])
                else:
                    lista_drogas.append('Nombre del medicamento desconocido.')
            final_html = self.dame_pag_web (lista_drogas) #llamamos al metodo dame_pag_web para realizar la pagina web.

            self.wfile.write(bytes(final_html, "utf8"))
        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_companies = []
            resultados_obtenidos = self.dame_resultados_obtenidos (limit)
            for resultado in resultados_obtenidos:
                if ('manufacturer_name' in resultado['openfda']):
                    lista_companies.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    lista_companies.append('El nombre de la "COMPANY" es desconocido')
            final_html = self.dame_pag_web(lista_companies)

            self.wfile.write(bytes(final_html, "utf8"))
        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_warnings = []
            resultados_obtenidos = self.dame_resultados_obtenidos (limit)
            for resultado in resultados_obtenidos:
                if ('warnings' in resultado):
                    lista_warnings.append (resultado['warnings'][0])
                else:
                    lista_warnings.append('El "WARNING" es desconocido.')
            final_html = self.dame_pag_web(lista_warnings)

            self.wfile.write(bytes(final_html, "utf8"))
            #se realizara para company y warnings el mismo proceso realizado para drugs.
        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limit = 10
            drug=self.path.split('=')[1]

            list_drugs = []
            conexion = http.client.HTTPSConnection(self.OPENFDA_URL)
            conexion.request("GET", self.OPENFDA_EVENTO + "?limit="+str(limit) + self.OPENFDA_DROGA + drug)
            r1 = conexion.getresponse()
            info1 = r1.read()
            info_raw = info1.decode("utf8")
            info = json.loads(info_raw)

            try:
                buscador_drugs = info['results']
                for resultado in buscador_drugs:
                    if ('generic_name' in resultado['openfda']):
                        list_drugs.append(resultado['openfda']['generic_name'][0])

                    else:
                        list_drugs.append('"DRUG" desconocida.')

                final_html = self.dame_pag_web(list_drugs)
                self.wfile.write(bytes(final_html, "utf8"))
            except KeyError:
                print('Introduzca un nombre de medicamento correcto.')

        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limit = 10
            company=self.path.split('=')[1]
            list_companies = []
            conexion = http.client.HTTPSConnection(self.OPENFDA_URL)
            conexion.request("GET", self.OPENFDA_EVENTO + "?limit=" + str(limit) + self.OPENFDA_COMPANIA + company)
            r1 = conexion.getresponse()
            info1 = r1.read()
            info_raw = info1.decode("utf8")
            info = json.loads(info_raw)
            buscador_company = info['results']

            for resultado in buscador_company:
                if ('manufacturer_name' in resultado['openfda']):
                    list_companies.append(resultado['openfda']['manufacturer_name'][0])

                else:
                    list_companies.append('"COMPANY" desconocida.')

            final_html = self.dame_pag_web(list_companies)
            self.wfile.write(bytes(final_html, "utf8"))
        elif 'redirect' in self.path: #Redireccion a la pagina principal.
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path: #En caso de que sea una URL de acceso restringido, recibiremos un error 401.
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else: # Si el recurso solicitado no se encuentra en el servidor, recibiremos un mensaje de error 404.
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(". Recurso no encontrado: '{}'.".format(self.path).encode())
        return



socketserver.TCPServer.allow_reuse_address= True
# El servidor comienza aquí:

Handler = testHTTPRequestHandler #Establecemos como manejador nuestra propia clase, llamada Handler (objeto).

httpd = socketserver.TCPServer(("", PORT), Handler)# Configuramos el socket del servidor, esperando conexiones
# de clientes.
print("serving at port", PORT)
# Entramos en el bucle principal, atendiendo las peticiones desde nuestro manejador (cada vez que ocurra un 'GET'
# se invocará nuestro método do_GET)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Servidor interrumpido por el usuario.")
    print("Servidor parado.")
    exit(1)# Salimos del código si el usuario interrumpe el server.