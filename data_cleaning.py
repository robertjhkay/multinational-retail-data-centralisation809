from data_extraction import DataExtractor
import numpy as np
import pandas as pd
import re

'''
This class has methods to clean data from each of the data sources.

'''

class DataCleaning:

        def __init__(self):
            self

        '''
        Method cleans user data by getting rid of NULL values, errors with dates and rows with incorrect information.
        '''

        def clean_user_data(self): 
            user_data_frame = DataExtractor().read_rds_table('legacy_users')
            user_data_frame.dropna(subset=['date_of_birth','join_date'], inplace=True)

            def move_digits_to_front(input_string): # Converts 12-2005-21 to '2005-12 21'
                match = re.search(r'\d{4}', input_string)
                if match:
                    digits = match.group()
                    result_string = digits + ' ' + input_string.replace(digits, '', 1)
                    result_string = result_string.replace('  ', ' ')
                    result_string = result_string.replace(' -', ' ')
                    result_string = result_string.replace('--', '-')
                else:
                    result_string = input_string
                return result_string
                

            
            user_data_frame.loc[:, 'date_of_birth'] = user_data_frame['date_of_birth'].apply(move_digits_to_front)
            user_data_frame.loc[:, 'join_date'] = user_data_frame['join_date'].apply(move_digits_to_front)

            def replace_month_names(date_string): # Converts December to 12
                month_dict = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                    }
                for month_name, month_number in month_dict.items():
                    date_string = date_string.replace(month_name, month_number)
                return date_string

            user_data_frame.loc[:, 'date_of_birth'] = user_data_frame['date_of_birth'].apply(replace_month_names)
            user_data_frame.loc[:, 'join_date'] = user_data_frame['join_date'].apply(replace_month_names)
            user_data_frame['date_of_birth'] = [date.replace('/', '-') for date in user_data_frame['date_of_birth']]
            user_data_frame['join_date'] = [date.replace('/', '-') for date in user_data_frame['join_date']]
            user_data_frame['date_of_birth'] = [date.replace(' ', '-') for date in user_data_frame['date_of_birth']]
            user_data_frame['join_date'] = [date.replace(' ', '-') for date in user_data_frame['join_date']]

            user_data_frame['country_code'] = user_data_frame['country_code'].str.replace('GGB', 'GB') # corrects country code for 6 cases
            country_code_allowed = ['US', 'GB', 'DE']
            country_code_index = user_data_frame['country_code'].isin(country_code_allowed)
            user_data_frame = user_data_frame[country_code_index]
            return user_data_frame
    
        '''
        Method cleans card data by getting rid of NULL values and rows with corrupt data.
        '''

        def clean_card_data(self):
            card_data_frame = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
            
            card_data_frame.replace({'card_number': ['NULL']}, {'card_number': [np.nan]}, inplace=True) # pdf has 'NULL' instead of blank spaces

            def question_mark_deletion(card_number):
                try:
                    card_number = str(card_number)
                    card_number = card_number.replace("?", '')
                except:
                    card_number = np.nan
                return card_number

            card_data_frame.loc[:, 'card_number'] = card_data_frame['card_number'].apply(question_mark_deletion)
            
            def corrupt_number(card_number):
                try:
                    card_number = int(card_number)
                except ValueError:
                    card_number = np.nan
                return card_number
            
            card_data_frame.loc[:, 'card_number'] = card_data_frame['card_number'].apply(corrupt_number) # sets card numbers to Null if they are a string
            card_data_frame.replace({'expiry_date': ['NULL']}, {'expiry_date': [np.nan]}, inplace=True)
            card_data_frame = card_data_frame.dropna(subset=['card_number', 'expiry_date']) # drops rows without a card number or expiry date

            def move_digits_to_front(input_string): # Converts 12-2005-21 to '2005-12 21'
                match = re.search(r'\d{4}', input_string)
                digits = match.group()
                result_string = digits + ' ' + input_string.replace(digits, '', 1)
                result_string = result_string.replace('  ', ' ')
                result_string = result_string.replace(' -', '-')
                result_string = result_string.replace('--', '-')
                return result_string
           
            card_data_frame.loc[:, 'date_payment_confirmed'] = card_data_frame['date_payment_confirmed'].apply(move_digits_to_front)
            
            def replace_month_names(date_string): # Converts December to 12
                month_dict = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                    }
                for month_name, month_number in month_dict.items():
                    date_string = date_string.replace(month_name, month_number)
                return date_string
            
            card_data_frame.loc[:, 'date_payment_confirmed'] = card_data_frame['date_payment_confirmed'].apply(replace_month_names)
            card_data_frame['date_payment_confirmed'] = [date.replace('/', '-') for date in card_data_frame['date_payment_confirmed']]
            card_data_frame['date_payment_confirmed'] = [date.replace(' ', '-') for date in card_data_frame['date_payment_confirmed']]
            return card_data_frame
        
        '''
        Method cleans store data by getting rid of rows with an incorrect country code and ensuring staff numbers is a numeric field.
        '''
        
        def called_clean_store_data(self):
            store_data_frame = DataExtractor().retrieve_stores_data()
            # store_data_frame = store_data_frame.drop('lat', axis=1) this is now done with SQL later on
            store_data_frame['country_code'] = store_data_frame['country_code'].str.replace('GGB', 'GB')
            country_code_allowed = ['US', 'GB', 'DE']
            country_code_index = store_data_frame['country_code'].isin(country_code_allowed)
            store_data_frame = store_data_frame[country_code_index]
            
            def staff_int(staff_numbers):
                try:
                    staff_numbers = int(staff_numbers)
                except ValueError:
                    staff_numbers = np.nan
                return staff_numbers
            
            store_data_frame.loc[:, 'staff_numbers'] = store_data_frame['staff_numbers'].apply(staff_int)
            return store_data_frame

        '''
        Method converts weight data from a string to a float in kg.
        '''
        
        def convert_product_weights(self):
            df = DataExtractor().extract_from_s3()
            df.replace({'weight':['77g .']}, {'weight':['77g']}, inplace=True)
            df = df.dropna()
            
            def weight_converter(weight):
                try:
                    weight = float(weight)
                except ValueError:
                    weight = str(weight)
                    weight = weight.strip()
                    if re.search('kg', weight):
                        x = re.sub('kg', "", weight)
                        weight = float(x)  # strips 'kg' unit
                    elif re.search('x', weight):
                        weight = re.sub('x', '*', weight)
                        x = re.sub('g', "", weight)
                        weight = eval(x) / 1000  # gives total weight of multipacks
                    elif re.search('g', weight):
                        x = re.sub('g', "", weight)
                        weight = float(x) / 1000  # converts g into kg
                    elif re.search('ml', weight):
                        x = re.sub('ml', "", weight)
                        weight = float(x) / 1000  # converts ml into kg
                    elif re.search('oz', weight):
                        x = re.sub('oz', "", weight)
                        weight = float(x) * 0.0283495  # converts 'oz' into kg
                    else:
                        return None
                return weight
            
            df.loc[:, 'weight'] = df['weight'].apply(weight_converter) # .loc prevents SettingWithCopyWarning
            filtered_df = df.dropna(subset=['weight'])
            return filtered_df
        
        '''
        Method cleans the product data. Utilizes method above.
        ''' 

        def clean_products_data(self):
            products_dataframe = self.convert_product_weights()
            product_categories=["diy", "health-and-beauty", "pets", "food-and-drink", "sports-and-leisure", "toys-and-games", "homeware"] # list of product categories sold by the store
            category_data_index = products_dataframe['category'].isin(product_categories)
            products_dataframe = products_dataframe[category_data_index] # only products in defined categories are selected 
            return products_dataframe
        
        
        
        '''
        Method cleans the order data.
        ''' 

        def clean_orders_data(self):
            orders_dataframe = DataExtractor().read_rds_table('orders_table') # reads orders table from AWS RDS database extracted in the dataextractor class
            orders_dataframe.drop(columns=['1', 'first_name', 'last_name', 'level_0'], inplace=True) # drops rows where the entries are '1', 'first_name' and 'last_name'
            return  orders_dataframe
        
        '''
        Method cleans the transaction data.
        ''' 
    
        def clean_date_times(self):
            date_time_dataframe = DataExtractor().extract_from_s3_json()
            date_time_dataframe['day'] = pd.to_numeric(date_time_dataframe['day'], errors='coerce')
            date_time_dataframe.dropna(subset=['day', 'year', 'month'], inplace=True) # drops rows which contain null values in the specified columns
            date_time_dataframe['timestamp'] = pd.to_datetime(date_time_dataframe['timestamp'], format='%H:%M:%S', errors='coerce') # timestamp in form hour minute and seconds
            return date_time_dataframe