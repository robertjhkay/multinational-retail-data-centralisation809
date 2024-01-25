from database_utils import DatabaseConnector
import pandas as pd
import tabula
import requests #pip install requests

'''
This class has methods that help extract data from different sources which include CSV files, an API and an S3 bucket.

'''

class DataExtractor:

        def __init__(self):
            self.db = DatabaseConnector()
            self.rds_database = self.db.init_db_engine()

        '''
        This method will extract the database table to a pandas DataFrame.
        '''
        def read_rds_table(self, table_name):
            return pd.read_sql_table(table_name, self.rds_database)
        
        '''
        This method will extract data from a pdf file.
        '''
        def retrieve_pdf_data(self, pdf_path):
            pdf_data = tabula.read_pdf(pdf_path, pages = 'all')
            return pd.concat(pdf_data)
        
        '''
        This method will tell us how many store there are from an API.
        '''
        def list_number_of_stores(self):
            KEY = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
            stores = requests.get('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', headers=KEY)
            number_of_stores = stores.json()
            return number_of_stores['number_stores']
        
        '''
        This method will extract all the stores from an API saving them in a pandas DataFrame.
        '''
        def retrieve_stores_data(self):
            KEY = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
            store_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details'
            number_of_stores = self.list_number_of_stores()
            store_data = []
            for store_number in range(0, number_of_stores):
                url = f'{store_url}/'+str(store_number)
                r = requests.get(url, headers=KEY)
                x = r.json()
                store_data.append(x)
            return pd.DataFrame(store_data)
        
        '''
        This method will extract a CSV file from a S3 bucket saving them in a pandas DataFrame.
        '''        
        def extract_from_s3(self):
            address = 's3://data-handling-public/products.csv'
            df = pd.read_csv(address)
            return df
    
        '''
        This method will extract a JSON file from a S3 bucket saving them in a pandas DataFrame.
        '''
        def extract_from_s3_json(self):
            address = 's3://data-handling-public/date_details.json'
            table = pd.read_json(address)
            return table
        
if __name__ == '__main__':
    
        def find_missing_card_numbers():
            orders_table = DataExtractor().read_rds_table('orders_table')
            card_details_pdf = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
            # Extract the 'card_number' columns from both DataFrames
            orders_card_numbers = orders_table['card_number']
            pdf_card_numbers = card_details_pdf['card_number']
            # Find the missing card numbers
            missing_card_numbers = orders_card_numbers[~orders_card_numbers.isin(pdf_card_numbers)]
            return missing_card_numbers

missing_card_numbers = find_missing_card_numbers()
print("Missing Card Numbers:")
print(missing_card_numbers)