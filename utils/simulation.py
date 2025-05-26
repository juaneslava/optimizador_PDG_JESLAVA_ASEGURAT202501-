def simulate_order(order_book, operation_type, amount, amount_type, fee_rate):
    """
    Simula la ejecución de una orden de mercado:
    - Recorre el libro (asks o bids) hasta llenar el monto solicitado.
    - Calcula precio promedio, fees, y resultado total.
    """
    # Elegir el lado del libro según si compras o vendes
    book_side = order_book["asks"] if operation_type == "buy" else order_book["bids"]

    executed_volume = 0       # Cuántos ETH compras o vendes
    executed_cost = 0         # Cuánto pagas o recibes en USDT

    # Recorrer el libro nivel por nivel
    for price, qty in book_side:
        if amount_type == "quote":
            # El usuario especificó su monto en quote (ej: USDT)
            cost_to_spend = price * qty  # Lo que costaría ese nivel
            if executed_cost + cost_to_spend >= amount:
                # Solo necesitamos una fracción de este nivel
                remaining = amount - executed_cost
                partial_qty = remaining / price
                executed_volume += partial_qty
                executed_cost += remaining
                break
            else:
                executed_volume += qty
                executed_cost += cost_to_spend
        else:
            # El usuario especificó su monto en base (ej: ETH)
            if executed_volume + qty >= amount:
                partial_qty = amount - executed_volume
                executed_volume += partial_qty
                executed_cost += partial_qty * price
                break
            else:
                executed_volume += qty
                executed_cost += qty * price

    # Precio promedio ponderado por volumen
    average_price = executed_cost / executed_volume

    # Calcular la comisión (fee)
    total_fee = executed_cost * fee_rate

    # Resultado total: si compras, pagas fee; si vendes, te descuentan el fee
    total_spent = executed_cost + total_fee if operation_type == "buy" else executed_cost - total_fee

    return {
        "operation": operation_type,
        "amount_requested": amount,
        "executed_volume": executed_volume,           # Cuánto ETH compraste o vendiste
        "average_price": round(average_price, 5),     # Precio promedio ponderado
        "total_cost_before_fee": round(executed_cost, 5),
        "taker_fee": round(total_fee, 5),
        "final_total": round(total_spent, 5)          # Total pagado (buy) o recibido (sell)
    }
 