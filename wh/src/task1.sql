SELECT id, first_name, last_name 
FROM customers
WHERE id IN 
(
    SELECT customer_id 
    FROM 
    (
       SELECT customer_id, MIN(created_at) 
       FROM orders
       GROUP BY customer_id 
       HAVING MIN(created_at) >= NOW() - INTERVAL '24 hours'
    ) AS ord 
)


SELECT id, first_name, last_name 
FROM customers   
WHERE id IN (
    SELECT orders.customer_id 
    FROM (
            SELECT orders.customer_id, 
            ROW_NUMBER() OVER (PARTITION BY orders.customer_id ORDER BY orders.created_at) as order_number
            FROM orders  
        ) as ord
        WHERE ord.order_number IN (2, 3) AND ord.created_at >= NOW() - INTERVAL '24 hours'
    );