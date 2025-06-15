import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# === 1. Cargar archivos CSV ===
buy_df = pd.read_csv("resultados_benchmark_buy.csv")
sell_df = pd.read_csv("resultados_benchmark_sell.csv")

# === 2. Limpiar y preparar ===
buy_df = buy_df[pd.to_datetime(buy_df["timestamp"], errors="coerce").notna()]
sell_df = sell_df[pd.to_datetime(sell_df["timestamp"], errors="coerce").notna()]
buy_df["tipo"] = "buy"
sell_df["tipo"] = "sell"
buy_df["timestamp"] = pd.to_datetime(buy_df["timestamp"])
sell_df["timestamp"] = pd.to_datetime(sell_df["timestamp"])

# === 3. Crear carpeta de salida de gráficas y resumen ===
os.makedirs("output/graficas_analisis", exist_ok=True)
log_path = os.path.join("output/graficas_analisis", "resumen.txt")
log_file = open(log_path, "w", encoding="utf-8")

def log_print(text):
    print(text)
    log_file.write(text + "\n")

# === 4. Ahorro acumulado por tipo ===
for tipo_df, tipo in zip([buy_df, sell_df], ["buy", "sell"]):
    tipo_df["ahorro_acumulado"] = tipo_df["ahorro"].cumsum()
    plt.figure()
    plt.plot(tipo_df["timestamp"], tipo_df["ahorro_acumulado"], marker='o')
    plt.title(f"Ahorro acumulado ({tipo})")
    plt.xlabel("Tiempo")
    plt.ylabel("Ahorro acumulado")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"output/graficas_analisis/ahorro_acumulado_{tipo}.png")

# === 5. Histograma del ahorro por operación ===
for tipo_df, tipo in zip([buy_df, sell_df], ["buy", "sell"]):
    plt.figure()
    tipo_df["ahorro"].hist(bins=20)
    plt.title(f"Histograma del ahorro por operación ({tipo})")
    plt.xlabel("Ahorro")
    plt.ylabel("Frecuencia")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"output/graficas_analisis/histograma_ahorro_{tipo}.png")

# === 6. Resumen por consola y archivo ===

def print_totales(df, tipo):
    log_print(f"\n=== Totales para operaciones '{tipo}' ===")
    total_binance = df["total_binance"].sum()
    total_kucoin = df["total_kucoin"].sum()
    total_kraken = df["total_kraken"].sum()
    total_coinbase = df["total_coinbase"].sum()
    total_optimizado = df["total_optimizado"].sum()
    total_operado = df["cantidad"].sum()

    log_print(f"→ Total operado: {round(total_operado, 4)} {df['tipo_cantidad'].iloc[0]}")
    log_print(f"→ Total Binance:   {round(total_binance, 4)}")
    log_print(f"→ Total KuCoin:    {round(total_kucoin, 4)}")
    log_print(f"→ Total Kraken:    {round(total_kraken, 4)}")
    log_print(f"→ Total Coinbase:  {round(total_coinbase, 4)}")
    log_print(f"→ Total Optimizado:{round(total_optimizado, 4)}")

    if tipo == "buy":
        peor = min(total_binance, total_kucoin, total_kraken, total_coinbase)
        ahorro = peor - total_optimizado
        porcentaje = (ahorro / peor) * 100
        log_print(f"✅ Ahorro total: {round(ahorro, 4)} → {round(porcentaje, 5)}% respecto al mejor exchange")
    elif tipo == "sell":
        mejor = max(total_binance, total_kucoin, total_kraken, total_coinbase)
        ganancia = total_optimizado - mejor
        porcentaje = (ganancia / mejor) * 100
        log_print(f"✅ Ganancia adicional total: {round(ganancia, 4)} → {round(porcentaje, 5)}% respecto al mejor exchange")

print_totales(buy_df, "buy")
print_totales(sell_df, "sell")

# Cerrar archivo de log
log_file.close()
