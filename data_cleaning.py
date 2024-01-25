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
            exclusion_list = ['752', '867', '1023', '1047', '1807', '2103', '2439', '6526', '2764', '2997', '3539', '4987', '5309', '5310', '6426', '6927', '7747', '8398', '9026', '10025', '10224', '10237', '10373', '11002', '11381', '11459', '11615', '11778', '11881', '12110', '12197', '12606', '13135', '13879', '14124', '14523']
            corrupt_data_index = user_data_frame['index'].astype(str).str.strip().isin(exclusion_list)
            user_data_frame = user_data_frame[~corrupt_data_index] #gets rid of 36 corrupt rows
            user_data_frame.replace({'date_of_birth':["1968 October 16", "January 1951 27", "November 1958 11", "1946 October 18", "1979 February 01", "June 1943 28", "November 1963 06", "February 2005 05", "July 1966 08", "1948 October 24", "December 1946 09", "2005 January 27", "July 1961 14", "July 1939 16", "1951 January 14", "May 1996 25"]}, {'date_of_birth':['1968-10-16', '1951-01-27', '1958-11-11', '1946-10-18', '1979-02-01', '1943-06-28', '1963-11-06', '2005-02-05', '1966-07-08', '1948-10-24', '1946-12-09', '2005-01-27', '1961-07-14', '1939-07-16', '1951-01-14','1996-05-25']}, inplace=True) # anomalies found in SQL which prevented changing data type to date
            user_data_frame['date_of_birth'] = user_data_frame['date_of_birth'].str.replace('/', '-') # another date anomaly
            user_data_frame['join_date'] = user_data_frame['join_date'].str.replace('/', '-')
            user_data_frame.replace({'join_date':["2006 September 03", "2001 October 14", "1998 June 28", "2022 October 04", "2008 December 05", "1994 February 12", "November 1994 28", "February 2019 03", "July 2002 21", "May 1999 31", "May 1994 27", "March 2011 04", "December 1992 09", "October 2022 26"]}, {'join_date':['2006-09-03', '2001-10-14', '1998-06-28', '2022-10-04', '2008-12-05', '1994-02-12', '1994-11-28', '2019-02-03', '2002-07-21', '1999-05-31', '1994-05-27', '2011-03-04', '1992-12-09', '2022-10-26']}, inplace=True)
            user_data_frame['country_code'] = user_data_frame['country_code'].str.replace('GGB', 'GB') # corrects country code for 6 cases
            return user_data_frame
    
        '''
        Method cleans card data by getting rid of NULL values and rows with corrupt data.
        '''

        def clean_card_data(self):
            card_data_frame = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
            card_data_frame.replace({'card_number': ['NULL']}, {'card_number': [np.nan]}, inplace=True) # pdf has 'NULL' instead of blank spaces
            card_data_frame.replace({'expiry_date': ['NULL']}, {'expiry_date': [np.nan]}, inplace=True)
            card_data_frame = card_data_frame.dropna(subset=['card_number', 'expiry_date']) # drops rows without a card number
            corrupt_card_numbers = ["VAB9DSB8ZM", "MOZOT5Q95V", "K0084A9R99", "Y8ITI33X30", "RNSCD8OCIM", "MIK9G2EMM0", "I4PWLWSIRJ", "OMZSBN2XG3", "NB8JJ05D7R", "G0EF4TS8C8", "Z8855EXTJX", "JQTLQAAQTD", "T23BTBBJDD", "LSWT9DT4G4"]
            corrupt_data_index = card_data_frame['card_number'].isin(corrupt_card_numbers)
            card_data_frame = card_data_frame[~corrupt_data_index] # gets rid of 14 corrupt rows
            card_data_frame.replace({'date_payment_confirmed': ["December 2021 17", "2005 July 01", "December 2000 01", "2008 May 11", "October 2000 04", "September 2016 04", "2017/05/15", "May 1998 09"]}, {'date_payment_confirmed':['2021-12-17', '2005-07-01', '2000-12-01', '2008-05-11', '2000-10-04', '2016-09-04', '2017-05-15', '1998-05-09']}, inplace=True)
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
                    staff_numbers = float(staff_numbers)
                    if staff_numbers >= 0:
                        return staff_numbers
                    else:
                        return None
                except ValueError:
                    return None
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

        def find_cleaned_missing_card_numbers():
            orders_table = DataCleaning().clean_orders_data()
            card_details_pdf = DataCleaning().clean_card_data()
            # Extract the 'card_number' columns from both DataFrames
            orders_card_numbers = orders_table['card_number']
            pdf_card_numbers = card_details_pdf['card_number']
            # Find the missing card numbers
            missing_card_numbers = orders_card_numbers[~orders_card_numbers.isin(pdf_card_numbers)]
            return missing_card_numbers

missing_card_numbers = find_cleaned_missing_card_numbers()
print("Missing Card Numbers:")
print(missing_card_numbers)