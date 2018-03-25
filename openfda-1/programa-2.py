import http.client
import json

headers = {'User-Agent': 'http-client'}
conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conexion.getresponse()
print(r1.status, r1.reason)
info_raw = r1.read().decode("utf-8")
conexion.close()
info = json.loads(info_raw)

for num_obj in range(len(info['results'])):
    print("El id", num_obj, "es:", info['results'][num_obj]['id'])
#  Para obtener diez objetos que coincidan con mi busqueda, utilizo limit (cuando mandamos el msj
#  de solicitud. Y para obtener informacion de cada uno, hago uso de un bucle for.
