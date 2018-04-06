import http.client
import json

headers = {'User-Agent': 'http-client'}
skip=0
while True:
    try:
        conexion = http.client.HTTPSConnection("api.fda.gov")
        conexion.request("GET", '/drug/label.json?search=substance_name:"ASPIRIN"&limit=100&skip='+str(skip), None, headers)
    except Exception:
        print("Error al solicitar el nombre del servidor.")
        exit(1)
    r1 =conexion.getresponse()
    if r1.status == 404:
        print("ERROR, recurso no encontrado.")
        exit(1)
    print(r1.status, r1.reason)
    info_raw = r1.read().decode("utf-8")
    conexion.close()
    info = json.loads(info_raw)  # transformamos el documento en diccionario
    for num_obj in range(len(info['results'])):
        if info['results'][num_obj]['openfda']:
            print("El fabricante", num_obj, "es:", info['results'][num_obj]['openfda']['manufacturer_name'][0])
        else:
            print("*El 'numero de results'", num_obj, "no tiene fabricante especificado.")
    if (len(info['results'])) < 100:
            break
    skip = skip + 100

 # En este caso, para encontrar los fabricantes de las aspirinas, en vez de buscarlos por su principio activo, los
 # buscamos mediante el 'nombre de sustancia', y al obtener mediante el limit, los 100 resultados que nos posibilita
 # este recurso, debemos asegurarnos de que estamos obteniendo todos los posibles, para ello usamos skip.
 # Skip nos permitirá, mediante un bucle infinito y el cambio de su valor, llegar a todos aquellos valores que
 # limit no habia podido obtener, y que concuerden con el search. En el momento en que los resultados restantes fueran
 # menores que 100 (el limite de limit), cerrariamos el bucle, habiendo obtenido todos los fabricantes de las aspirinas.