# Multinational-Retail-Data-Centralisation

A multinational company that sells various goods across the globe. Their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. This project enables the multinational to make its sales data accessible from one centralised location.

## Milestone 1: Set up the environment

- Set up a repository in GitHub to track changes to code and save them online.

## Milestone 2: Extract and clean the data from the data sources

- Set up a new database within pgadmin4 named sales_data.
- Definie scripts and classes to extract and clean the data from multiple data sources.
- Extract data of users stored in an AWS database.
- Extract user card details stored in a PDF document in an AWS S3 bucket.
- Extract store data through the use of an API.
- Retrive and clean the orders table.
- Retrive and clean the date events data.

## Milestone 3: Create the Database Schema

- Develop the star-based schema of the database. This includes primary keys created in the tables prefixed with dim and foreign keys in the orders_table to reference the primary keys in the other tables.

