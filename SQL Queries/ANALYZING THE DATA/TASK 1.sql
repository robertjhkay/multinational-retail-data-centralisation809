--How many stores in each country?
--+----------+-----------------+
--| country  | total_no_stores |
--+----------+-----------------+
--| GB       |             265 |
--| DE       |             141 |
--| US       |              34 |
--+----------+-----------------+
--Note: DE is short for Deutschland(Germ
SELECT
	country_code,
	COUNT(country_code)
FROM
	dim_store_details
GROUP BY
	country_code
ORDER BY
	count DESC 