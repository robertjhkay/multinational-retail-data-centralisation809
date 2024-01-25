-- The following creates a variable 'weight_class'
ALTER TABLE dim_products ADD COLUMN weight_class VARCHAR(14);
UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight BETWEEN 3 AND 40 THEN 'Mid_Sized'
    WHEN weight BETWEEN 41 AND 140 THEN 'Heavy'
    ELSE 'Truck_required'
END;

-- The following renames a variable
ALTER TABLE dim_products 
RENAME COLUMN removed TO still_available;

--The following gets rid of the '£' symbol so it can be changed to a numeric datatype
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')
WHERE product_price LIKE '£%';

--The following stipulates to data types of all the variables
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::double precision;

ALTER TABLE dim_products
ALTER COLUMN weight TYPE FLOAT;

ALTER TABLE dim_products
ALTER COLUMN "EAN" TYPE VARCHAR(50);

ALTER TABLE dim_products
ALTER COLUMN product_code TYPE VARCHAR(50);

ALTER TABLE dim_products
ALTER COLUMN date_added TYPE DATE USING date_added::date;

ALTER TABLE dim_products
ALTER COLUMN uuid TYPE UUID USING uuid::uuid;

ALTER TABLE dim_products
ALTER COLUMN still_available TYPE BOOL USING 
	CASE 
		WHEN still_available LIKE 'Still_available' THEN true
		ELSE false
	END