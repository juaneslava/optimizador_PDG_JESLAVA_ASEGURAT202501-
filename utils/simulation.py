def simulate_order(order_book, operation_type, amount, amount_type, fee_rate):
    book_side = order_book["asks"] if operation_type == "buy" else order_book["bids"]

    executed_volume = 0
    executed_cost = 0

    for price, qty in book_side:
        if amount_type == "quote":  # operar con USDT
            cost_to_spend = price * qty
            if executed_cost + cost_to_spend >= amount:
                remaining = amount - executed_cost
                partial_qty = remaining / price
                executed_volume += partial_qty
                executed_cost += remaining
                break
            else:
                executed_volume += qty
                executed_cost += cost_to_spend
        else:  # operar con ETH directamente
            if executed_volume + qty >= amount:
                partial_qty = amount - executed_volume
                executed_volume += partial_qty
                executed_cost += partial_qty * price
                break
            else:
                executed_volume += qty
                executed_cost += qty * price

    average_price = executed_cost / executed_volume
    total_fee = executed_cost * fee_rate
    total_spent = executed_cost + total_fee if operation_type == "buy" else executed_cost - total_fee

    return {
        "operation": operation_type,
        "amount_requested": amount,
        "executed_volume": executed_volume,
        "average_price": round(average_price, 6),
        "total_cost_before_fee": round(executed_cost, 2),
        "taker_fee": round(total_fee, 2),
        "final_total": round(total_spent, 2)
    }
