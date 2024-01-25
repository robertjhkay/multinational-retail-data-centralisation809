SELECT *
FROM dim_users
WHERE NOT (date_of_birth ~ '^\d{4}-\d{2}-\d{2}$' AND date_of_birth::date IS NOT NULL)