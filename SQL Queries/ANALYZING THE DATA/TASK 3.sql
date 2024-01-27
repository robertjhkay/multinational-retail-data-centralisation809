--Which months have produced the most sales?
--+-------------+-------+
--| total_sales | month |
--+-------------+-------+
--|   673295.68 |     8 |
--|   668041.45 |     1 |
--|   657335.84 |    10 |
--|   650321.43 |     5 |
--|   645741.70 |     7 |
--|   645463.00 |     3 |
--+-------------+-------+
SELECT
    SUM(dp.product_price*ot.product_quantity) AS sales,
	dt.month
FROM
    orders_table AS ot
JOIN
    dim_date_times AS dt ON ot.date_uuid = dt.date_uuid
JOIN
    dim_products AS dp ON ot.product_code = dp.product_code
GROUP BY
	dt.month
ORDER BY
    sales DESC
