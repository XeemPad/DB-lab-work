SELECT MAX(`order_id`) as `order_id`
FROM `order` 
WHERE `buye_id` = $e_user_id AND `order_datetime` = '$e_order_date';