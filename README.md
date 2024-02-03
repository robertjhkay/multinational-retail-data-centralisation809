# Multinational-Retail-Data-Centralisation

A multinational company that sells various goods across the globe. Their sales data is spread across many different data sources, making it not easily accessible or analyzable by current members of the team. This project enables the multinational to make its sales data accessible from one centralized location.

## Milestone 1: Set up the environment

- Set up a repository on GitHub to track changes to code and save them online.

## Milestone 2: Extract and clean the data from the data sources

- Set up a new database within pgAdmin4 named `sales_data`.
- Define scripts and classes to extract and clean the data from multiple data sources. Defining classes allows functions to be executed one stage at a time and also makes the code more navigable.
- Extract data of users stored in an AWS database. This requires importing a YAML file containing the necessary login details.
- Extract user card details stored in a PDF document in an AWS S3 bucket. Note that issues arose because Java was not an environmental variable. Please read installation instructions carefully to avoid similar difficulties.
- Extract store data through the use of an API.
- Retrieve and clean the orders table. This is another table within the AWS database for which a connection was already established.
- Retrieve and clean the date events data.

## Milestone 3: Create the Database Schema using SQL

Develop the star-based schema of the database. This includes creating primary keys in the tables prefixed with `dim` and foreign keys in the `orders_table` to reference the primary keys in the other tables.

## Milestone 4: Answer Business Related Questions using SQL

This was done within PgAdmin. After each question, a table of results was shown, and the subsequent code provides similar figures. Due to differing philosophies on data cleaning, there are more stores in the `dim_store_details` table. The one notable difference is 'Task 9,' which asks for the average time between each sale. The issue arises from going from one business day to another. As the operation spans two continents, the business could be considered a 24-hour affair. My assumptions for this calculation are that:

- Time between business days should count.
- Where there are global holidays (e.g., Christmas), the time should not factor into the calculation.
- In every business day, there is at least one sale.

## Installation Instructions

Before proceeding, ensure that `JAVA_HOME` is an environmental variable in the operating system. If not, uninstall Java if necessary, and install it by downloading the relevant package from the [Corretto website](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/downloads-list.html).

Then ensure the following is installed within your Python environment:

- `pip install pandas`
- `pip install pyyaml`
- `pip install tabula-py` (which has the following [documentation](https://pypi.org/project/tabula-py/))

NOTE: YAML is used to load credential details to connect to the AWS bucket. The file itself is excluded from the repository.

Once the data is downloaded and cleaned, it is analyzed within an SQL platform. Therefore, PostgreSQL and pgAdmin must be installed ahead of time.

## Usage instructions

## File structure of the project

The following files cover what was accomplished in Milestone 2:

- `data_cleaning.py`
- `data_extraction.py`
- `database_utils.py`

For Milestones 3 & 4, please go to the SQL Folder.

## License information

Copyright (c) 2024 Robert Kay

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.