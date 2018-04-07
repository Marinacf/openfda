import http.client
import json

headers = {'User-Agent': 'http-client'}

try:
    conexion = http.client.HTTPSConnection("api.fda.gov")
    conexion.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=100', None, headers)
except Exception:
    print("Error al solicitar el nombre del servidor")
    exit(1)
r1 = conexion.getresponse()
if r1.status == 404:
    print("ERROR, recurso no encontrado")
    exit(1)
print(r1.status, r1.reason)
info_raw = r1.read().decode("utf-8")
conexion.close()

info = json.loads(info_raw)

for num_obj in range(len(info['results'])):
    if info['results'][num_obj]['openfda']:
        print("*El 'numero de results'", num_obj, ", tiene el fabricante:", info['results'][num_obj]['openfda']['manufacturer_name'][0])
    else:
        print("*El 'numero de results'", num_obj, ", no tiene fabricante especificado.")

#  Para encontrar todos aquellos fabricantes de las aspirinas, utilizamos un limit en el mensaje
#  de petición, de modo que nos devolverá todos aquellos archivos que coincidan con la busqueda
#  manual realizada (search=active ingredient:'acetylsalicylic'). Para obtener información, realizamos un bucle
# for iterando sobre todos aquellos archivos que coincidieron con el 'search', recalcando que: si no existe la
# información buscada, printeemos que no existe un fabricante especificado (usando un if-else).
#  Debido a que solo nos dan 4 resultados, no hace falta incluir ningun otro parametro, con el limit basta.
