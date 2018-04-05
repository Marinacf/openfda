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
    try:
        print("*El 'numero de results'", num_obj, ", tiene el fabricante:", info['results'][num_obj]['openfda']['manufacturer_name'][0])
    except KeyError:
        print("*El 'numero de results'", num_obj, ", no tiene fabricante especificado.")

#  Para encontrar todos aquellos fabricantes de las aspirinas, utilizamos un limit en el mensaje
#  de peticion, de modo que nos devolvera todos aquellos archivos que coincidan con la busqueda
#  manual realizada (search parameter). Para obtener informacion, realizamos un bucle for sobre
#  todos aquellos archivos que coincidieron con el 'search', recalcando que si no exite la info
#  buscada, hagamos un except con dicho KeyError.
#  Debido a que solo nos dan 4 resultados, no hace falta incluir ningun otro parametro, con el limit basta.
