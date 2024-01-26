from data_extraction import DataExtractor
from data_cleaning import DataCleaning

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
    
    def find_clean_missing_card_numbers():
        orders_table = DataCleaning().clean_orders_data()
        card_details_pdf = DataCleaning().clean_card_data()
        # Extract the 'card_number' columns from both DataFrames
        orders_card_numbers = orders_table['card_number']
        pdf_card_numbers = card_details_pdf['card_number']
        # Find the missing card numbers
        missing_card_numbers = orders_card_numbers[~orders_card_numbers.isin(pdf_card_numbers)]
        return missing_card_numbers

missing_card_numbers = find_missing_card_numbers()
print("Missing Card Numbers:")
print(missing_card_numbers)