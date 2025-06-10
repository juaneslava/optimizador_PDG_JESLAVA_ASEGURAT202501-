import requests

def get_order_book_coinbase(symbol, limit=100):
    """
    Obtiene el libro de órdenes del par dado desde Coinbase Exchange.

    symbol: par como 'ETH-USD' (nota el guión en lugar de ETHUSD).
    """
    url = f"https://api.exchange.coinbase.com/products/{symbol}/book?level=2"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "bids": [[float(p), float(q)] for p, q, _ in data["bids"][:limit]],
            "asks": [[float(p), float(q)] for p, q, _ in data["asks"][:limit]],
        }
    else:
        print(f"Error al obtener datos de Coinbase: {response.status_code}")
        return None

def get_coinbase_symbol_format(input_pair):
    """
    Convierte un par como 'ETHUSDT' a 'ETH-USDT' para Coinbase.
    """
    if len(input_pair) >= 6:
        base = input_pair[:-4]
        quote = input_pair[-4:]
        return f"{base}-{quote}"
    return None
