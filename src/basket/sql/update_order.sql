UPDATE `order`
SET total_cost_rubles = $total_cost
WHERE order_id = $e_order_id;