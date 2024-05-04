import requests
num = 4;
api_url = "https://opensky-network.org/api/states/all?lamin=48.8135&lomin=-123.7015&lamax=49.4306&lomax=-122.2843"
response = requests.get(api_url)
print(response.json())

# import requests

# url = "https://opensky-network.org/api/states/all?lamin=48.8135&lomin=-123.7015&lamax=49.4306&lomax=-122.2843"

# payload = {}
# headers = {
#   'Authorization': 'Basic SkdpbGJlcmc6S29kYWsyMjA5',
#   'Cookie': 'XSRF-TOKEN=7b7b99c3-c8f5-420d-a941-1560c7423dc9'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
