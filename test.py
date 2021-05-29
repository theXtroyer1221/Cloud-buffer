import requests

url = "https://freegeoip.app/json/"

headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)