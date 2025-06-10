import os
from datetime import datetime
import matplotlib.pyplot as plt

def plot_distribution(exchange_names, distribution, filename_prefix="grafico_resultado"):
    """
    Muestra y guarda un gráfico de barras con la distribución óptima.
    """
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/{filename_prefix}_{timestamp}.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(exchange_names, [p * 100 for p in distribution], color='skyblue', edgecolor='black')

    for bar, pct in zip(bars, distribution):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{pct*100:.2f}%", 
                ha='center', va='bottom')

    ax.set_ylabel("Distribución óptima (%)")
    ax.set_title("Distribución óptima por exchange")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"📊 Gráfico de distribución guardado en: {filename}")


def plot_full_execution_comparison(exchange_names, final_totals, opt_total, filename_prefix="grafico_comparacion_full"):
    """
    Crea un gráfico de barras comparando la ejecución completa en cada exchange vs el resultado optimizado.
    """
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/{filename_prefix}_{timestamp}.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(exchange_names, final_totals, color='lightcoral', edgecolor='black')

    ax.axhline(opt_total, color='green', linestyle='--', linewidth=2, label=f"Optimizado: ${round(opt_total, 2)}")

    for bar, total in zip(bars, final_totals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f"${round(total, 2)}", 
                ha='center', va='bottom')

    ax.set_ylabel("Total final (USDT)")
    ax.set_title("Resultado al ejecutar el 100% en cada exchange")
    ax.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"📊 Gráfico de comparación guardado en: {filename}")


