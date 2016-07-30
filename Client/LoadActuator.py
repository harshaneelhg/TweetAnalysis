# This script is used for testing requests. This scripts randomly fires REST API
# calls on the server to test its capacity to handle requests.
# To do that is loads one of the fragments of Twitter data from /TwitterData folder
# and randomly chooses one of the requests to fire on the server. To increase the
# volume of the requests one can run multiple instances of this program with different
# fragments of the data.

import requests

url = 'http://localhost:8080/api/login'
data = {'username':'Harsh', 'password':'123'}

response = requests.post(url, data=data)
print response.json()
