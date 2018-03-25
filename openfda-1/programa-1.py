import http.client  # importamos aquellos modulos que vayamos a utilizar posteriormente.
import json

headers = {'User-Agent': 'http-client'}
conexion = http.client.HTTPSConnection("api.fda.gov")  # nos conectamos con la pagina pedida por el ej.
conexion.request("GET", "/drug/label.json", None, headers)  # Le mandamos un mensaje de solicitud (verbo:GET).
r1 = conexion.getresponse()  # Leer el mensaje que se recibe
print(r1.status, r1.reason)  # Imprimimos la lina de estado de la respuesta (status:200, reason:OK)
info_raw = r1.read().decode("utf-8")  # Convertimos el codigo en una cadena
conexion.close()
info = json.loads(info_raw)  # transformamos la informacion en cadena, en diccionario, para un mejor uso.

print("El id es", info['results'][0]['id'])
print("El proposito del producto es", info['results'][0]['purpose'][0])
print("El nombre del fabricante es", info['results'][0]['openfda']['manufacturer_name'][0])
# Para obtener informacion, nos metemos en el diccionario info, en la clave 'results', dentro de ella, en
# la subclave '0', y una vez ahi buscamos la informacion segun nos pida el ejercicio.
