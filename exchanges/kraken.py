import requests

def get_order_book_kraken(symbol, limit=100):
    """
    Obtiene el libro de órdenes de Kraken para un par dado.
    Adapta el símbolo si es necesario (e.g., BTC → XBT).
    """

    # === Convertir a formato Kraken (XBT para BTC) ===
    symbol = symbol.upper().replace("BTC", "XBT")

    # === Verificar si Kraken soporta el par ===
    pairs_response = requests.get("https://api.kraken.com/0/public/AssetPairs")
    if pairs_response.status_code != 200:
        print("❌ No se pudo verificar la lista de pares de Kraken.")
        return None

    pairs_data = pairs_response.json().get("result", {})

    # Buscar el nombre de par válido
    kraken_pair = None
    for k, v in pairs_data.items():
        altname = v.get("altname")
        if altname == symbol:
            kraken_pair = k
            break

    if not kraken_pair:
        print(f"❌ El par {symbol} no está disponible en Kraken.")
        return None

    # === Obtener el libro de órdenes ===
    url = f"https://api.kraken.com/0/public/Depth?pair={kraken_pair}&count={limit}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["result"]
        book_data = list(data.values())[0]

        return {
            "bids": [[float(p), float(q)] for p, q, *_ in book_data["bids"]],
            "asks": [[float(p), float(q)] for p, q, *_ in book_data["asks"]],
        }
    else:
        print(f"❌ Error al obtener el libro de órdenes: {response.status_code}")
        return None
