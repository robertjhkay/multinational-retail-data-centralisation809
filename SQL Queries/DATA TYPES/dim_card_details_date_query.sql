SELECT *
FROM dim_card_details
WHERE NOT (date_payment_confirmed ~ '^\d{4}-\d{2}-\d{2}$' AND date_payment_confirmed::date IS NOT NULL)