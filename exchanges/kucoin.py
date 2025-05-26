import requests

def get_order_book_kucoin(symbol, limit=100):
    """
    Obtiene el order book del par dado desde KuCoin.
    
    symbol: ejemplo 'ETH-USDT' (con guión)
    """
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol={symbol}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "bids": [[float(p), float(q)] for p, q in data["data"]["bids"]],
            "asks": [[float(p), float(q)] for p, q in data["data"]["asks"]]
        }
    else:
        print(f"Error al obtener datos de KuCoin: {response.status_code}")
        return None

def get_kucoin_symbol_format(input_pair):
    """
    Convierte un par como 'ETHUSDT' en el formato 'ETH-USDT' usado por KuCoin,
    verificando contra su lista oficial de símbolos.
    """
    response = requests.get("https://api.kucoin.com/api/v1/symbols")

    if response.status_code != 200:
        print("No se pudo obtener la lista de pares de KuCoin")
        return None

    data = response.json()["data"]

    for item in data:
        base = item["baseCurrency"]
        quote = item["quoteCurrency"]
        if input_pair == base + quote:
            return f"{base}-{quote}"

    print(f"No se encontró el par '{input_pair}' en KuCoin.")
    return None