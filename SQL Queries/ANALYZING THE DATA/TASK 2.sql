--Which locations have the most stores?
--+-------------------+-----------------+
--|     locality      | total_no_stores |
--+-------------------+-----------------+
--| Chapletown        |              14 |
--| Belper            |              13 |
--| Bushley           |              12 |
--| Exeter            |              11 |
--| High Wycombe      |              10 |
--| Arbroath          |              10 |
--| Rutherglen        |              10 |
--+-------------------+-----------------+
SELECT
	locality,
	COUNT(locality) AS total_no_stores
FROM
	dim_store_details
GROUP BY
	locality
HAVING
	COUNT(locality) > 9
ORDER BY
    total_no_stores DESC