import json
import requests

payload = {
    'q': "london",
    'units': 'metric',
    'appid': 'd4783db24d0d806b60afb366ceea4d7e'
}
r = requests.get('http://api.openweathermap.org/data/2.5/weather',
                    params=payload)
data = r.json()

print(data['main']['temp'])