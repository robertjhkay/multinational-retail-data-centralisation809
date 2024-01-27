WITH converted_dates AS (
    SELECT
        dt.year,
        CAST(dt.month AS INTEGER) AS numeric_month,
        CAST(dt.day AS INTEGER) AS numeric_day,
        dt.timestamp AS current_sale,
        LEAD(dt.timestamp, 1) OVER (ORDER BY dt.year, CAST(dt.month AS INTEGER), CAST(dt.day AS INTEGER), dt.timestamp) AS next_sale
    FROM
        orders_table AS ot
    JOIN
        dim_date_times AS dt ON ot.date_uuid = dt.date_uuid
)
SELECT
    year,
    numeric_month,
    numeric_day,
    current_sale,
    next_sale,
    (next_sale - current_sale)::interval AS time_diff
FROM
    converted_dates;
