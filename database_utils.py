import yaml
import sqlalchemy

'''
This class connects and uploads data to the sales_data database.

'''

class DatabaseConnector:

        def __init__(self):
            self

        '''
        The following method ensures the login credentials are read in the yaml file.
        '''
        def read_db_creds(self):
            with open('db_creds.yaml', 'r') as file:
                creds = yaml.safe_load(file)
            return creds

        '''
        The following method will use the credentials to connect to the database.
        '''
        def init_db_engine(self):
            creds = self.read_db_creds()
            database_type = 'postgresql'
            host = creds['RDS_HOST']
            username = creds['RDS_USER']
            password = creds['RDS_PASSWORD']
            database = creds['RDS_DATABASE']
            port = creds['RDS_PORT']
            db_conn_url = f"{database_type}://{username}:{password}@{host}:{port}/{database}"
            engine = sqlalchemy.create_engine(db_conn_url)
            return engine

        '''
        The following method lists all the tables in the database so you know which tables you can extract data from.
        '''
        def list_db_tables(self):
            engine = self.init_db_engine()
            with engine.connect() as connection:
                metadata = sqlalchemy.MetaData()
                metadata.reflect(bind=connection)
            table_names = metadata.tables.keys()

            return table_names
        
        '''
        The following method uploads the database to a local machine.
        '''
        
        def upload_to_db(self, df, table_name):

            DATABASE_TYPE = 'postgresql'
            DBAPI = 'psycopg2'
            HOST = 'localhost'
            USER = 'postgres'
            PASSWORD = 'hello'
            DATABASE = 'sales_data'
            PORT = 5432
            local_engine = sqlalchemy.create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
            df.to_sql(table_name, local_engine, if_exists='replace')

   
if __name__ == '__main__':
    print('Tables in Database:', DatabaseConnector().list_db_tables())
    from data_cleaning import DataCleaning
    #DatabaseConnector().upload_to_db(DataCleaning().clean_user_data(),'dim_users')
    DatabaseConnector().upload_to_db(DataCleaning().clean_card_data(),'dim_card_details')
    #DatabaseConnector().upload_to_db(DataCleaning().called_clean_store_data(),'dim_store_details')
    #DatabaseConnector().upload_to_db(DataCleaning().clean_products_data(),'dim_products')
    #DatabaseConnector().upload_to_db(DataCleaning().clean_orders_data(),'orders_table')
    #DatabaseConnector().upload_to_db(DataCleaning().clean_date_times(),'dim_date_times')