--How quickly is the company making sales?
--+------+-------------------------------------------------------+
--| year |                           actual_time_taken           |
--+------+-------------------------------------------------------+
--| 2013 | "hours": 2, "minutes": 17, "seconds": 12, "millise... |
--| 1993 | "hours": 2, "minutes": 15, "seconds": 35, "millise... |
--| 2002 | "hours": 2, "minutes": 13, "seconds": 50, "millise... | 
--| 2022 | "hours": 2, "minutes": 13, "seconds": 6,  "millise... |
--| 2008 | "hours": 2, "minutes": 13, "seconds": 2,  "millise... |
--+------+-------------------------------------------------------+
WITH final_table AS (
	WITH actual_time_taken AS (
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
	    	converted_dates
	)
	SELECT
	    year,
	    numeric_month,
	    numeric_day,
	    current_sale,
	    next_sale,
		CASE WHEN EXTRACT(HOUR FROM time_diff) < 0 THEN INTERVAL '24 hour' + time_diff ELSE time_diff END AS actual_time_taken
	FROM
	    actual_time_taken
)
SELECT
	year,
	AVG(actual_time_taken) AS actual_time_taken
FROM
	final_table
GROUP BY
	year
ORDER BY
	actual_time_taken DESC