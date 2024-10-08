import requests

n = int(input("Ingrese la cantidad de bitcoins que posee: "))

url="https://api.coindesk.com/v1/bpi/currentprice.json"
data=requests.get(url)
if data.status_code == 200:
    data = data.json()
    for e in data['bpi']:
        print(e['USD'])
