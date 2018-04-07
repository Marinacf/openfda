import http.client
import json

headers = {'User-Agent': 'http-client'}
try:
    conexion = http.client.HTTPSConnection("api.fda.gov")
    conexion.request("GET", "/drug/label.json?limit=10", None, headers)
except Exception:
    print("Error al solicitar el nombre del servidor")
    exit(1)
r1 = conexion.getresponse()
if r1.status==404:
    print("ERROR, recurso no encontrado.")
    exit(1)
print(r1.status, r1.reason)
info_raw = r1.read().decode("utf-8")
conexion.close()
info = json.loads(info_raw)

for num_obj in range(len(info['results'])):
    print("-El id", num_obj, "es:", info['results'][num_obj]['id'])
#  Para obtener diez objetos que coincidan con mi búsqueda, utilizo limit cuando mandamos el msj
#  de solicitud. Para adquirir información concreta de cada uno de los objetos, hago uso de un bucle for.
