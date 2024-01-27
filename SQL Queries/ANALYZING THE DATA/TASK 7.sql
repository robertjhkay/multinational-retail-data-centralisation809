--What is our staff headcount?
--+---------------------+--------------+
--| total_staff_numbers | country_code |
--+---------------------+--------------+
--|               13307 | GB           |
--|                6123 | DE           |
--|                1384 | US           |
--+---------------------+--------------+
SELECT
	SUM(staff_numbers) AS total_staff_numbers,
	country_code
FROM
	dim_store_details
GROUP BY
	country_code
ORDER BY
	total_staff_numbers DESC