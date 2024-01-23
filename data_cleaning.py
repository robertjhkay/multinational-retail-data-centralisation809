from data_extraction import DataExtractor
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
            return user_data_frame
    
        '''
        Method cleans card data by getting rid of NULL values and rows with corrupt data.
        '''

        def clean_card_data(self):
            card_data_frame = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
            card_data_frame = card_data_frame.dropna(how='any',axis=0) #drops null values
            corrupt_card_numbers = ["VAB9DSB8ZM", "MOZOT5Q95V", "K0084A9R99", "Y8ITI33X30", "RNSCD8OCIM", "MIK9G2EMM0", "I4PWLWSIRJ", "OMZSBN2XG3", "NB8JJ05D7R", "G0EF4TS8C8", "Z8855EXTJX", "JQTLQAAQTD", "T23BTBBJDD", "LSWT9DT4G4"]
            corrupt_data_index = card_data_frame['card_number'].isin(corrupt_card_numbers)
            card_data_frame = card_data_frame[~corrupt_data_index] #gets rid of 14 corrupt rows
            return card_data_frame
        
        '''
        Method cleans store data by getting rid of 'lat' column and rows with a correct country code.
        '''
        
        def called_clean_store_data(self):
            store_data_frame = DataExtractor().retrieve_stores_data()
            store_data_frame = store_data_frame.drop('lat', axis=1)
            country_code_allowed = ['US', 'GB', 'DE']
            country_code_index = store_data_frame['country_code'].isin(country_code_allowed)
            store_data_frame = store_data_frame[country_code_index]
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
            df['weight'] = df['weight'].apply(weight_converter)
            filtered_df = df.dropna(subset=['weight'])
            return filtered_df
        
        '''
        Method cleans the product data. Utilizes method above.
        ''' 

        def clean_products_data(self):
            products_dataframe = self.convert_product_weights()
            drop_prod_list=['S1YB74MLMJ','C3NCA2CL35', 'WVPMHZP59U'] # list of strings to drop rows for in the next line
            corrupt_data_index = products_dataframe['category'].isin(drop_prod_list)
            products_dataframe = products_dataframe[~corrupt_data_index] # drop the rows where the category column has entries equal to thouse in the list above
            products_dataframe.drop(products_dataframe[products_dataframe['category'].isin(drop_prod_list)].index, inplace=True) 
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

if __name__ == '__main__':
    print(DataCleaning().convert_product_weights().axes)
