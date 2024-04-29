import requests
api_url = "https://opensky-network.org/api/states/all?lamin=48.8135&lomin=-123.7015&lamax=49.4306&lomax=-122.2843"
response = requests.get(api_url)
response.json()
print(response.json())