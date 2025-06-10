# Importa funciones específicas desde cada archivo
from exchanges.binance import get_order_book_binance                                 # Llama al libro de órdenes de Binance
from exchanges.kucoin import get_order_book_kucoin, get_kucoin_symbol_format         # Llama al libro de órdenes de KuCoin
from exchanges.kraken import get_order_book_kraken                                   # Llama al libro de órdenes de Kraken
from exchanges.coinbase import get_order_book_coinbase, get_coinbase_symbol_format   # Llama al libro de órdenes de Coinbase (opcional)
from utils.simulation import simulate_order                                          # Lógica de simulación (VWAP, fee, resultado)
from utils.optimization import optimize_distribution                                 # Lógica de optimización (distribución entre exchanges)
from utils.visualization import plot_distribution,   plot_full_execution_comparison                               # Lógica de visualización (gráfico de barras)
from config import BINANCE_FEE, KUCOIN_FEE, KRAKEN_FEE, COINBASE_FEE                 # Carga de configuración de fees

if __name__ == "__main__":

    # === 1. Datos al usuario ===
    print("=== SIMULADOR DE ORDEN DE COMPRA O VENTA EN BINANCE, KRAKEN Y KUCOIN ===\n")
    print("👉 Tipos de operación: 'buy' (comprar), 'sell' (vender)")
    print("👉 Par de trading: ejemplo 'ETHUSDT', 'BTCUSDT', 'ADAETH'")
    print("   (Base = lo que compras o vendes, Quote = con qué lo haces)")
    print("👉 Cantidad: monto a operar (ej: 2.8 si vendes ETH)")
    print("👉 Tipo de cantidad:")
    print("   - 'base' si escribiste la cantidad en la criptomoneda (ej: ETH)")
    print("   - 'quote' si escribiste el monto en USDT, BTC, etc.\n")

    # Obtener tipo de operación
    while True:
        operation_type = input("¿Quieres comprar o vender? (buy/sell): ").lower()
        if operation_type in ["buy", "sell"]:
            break
        print("❌ Entrada inválida. Escribe 'buy' o 'sell'.")

    # Obtener par
    pair_input = input("¿Qué par quieres operar? (ej: ETHUSDT): ").upper()

    # Obtener monto
    while True:
        try:
            amount = float(input("¿Cuánto quieres operar?: "))
            if amount > 0:
                break
            else:
                print("❌ El monto debe ser mayor que 0.")
        except ValueError:
            print("❌ Entrada inválida. Ingresa un número válido.")

    # Obtener tipo de cantidad con validación adicional
    while True:
        amount_type = input("¿Es cantidad en base o quote? (base/quote): ").lower()
        if amount_type in ["base", "quote"]:
            if operation_type == "sell" and amount_type == "quote":
                print("⚠️ No puedes vender indicando el monto en quote.")
                print("💡 Por favor indica cuánto del activo base deseas vender.")
            else:
                break
        else:
            print("❌ Entrada inválida. Escribe 'base' o 'quote'.")

    # === 2. Ajustar el formato del par según el exchange ===
    binance_pair = pair_input
    kucoin_pair = get_kucoin_symbol_format(pair_input)
    kraken_pair = pair_input  # Por ahora usamos el mismo formato, se ajusta dentro del script de Kraken
    coinbase_pair = get_coinbase_symbol_format(pair_input)
    print(f"Par en Kraken: {kraken_pair}")
    print(f"Par en Binance: {binance_pair}")
    print(f"Par en KuCoin: {kucoin_pair}")
    print(f"Par en Coinbase: {coinbase_pair}")
    base, quote = kucoin_pair.split("-")
    unidad = base if amount_type == "base" else quote

    # === 3. Obtener los order books solo una vez ===
    binance_order_book = get_order_book_binance(binance_pair)
    kucoin_order_book = get_order_book_kucoin(kucoin_pair)
    kraken_order_book = get_order_book_kraken(kraken_pair)
    coinbase_order_book = get_order_book_coinbase(coinbase_pair)

    if not binance_order_book or not kucoin_order_book or not kraken_order_book:
        print("❌ No se pudieron obtener los libros de órdenes. Intenta de nuevo.")
        exit()

    order_books = [binance_order_book, kucoin_order_book, kraken_order_book, coinbase_order_book]
    fees = [BINANCE_FEE, KUCOIN_FEE, KRAKEN_FEE, COINBASE_FEE]
    exchange_names = ["Binance", "KuCoin", "Kraken", "Coinbase"]


    # === 4. Ejecutar optimización con los mismos libros ===
    optimization_result = optimize_distribution(
        order_books, fees, operation_type, amount, amount_type
    )

    # === 5. Simulación de 100% en cada exchange con los mismos libros ===
    results_full = []
    for i in range(len(order_books)):
        result = simulate_order(
            order_books[i], operation_type, amount, amount_type, fees[i]
        )
        results_full.append(result)

    print("\n--- COMPARACIÓN ENTRE EXCHANGES (100% de la orden) ---\n")
    print("Exchange | Precio Prom. | Fee     | Total Final")
    print("----------------------------------------------")

    for i, exchange in enumerate(exchange_names):
        avg = round(results_full[i]["average_price"], 5)
        fee = results_full[i]["taker_fee"]
        total = results_full[i]["final_total"]
        print(f"{exchange:<8} | {avg:<13} | {fee:<7} | {total:<11}")

    # === 6. Mostrar tabla final optimizada ===
    opt_dist = optimization_result["optimal_distribution"]
    opt_total = optimization_result["total_final"]
    opt_results = optimization_result["results"]

    print("\n--- TABLA COMPARATIVA FINAL ---\n")
    print("Exchange | Precio Prom. | Fee     | Total Final | % Óptimo | Valor asignado")
    print("-------------------------------------------------------------------------")

    for i, exchange in enumerate(exchange_names):
        avg_price = round(opt_results[i]["average_price"], 4)
        fee = round(opt_results[i]["taker_fee"], 4)
        final = round(opt_results[i]["final_total"], 4)
        pct = round(opt_dist[i]*100, 2)
        valor = round(opt_dist[i] * amount, 6)
        print(f"{exchange:<8} | {avg_price:<13} | {fee:<7} | {final:<11} | {pct:<8}% | {valor} {unidad}")

    unidad_resultado = quote if amount_type == "base" else base
    
    print("-------------------------------------------------------------------------")
    print(f"🧮 Resultado total optimizado: {round(opt_total, 4)} {unidad_resultado}")
    exchange_names = ["Binance", "KuCoin", "Kraken", "Coinbase"]
    percentages = opt_dist
    final_totals = [res["final_total"] for res in opt_results]

    plot_distribution(exchange_names, percentages, final_totals)
    print("📊 Se generó el gráfico 'grafico_resultado.png' con la distribución óptima.")
    plot_full_execution_comparison(
        exchange_names, 
        [res["final_total"] for res in results_full],
        opt_total
    )
    print("📊 También se generó el gráfico 'grafico_comparacion_full.png' con la comparación 100%.")

    print("\n--- FIN DEL SIMULADOR ---")