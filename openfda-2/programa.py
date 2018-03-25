import http.client
import json

headers = {'User-Agent': 'http-client'}

conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=100', None, headers)
r1 = conexion.getresponse()
print(r1.status, r1.reason)
info_raw = r1.read().decode("utf-8")
conexion.close()

info = json.loads(info_raw)

for num_obj in range(len(info['results'])):
    try:
        print("El fabricante", num_obj, "es:", info['results'][num_obj]['openfda']['manufacturer_name'][0])
    except KeyError:
        print("El fabricante", num_obj, "no tiene fabricante especificado.")
#  Para encontrar todos aquellos fabricantes de las aspirinas, utilizamos un limit en el mensaje
#  de peticion, de modo que nos devolvera todos aquellos archivos que coincidan con la busqueda
#  manual realizada (search parameter). Para obtener informacion, realizamos un bucle for sobre
#  todos aquellos archivos que coincidieron con el 'search', recalcando que si no exite la info
#  buscada, hagamos un except con dicho KeyError.
