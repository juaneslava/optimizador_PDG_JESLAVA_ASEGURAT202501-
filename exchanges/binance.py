import requests

def get_order_book_binance(symbol, limit=100):
    url = f'https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "bids": [[float(p), float(q)] for p, q in data["bids"]],
            "asks": [[float(p), float(q)] for p, q in data["asks"]]
        }
    else:
        print(f"Error al obtener datos: {response.status_code}")
        return None
