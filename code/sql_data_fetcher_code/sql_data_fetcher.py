import pyodbc

class SqlDataFetcher:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None


    def fetch_data(self, query_params, flag=0):
        self.validate_input(query_params)

        data = None  # Initialize data variable
        error_message = None  # Variable to store the error message

        try:
            # Establish the connection
            self.conn = pyodbc.connect(self.connection_string)
            cursor = self.conn.cursor()

            # Your SQL query to select data with specified conditions from query_params
            select_query = f"SELECT * FROM {query_params.object_name} WHERE " \
                           f"(Year_p >= 'Year={query_params.date_start_monthyear}' AND " \
                           f"Year_p <= 'Year={query_params.date_end_monthyear}') AND " \
                           f"(AccountID_p = 'AccountId={query_params.account_id}') " \
                           f"ORDER BY AccountId_p " \
                           f"OFFSET {query_params.page_number * query_params.page_size} ROWS " \
                           f"FETCH NEXT {query_params.page_size} ROWS ONLY;"

            # Execute the query to select data
            cursor.execute(select_query)

            # Fetch the results
            data = cursor.fetchall()

        except pyodbc.Error as e:
            # Log the error details for debugging
            error_message = f"PyODBC Error: {e}"
            print(error_message)  # You can replace this with a logging mechanism if available
            raise  # Re-raise the exception for higher-level error handling

        except Exception as ex:
            # Log other unexpected exceptions
            error_message = f"Unexpected Error: {ex}"
            print(error_message)  # You can replace this with a logging mechanism if available
            raise  # Re-raise the exception for higher-level error handling

        finally:
            # Close the connection if it's open
            if self.conn:
                self.conn.close()

        # Check the flag and return data or error message based on the flag value
        if flag == 1:
            if error_message:
                return error_message
            elif data:
                return True
            else:
                return False
        else:
            return data

# Assuming you have a QueryParameters class defined somewhere in your code
class QueryParameters:
    def __init__(self, account_id, object_name, date_start_monthyear, date_end_monthyear, page_number, page_size):
        self.account_id = account_id
        self.object_name = object_name
        self.date_start_monthyear = date_start_monthyear
        self.date_end_monthyear = date_end_monthyear
        self.page_number = page_number
        self.page_size = page_size

# Example Usage:
# Define the connection string
# connection_string = (
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     "Server=tcp:synw-smb-sfda-dev-ondemand.sql.azuresynapse.net,1433;"
#     "DATABASE=smb-dev-sfda-synw-sqldb;"
#     "UID=funcuser;"
#     "PWD=Smuser@098!!!;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )

# # Create an instance of the SqlDataFetcher class
# data_fetcher = SqlDataFetcher(connection_string)

# # Create an instance of the QueryParameters class
# query_params = QueryParameters(
#     account_id="0017X00001571soQAA",
#     object_name="Payment",
#     date_start_monthyear="2023",
#     date_end_monthyear="2025",
#     page_number=0,
#     page_size=10
# )

# try:
#     # Fetch data using the QueryParameters object and set flag to 1
#     data_result = data_fetcher.fetch_data(query_params, flag=1)

#     # Print or use data_result as needed
#     print(data_result)

# except ValueError as ve:
#     # Handle the exception, print or log the error message
#     print(ve)
# except pyodbc.Error as e:
#     # Handle other pyodbc errors
#     print(f"PyODBC Error: {e}")
# except Exception as ex:
#     # Handle any other unexpected exceptions
#     print(f"Unexpected Error: {ex}")
