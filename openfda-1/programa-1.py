import http.client  # importamos aquellos módulos que vayamos a utilizar posteriormente.
import json

headers = {'User-Agent': 'http-client'}
try:
    conexion = http.client.HTTPSConnection("api.fda.gov")  # nos conectamos con la página pedida por el ej.
    conexion.request("GET", "/drug/label.json", None, headers)  # Le mandamos un mensaje de solicitud (verbo:GET).
except Exception: # utilizamos un try-except, para conectarnos siempre que no haya un error producido por el nombre del servidor.
    print("Error al solicitar el nombre del servidor")
    exit(1)  # Si hay un error nos salimos del programa.
r1 = conexion.getresponse()  # Leer el mensaje que se recibe, una vez establecida la conexión.
if r1.status == 404: # Comprobamos si hay un error en el recurso, mediante el estado, sabiendo que si es 200 (OK) y 404 (ERROR)
    print("ERROR, recurso no encontrado.")
    exit(1)
print(r1.status, r1.reason)  # Imprimimos la linea de estado de la respuesta (status:200, reason:OK)
info_raw = r1.read().decode("utf-8")  # Convertimos el código en una cadena.
conexion.close()
info = json.loads(info_raw)  # transformamos la información en cadena, en diccionario (info), para un mejor uso.

print("-> El id es", info['results'][0]['id'])
print("-> El proposito del producto es", info['results'][0]['purpose'][0])
print("-> El nombre del fabricante es", info['results'][0]['openfda']['manufacturer_name'][0])
# Para obtener información, nos metemos en el diccionario info, en la clave 'results', dentro de ella, en
# la subclave '0', y una vez ahí, buscamos la información según nos pida el ejercicio.
