import requests
import json

url = 'http://0.0.0.0:5000/api/'


text= "how install python" #"How can I r r r r r check if a keyboard modifier is pressed (Shift, Ctrl, or Alt)"
data = [text]
# data = [input()]
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)