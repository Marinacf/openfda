import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("https://api.fda.gov/drug/label.json")
conn.request("GET", "/users/Marinacf/repos", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

repo = repos[0]
print("The owner of the first repository is", repo['owner']['login'])



