import http.client
import json

headers = {'User-Agent': 'http-client'}
skip_num=0
while True:
    try:
        conexion = http.client.HTTPSConnection("api.fda.gov")
        conexion.request("GET", '/drug/label.json?search=substance_name:"ASPIRIN"+active_ingredient:"acetylsalicylic"&limit=100&skip='+str(skip_num), None, headers)
        #  En este caso buscamos resultados que concuerden con cualquiera de los dos campos, aspirina o su principio activo
        #  Y si pusieramos +AND+ en vez de un solo +, buscariamos aquellos resultados que concordasen(match) con ambos
        #  campos a la vez. Tambien usamos skip por la misma razón que en el programa  que unicamente usamos el 'nombre de la sustancia'.

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
    skip_num = skip_num + 100