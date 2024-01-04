import pyodbc

class SqlDataFetcher:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None

    def connect(self):
        # Connect to the SQL Server database
        self.conn = pyodbc.connect(self.connection_string)

    def disconnect(self):
        # Close the database connection
        if self.conn:
            self.conn.close()

    def execute_sql_query(self, params, flag=0):
        if not self.conn:
            raise Exception("Database connection is not established. Call connect() method first.")

        # Create a cursor
        cursor = self.conn.cursor()

        try:
            print(params)
            # Define your SQL query


            query = f"""
                    SELECT *
                    FROM {params['object_name']}
                    WHERE
                    {'Year_p >= ' + f"'{params['start_year_param']}' AND " if params['start_year_param'] != 'Year=*' else ''}
                    {'Year_p <= ' + f"'{params['end_year_param']}' AND " if params['end_year_param'] != 'Year=*' else ''}
                    {'Month_p >= ' + f"'{params['start_month_param']}' AND " if params['start_month_param'] != 'Month=*' else ''}
                    {'Month_p <= ' + f"'{params['end_month_param']}' AND " if params['end_month_param'] != 'Month=*' else ''}
                    AccountID_p = '{params['account_id_param']}'
                    ORDER BY AccountId_p
                    OFFSET {params['offset_param']} ROWS FETCH NEXT {params['fetch_next_param']} ROWS ONLY;
                """

            print(query)

 

            # Execute the query with parameters
            
            cursor.execute(query)

            # Fetch the results
            data = cursor.fetchall()
            print(data)

            # Check the flag and return data or error message based on the flag value
            if flag == 1:
                return bool(data)  # Return True if data is not empty, False otherwise
            else:
                return data

        except Exception as e:
            # Handle exceptions and return error message
            error_message = f"Error executing SQL query: {str(e)}"
            if flag == 1:
                return error_message
            else:
                raise Exception(error_message)

        finally:
            # Close the cursor
            cursor.close()

class QueryParameters:
    def __init__(self, account_id, object_name, date_start_monthyear, date_end_monthyear, page_number, page_size):
        self.account_id = account_id
        self.object_name = object_name
        self.date_start_monthyear = date_start_monthyear
        self.date_end_monthyear = date_end_monthyear
        self.page_number = page_number
        self.page_size = page_size

    def transform(self):
        start_year_param = f'Year={self.extract_year(self.date_start_monthyear)}' if self.date_start_monthyear != "*" else "Year=*"
        end_year_param = f'Year={self.extract_year(self.date_end_monthyear)}' if self.date_end_monthyear != "*" else "Year=*"
        start_month_param = f'Month={self.extract_month(self.date_start_monthyear)}' if self.date_start_monthyear != "*" else "Month=*"
        end_month_param = f'Month={self.extract_month(self.date_end_monthyear)}' if self.date_end_monthyear != "*" else "Month=*"

        output_params = {
            'account_id_param': f'AccountId={self.account_id}',
            'object_name': f'{self.object_name}',
            'start_year_param': start_year_param,
            'end_year_param': end_year_param,
            'start_month_param': start_month_param,
            'end_month_param': end_month_param,
            'offset_param': self.page_number,
            'fetch_next_param': self.page_size
        }
        return output_params

    @staticmethod
    def extract_year(date):
        return date.split('/')[1].zfill(4) if date != "*" else "*"

    @staticmethod
    def extract_month(date):
        return date.split('/')[0].zfill(2) if date != "*" else "*"


# Example usage
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "Server=tcp:synw-smb-sfda-dev-ondemand.sql.azuresynapse.net,1433;"
    "DATABASE=smb-dev-sfda-synw-sqldb;"
    "UID=funcuser;"
    "PWD=Smuser@098!!!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Create SqlDataFetcher instance
sql_data_fetcher = SqlDataFetcher(connection_string)

query_params = QueryParameters(
    account_id="0017X00001571soQAA",
    object_name="Service_Work_Order__c",
    date_start_monthyear="1/2024",
    date_end_monthyear="12/2025",
    page_number=0,
    page_size=2
)
query_params_data = query_params.transform()

# Connect to the database
sql_data_fetcher.connect()

# Define your parameters
params = query_params_data

# Execute the SQL query with the flag set to 1
result = sql_data_fetcher.execute_sql_query(params, flag=0)

# Disconnect from the database
sql_data_fetcher.disconnect()

# Handle the result based on the flag value
if result is True:
    print("Query executed successfully. Data found.")
elif result is False:
    print("Query executed successfully. No data found.")
else:
    print(f"{result}")
