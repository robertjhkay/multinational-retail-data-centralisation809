--Which month in which year produced the highest sales?
--+-------------+------+-------+
--| total_sales | year | month |
--+-------------+------+-------+
--|    27936.77 | 1994 |     3 |
--|    27356.14 | 2019 |     1 |
--|    27091.67 | 2009 |     8 |
--|    26679.98 | 1997 |    11 |
--|    26310.97 | 2018 |    12 |
--|    26277.72 | 2019 |     8 |
--|    26236.67 | 2017 |     9 |
--|    25798.12 | 2010 |     5 |
--|    25648.29 | 1996 |     8 |
--|    25614.54 | 2000 |     1 |
--+-------------+------+-------+
WITH ranked_sales AS (
    SELECT
        SUM(dp.product_price * ot.product_quantity) AS total_sales,
        dt.year AS year,
        dt.month AS month,
        ROW_NUMBER() OVER (PARTITION BY dt.year ORDER BY SUM(dp.product_price * ot.product_quantity) DESC) AS row_num
    FROM
        orders_table AS ot
    JOIN
        dim_products AS dp ON ot.product_code = dp.product_code
    JOIN
        dim_date_times AS dt ON ot.date_uuid = dt.date_uuid
    GROUP BY
        dt.year,
        dt.month
)
SELECT
    total_sales,
    year,
    month
FROM
    ranked_sales
WHERE
    row_num = 1
ORDER BY
	total_sales DESC