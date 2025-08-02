import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        user='maxsilver9890',
        password='wT8kiuNbHtUTBNf',
        account='PFOBQAM-IW03734',
        warehouse='COMPUTE_WH',
        database='MOVIELENS',
        schema='DEV'
    )
