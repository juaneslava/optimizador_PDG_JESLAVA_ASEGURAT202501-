# Importa funciones específicas desde cada archivo
from exchanges.binance import get_order_book_binance                                  # Llama al libro de órdenes de Binance
from exchanges.kucoin import get_order_book_kucoin,   get_kucoin_symbol_format        # Llama al libro de órdenes de KuCoin
from utils.simulation import simulate_order                                           # Lógica de simulación (VWAP, fee, resultado)
from utils.optimization import optimize_distribution                                  # Lógica de optimización (distribución entre exchanges)
from config import BINANCE_FEE, KUCOIN_FEE                                            # Carga de configuración de fees

if __name__ == "__main__":

    # === 1. Datos al usuario ===
    print("=== SIMULADOR DE ORDEN DE COMPRA O VENTA EN BINANCE Y KUCOIN ===\n")
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
    kucoin_pair = get_kucoin_symbol_format(pair_input)  # Convierte a formato KuCoin (con guiones)
    print(f"Par en Binance: {binance_pair}")
    print(f"Par en KuCoin: {kucoin_pair}")
    # Extraer base y quote desde el formato KuCoin
    base, quote = kucoin_pair.split("-")
    unidad = base if amount_type == "base" else quote


    # === 3. Obtener y simular en BINANCE ===
    binance_order_book = get_order_book_binance(binance_pair)  # Llama al libro de Binance

    binance_result = None  # Resultado por defecto (por si hay error)

    if binance_order_book:
        # Simula la orden en Binance si hay datos
        binance_result = simulate_order(
            binance_order_book,
            operation_type,
            amount,
            amount_type,
            BINANCE_FEE
        )

    # === 4. Obtener y simular en KUCOIN ===
    kucoin_order_book = get_order_book_kucoin(kucoin_pair)  # Llama al libro de KuCoin

    kucoin_result = None  # Resultado por defecto

    if kucoin_order_book:
        # Simula la orden en KuCoin si hay datos
        kucoin_result = simulate_order(
            kucoin_order_book,
            operation_type,
            amount,
            amount_type,
            KUCOIN_FEE
        )

    # === 5. Mostrar resultados comparativos si ambos existen ===
    if binance_result and kucoin_result:
        print("\n--- COMPARACIÓN ENTRE EXCHANGES ---")
        print("\n📘 Explicación de columnas:")
        print("- Precio Prom.: Precio promedio ponderado al ejecutar tu orden.")
        print("- Fee: Comisión del exchange por usar orden de mercado.")
        print("- Total Final: Valor que realmente pagas (compra) o recibes (venta) luego del fee.\n")

        print("Exchange | Precio Prom. | Fee | Total Final")
        print("----------------------------------------------")
        print(f"Binance  | {round(binance_result['average_price'], 5)} | {binance_result['taker_fee']} | {binance_result['final_total']}")
        print(f"KuCoin   | {round(kucoin_result['average_price'], 5)} | {kucoin_result['taker_fee']} | {kucoin_result['final_total']}")
    else:
        print("No fue posible obtener los datos de ambos exchanges.")
    
    # === 6. OPTIMIZACIÓN AUTOMÁTICA ENTRE EXCHANGES ===
    #print("\n--- OPTIMIZACIÓN AUTOMÁTICA ---")

    order_books = [binance_order_book, kucoin_order_book]
    fees = [BINANCE_FEE, KUCOIN_FEE]

    optimization_result = optimize_distribution(
        order_books, fees, operation_type, amount, amount_type
    )

    opt_dist = optimization_result["optimal_distribution"]
    opt_total = optimization_result["total_final"]
    opt_results = optimization_result["results"]

    # === 7. TABLA COMPARATIVA FINAL ===
    print("\n--- TABLA COMPARATIVA FINAL ---\n")

    print("📘 Explicación de columnas:")
    print("- Precio Prom.: Precio promedio ponderado al ejecutar tu orden.")
    print("- Fee: Comisión del exchange por usar orden de mercado.")
    print("- Total Final: Valor que realmente pagas (compra) o recibes (venta) luego del fee.")
    print("- % Óptimo: Proporción de la orden asignada por el optimizador.")
    print("- Valor asignado: Monto exacto asignado a ese exchange.\n")

    print("Exchange | Precio Prom. | Fee     | Total Final | % Óptimo | Valor asignado")
    print("-------------------------------------------------------------------------")

    for i, exchange in enumerate(["Binance", "KuCoin"]):
        avg_price = round(opt_results[i]["average_price"], 4)
        fee = round(opt_results[i]["taker_fee"], 4)
        final = round(opt_results[i]["final_total"], 4)
        pct = round(opt_dist[i]*100, 2)
        valor = round(opt_dist[i] * amount, 6) 

        print(f"{exchange:<8} | {avg_price:<13} | {fee:<7} | {final:<11} | {pct:<8}% | {valor} {unidad}")

    unidad_resultado = quote if amount_type == "base" else base

    print("-------------------------------------------------------------------------")
    print(f"🧮 Resultado total optimizado: {round(opt_total, 4)} {unidad_resultado}")


    print("\n--- FIN DEL SIMULADOR ---")

