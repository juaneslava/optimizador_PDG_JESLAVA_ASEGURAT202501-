from exchanges.binance import get_order_book_binance
from utils.simulation import simulate_order
from config import BINANCE_FEE

if __name__ == "__main__":
    # Entrada por consola
    operation_type = input("¿Quieres comprar o vender? (buy/sell): ").lower()
    pair = input("¿Qué par quieres operar? (ej: ETHUSDT): ").upper()
    amount = float(input("¿Cuánto quieres operar?: "))
    amount_type = input("¿Es cantidad en base o quote? (base/quote): ").lower()

    # Obtener order book de Binance
    order_book = get_order_book_binance(pair)
    if order_book:
        result = simulate_order(order_book, operation_type, amount, amount_type, BINANCE_FEE)
        print(f"\nResultado en Binance:\n{result}")
    else:
        print("No se pudo obtener el order book.")
