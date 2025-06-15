import time
import csv
import random

from datetime import datetime

from exchanges.binance import get_order_book_binance
from exchanges.kucoin import get_order_book_kucoin, get_kucoin_symbol_format
from exchanges.kraken import get_order_book_kraken
from exchanges.coinbase import get_order_book_coinbase, get_coinbase_symbol_format
from utils.simulation import simulate_order
from utils.optimization import optimize_distribution
from config import BINANCE_FEE, KUCOIN_FEE, KRAKEN_FEE, COINBASE_FEE

# === CONFIGURACIÓN MANUAL ===
operation_type = "sell"          # 'buy' o 'sell'
pair_input = "ETHUSDT"          # Ejemplo de par
amount = amount = 0  # Monto aleatorio entre 120 y 200
amount_type = "base"            # 'base' o 'quote'
intervalo_min = 1               # Tiempo entre ejecuciones
archivo_csv = "resultados_benchmark_sell_2.csv"

# === Inicializar archivo CSV si no existe ===
try:
    with open(archivo_csv, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp", "operacion", "par", "cantidad", "tipo_cantidad",
            "total_binance", "total_kucoin", "total_kraken", "total_coinbase",
            "total_optimizado", "ahorro"
        ])
except FileExistsError:
    pass

# === LOOP DE EJECUCIÓN AUTOMÁTICA ===
while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount = amount = round(random.uniform(120, 200), 2)  # Monto aleatorio entre 120 y 200
    print(f"\n⏳ Ejecutando simulación a las {timestamp}...")

    try:
        # Ajustar formato
        binance_pair = pair_input
        kucoin_pair = get_kucoin_symbol_format(pair_input)
        kraken_pair = pair_input
        coinbase_pair = get_coinbase_symbol_format(pair_input)

        # Obtener order books
        binance_book = get_order_book_binance(binance_pair)
        kucoin_book = get_order_book_kucoin(kucoin_pair)
        kraken_book = get_order_book_kraken(kraken_pair)
        coinbase_book = get_order_book_coinbase(coinbase_pair)

        order_books = [binance_book, kucoin_book, kraken_book, coinbase_book]
        fees = [BINANCE_FEE, KUCOIN_FEE, KRAKEN_FEE, COINBASE_FEE]

        if any(book is None for book in order_books):
            raise Exception("❌ No se pudo obtener uno de los libros de órdenes.")

        # Simulación 100% por exchange
        resultados_full = []
        for i in range(4):
            res = simulate_order(order_books[i], operation_type, amount, amount_type, fees[i])
            resultados_full.append(res["final_total"])

        # Simulación optimizada
        resultado_opt = optimize_distribution(order_books, fees, operation_type, amount, amount_type)
        total_opt = resultado_opt["total_final"]

        # Ahorro
        mejor_full = min(resultados_full) if operation_type == "buy" else max(resultados_full)
        ahorro = mejor_full - total_opt if operation_type == "buy" else total_opt - mejor_full

        # Guardar resultados
        with open(archivo_csv, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, operation_type, pair_input, amount, amount_type,
                round(resultados_full[0], 4),
                round(resultados_full[1], 4),
                round(resultados_full[2], 4),
                round(resultados_full[3], 4),
                round(total_opt, 4),
                round(ahorro, 6)
            ])
        print(f"✅ Guardado en CSV. Ahorro: {round(ahorro, 6)}")

    except Exception as e:
        print(f"⚠️ Error en ejecución: {e}")

    time.sleep(intervalo_min * 60)

