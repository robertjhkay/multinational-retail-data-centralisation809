--Which german store is selling the most?
--+--------------+-------------+--------------+
--| total_sales  | store_type  | country_code |
--+--------------+-------------+--------------+
--|   198373.57  | Outlet      | DE           |
--|   247634.20  | Mall Kiosk  | DE           |
--|   384625.03  | Super Store | DE           |
--|  1109909.59  | Local       | DE           |
--+--------------+-------------+--------------+
SELECT
    SUM(dp.product_price * ot.product_quantity) AS total_sales,
    ds.store_type,
    ds.country_code
FROM
    orders_table AS ot
JOIN
    dim_products AS dp ON ot.product_code = dp.product_code
JOIN
    dim_store_details AS ds ON ot.store_code = ds.store_code
WHERE
    ds.country_code = 'DE'
GROUP BY
    ds.store_type, ds.country_code
ORDER BY
    total_sales