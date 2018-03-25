import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=100', None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)#transformamos el documento en diccionario

for num_obj in range(len(repos['results'])):
    try:
        print("El fabricante", num_obj, "es:", repos['results'][num_obj]['openfda']['manufacturer_name'][0])
    except KeyError:
        print("El fabricante", num_obj, "no tiene fabricante especificado.")

