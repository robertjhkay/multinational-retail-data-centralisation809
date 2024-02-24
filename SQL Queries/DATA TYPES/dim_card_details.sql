ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(20) USING card_number::VARCHAR(20);

ALTER TABLE dim_card_details
ALTER COLUMN expiry_date TYPE VARCHAR(5) USING expiry_date::VARCHAR(5);

ALTER TABLE dim_card_details
ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE