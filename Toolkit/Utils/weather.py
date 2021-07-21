import json,requests
def weather(city, key):
    api_key = key
    uul = ("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key)
    url = uul
    response = requests.get(url)
    data = json.loads(response.text)
    return data