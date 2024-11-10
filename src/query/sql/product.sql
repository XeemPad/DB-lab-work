SELECT prod_name, prod_price, prod_amount, prod_measure
FROM product JOIN category ON prod_category=category.id 
WHERE cat_name = "$prod_category";
