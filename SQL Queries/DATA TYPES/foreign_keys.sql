ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times(date_uuid);

DELETE FROM orders_table
WHERE store_code NOT IN (SELECT store_code FROM dim_store_details);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_store_code
FOREIGN KEY (store_code)
REFERENCES dim_store_details(store_code);

DELETE FROM orders_table
WHERE product_code NOT IN (SELECT product_code FROM dim_products);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_product_code
FOREIGN KEY (product_code)
REFERENCES dim_products(product_code);

DELETE FROM orders_table
WHERE user_uuid NOT IN (SELECT user_uuid FROM dim_users);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_table_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users(user_uuid)
