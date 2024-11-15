SELECT product_name AS 'Название продукта', monthlyOrders AS 'Количество покупок',
    monthlyRevenue AS 'Выручка от продукта'
FROM product_popularity_report
WHERE year='$year' AND month='$month';