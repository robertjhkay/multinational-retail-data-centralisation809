--What percentage of sales come through each type of store?
--+-------------+-------------+---------------------+
--| store_type  | total_sales | percentage_total(%) |
--+-------------+-------------+---------------------+
--| Local       |  3440896.52 |               44.87 |
--| Web portal  |  1726547.05 |               22.44 |
--| Super Store |  1224293.65 |               15.63 |
--| Mall Kiosk  |   698791.61 |                8.96 |
--| Outlet      |   631804.81 |                8.10 |
--+-------------+-------------+---------------------+
SELECT
	ds.store_type,
	SUM(dp.product_price*ot.product_quantity) AS total_sales,
	100*SUM(dp.product_price*ot.product_quantity)/
        (SELECT 
            SUM(dp.product_price*ot.product_quantity)
        FROM 
            orders_table AS ot
        JOIN
		 	dim_products dp ON ot.product_code = dp.product_code) 
    AS "percentage_total(%)"
FROM
	orders_table AS ot
JOIN
    dim_store_details AS ds ON ot.store_code = ds.store_code
JOIN
    dim_products AS dp ON ot.product_code = dp.product_code
GROUP BY
	store_type
ORDER BY
	total_sales DESC