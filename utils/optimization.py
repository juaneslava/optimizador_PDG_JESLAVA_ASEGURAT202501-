from scipy.optimize import minimize  # Importa el solver de optimización
from utils.simulation import simulate_order  # Función que simula la ejecución real en un exchange

def optimize_distribution(order_books, fees, operation_type, amount, amount_type):
    """
    Optimiza la distribución del monto total entre múltiples exchanges (actualmente 2).

    Parámetros:
    - order_books: lista de libros de órdenes (uno por exchange), con datos reales.
    - fees: lista de comisiones taker (una por exchange).
    - operation_type: 'buy' o 'sell'.
    - amount: cantidad total a operar.
    - amount_type: 'base' o 'quote'.

    El objetivo es minimizar (en compras) o maximizar (en ventas) el resultado total.
    """

    n = len(order_books)  # Número de exchanges (n)

    # === FUNCIÓN OBJETIVO ===
    def objective(x):
        """
        Función objetivo f(x), donde x es un vector con las proporciones x_i.

        En el caso de 'buy', se minimiza el costo total gastado.
        En el caso de 'sell', se maximiza el ingreso neto (minimizando su negativo).

        x: vector de proporciones, tal que sum(x) = 1 y 0 <= x_i <= 1.
        """
        total = 0
        for i in range(n):
            sub_amount = x[i] * amount  # Cantidad a operar en el exchange i (x_i * A)
            result = simulate_order(    # Evalúa f_i(x_i * A) con datos reales
                order_books[i], 
                operation_type, 
                sub_amount, 
                amount_type, 
                fees[i]
            )
            final = result["final_total"]  # Resultado neto (gasto o ingreso)
            total += final

        # Si estás comprando: quieres minimizar el total gastado
        # Si estás vendiendo: quieres maximizar el total recibido → minimizar el negativo
        return total if operation_type == "buy" else -total

    # === RESTRICCIÓN DE SUMA DE PROPORCIONES ===
    constraints = [{"type": "eq", "fun": lambda x: sum(x) - 1}]
    # Esto impone: sum(x_i) = 1

    # === LÍMITES DE LAS VARIABLES ===
    bounds = [(0, 1) for _ in range(n)]
    # Esto impone: 0 <= x_i <= 1 para cada exchange i

    # === VALOR INICIAL: DISTRIBUCIÓN UNIFORME ===
    x0 = [1 / n] * n

    # === EJECUTAR OPTIMIZACIÓN NUMÉRICA ===
    result = minimize(objective, x0, bounds=bounds, constraints=constraints)
    # Usa el método SLSQP por defecto para restricciones lineales y no lineales

    # === SIMULACIÓN FINAL USANDO LA DISTRIBUCIÓN ÓPTIMA ===
    allocation = result.x  # Vector solución óptima x* = [x_1*, x_2*, ..., x_n*]

    results_by_exchange = []
    for i in range(n):
        sub_amount = allocation[i] * amount  # Operación óptima asignada al exchange i
        result_i = simulate_order(           # Simulación real con esa cantidad
            order_books[i], 
            operation_type, 
            sub_amount, 
            amount_type, 
            fees[i]
        )
        results_by_exchange.append(result_i)

    # Calcular el resultado total neto final (suma de ingresos o gastos)
    total_final = sum(r["final_total"] for r in results_by_exchange)

    return {
        "optimal_distribution": allocation,       # Lista de proporciones óptimas
        "results": results_by_exchange,           # Resultados por exchange
        "total_final": total_final                # Resultado total global
    }
