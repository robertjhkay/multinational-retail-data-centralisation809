--How many sales are comming from online?
--+------------------+-------------------------+----------+
--| numbers_of_sales | product_quantity_count  | location |
--+------------------+-------------------------+----------+
--|            26957 |                  107739 | Web      |
--|            93166 |                  374047 | Offline  |
--+------------------+-------------------------+----------+
SELECT
	SUM(1) AS numbers_of_sales,
	SUM(ot.product_quantity) AS product_quantity_count,
	CASE WHEN ds.store_type = 'Web Portal' THEN 'Web' ELSE 'Offline' END AS location
FROM
	orders_table AS ot
JOIN
    dim_store_details AS ds ON ot.store_code = ds.store_code
GROUP BY
	location
ORDER BY
	numbers_of_sales
