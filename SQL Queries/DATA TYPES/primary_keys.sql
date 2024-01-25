ALTER TABLE dim_card_details
ADD CONSTRAINT PK_dim_card_details_card_number PRIMARY KEY (card_number);

ALTER TABLE dim_date_times
ADD CONSTRAINT PK_dim_date_times_date_uuid PRIMARY KEY (date_uuid);

ALTER TABLE dim_store_details
ADD CONSTRAINT PK_dim_store_details_store_code PRIMARY KEY (store_code);

ALTER TABLE dim_products
ADD CONSTRAINT PK_dim_products_product_code PRIMARY KEY (product_code);

ALTER TABLE dim_users
ADD CONSTRAINT PK_dim_users_user_uuid PRIMARY KEY (user_uuid)