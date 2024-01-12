import pyodbc
import json
from datetime import datetime
import logging
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
class SqlDataFetcher:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.logger = logging.getLogger(__name__)

    def execute_sql_query(self, params, flag=0):
        with pyodbc.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                try:
                    count_query = self._build_count_query(params)
                    self.logger.debug(count_query)
                    cursor.execute(count_query)
                    count_result = cursor.fetchone()[0]

                    # Check if count_result is 0
                    if count_result == 0:
                        self.logger.warning("No data found. Returning False.")
                        return False, count_result
                    elif count_result>0 and flag==1:
                        return True, count_result

                    data_query = self._build_data_query(params)
                    self.logger.debug(data_query)
                    cursor.execute(data_query)
                    rows = cursor.fetchall()

                    if not rows:
                        return False, count_result

                    data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
                    json_data = json.dumps(data, cls=CustomEncoder)

                    return (json_data, count_result) if flag == 0 else (True, count_result)

                except pyodbc.Error as e:
                    self.logger.error(f"Error executing SQL query: {e}")
                    raise

    def _build_count_query(self, params):
        return f"""
            SET ANSI_WARNINGS OFF;
            SELECT COUNT(*)
            FROM {params['object_name']}
            WHERE
            {'Year_p >= ' + f"'{params['start_year_param']}' AND " if params['start_year_param'] != 'Year=*' else ''}
            {'Year_p <= ' + f"'{params['end_year_param']}' AND " if params['end_year_param'] != 'Year=*' else ''}
            {'Month_p >= ' + f"'{params['start_month_param']}' AND " if params['start_month_param'] != 'Month=*' else ''}
            {'Month_p <= ' + f"'{params['end_month_param']}' AND " if params['end_month_param'] != 'Month=*' else ''}
            {'Day_p >= ' + f"'{params['start_day_param']}' AND " if params['start_day_param'] != 'Day=*' else ''}
            {'Day_p <= ' + f"'{params['end_day_param']}' AND " if params['end_day_param'] != 'Day=*' else ''}
            AccountId = '{params['account_id_param']}';
            SET ANSI_WARNINGS ON;
        """

    def _build_data_query(self, params):
        return f"""
            SET ANSI_WARNINGS OFF; 
            SELECT *
            FROM {params['object_name']}
            WHERE
            {'Year_p >= ' + f"'{params['start_year_param']}' AND " if params['start_year_param'] != 'Year=*' else ''}
            {'Year_p <= ' + f"'{params['end_year_param']}' AND " if params['end_year_param'] != 'Year=*' else ''}
            {'Month_p >= ' + f"'{params['start_month_param']}' AND " if params['start_month_param'] != 'Month=*' else ''}
            {'Month_p <= ' + f"'{params['end_month_param']}' AND " if params['end_month_param'] != 'Month=*' else ''}
            {'Day_p >= ' + f"'{params['start_day_param']}' AND " if params['start_day_param'] != 'Day=*' else ''}
            {'Day_p <= ' + f"'{params['end_day_param']}' AND " if params['end_day_param'] != 'Day=*' else ''}
            AccountId = '{params['account_id_param']}'
            ORDER BY AccountId
            OFFSET {params['offset_param']} ROWS FETCH NEXT {params['fetch_next_param']} ROWS ONLY;
            -- Set ANSI_WARNINGS back ON for other queries 
            SET ANSI_WARNINGS ON; 
        """

class QueryParameters:
    def __init__(self, account_id, object_name, date_start_daymonthyear, date_end_daymonthyear, page_number, page_size):
        self.account_id = account_id
        self.object_name = object_name
        self.date_start_daymonthyear = date_start_daymonthyear
        self.date_end_daymonthyear = date_end_daymonthyear
        self.page_number = page_number
        self.page_size = page_size

    def transform(self):
        start_year_param = f'Year={self.extract_year(self.date_start_daymonthyear)}' if self.date_start_daymonthyear != "*" else "Year=*"
        end_year_param = f'Year={self.extract_year(self.date_end_daymonthyear)}' if self.date_end_daymonthyear != "*" else "Year=*"
        start_month_param = f'Month={self.extract_month(self.date_start_daymonthyear)}' if self.date_start_daymonthyear != "*" else "Month=*"
        end_month_param = f'Month={self.extract_month(self.date_end_daymonthyear)}' if self.date_end_daymonthyear != "*" else "Month=*"
        start_day_param = f'Day={self.extract_day(self.date_start_daymonthyear)}' if self.date_start_daymonthyear != "*" else "Day=*"
        end_day_param = f'Day={self.extract_day(self.date_end_daymonthyear)}' if self.date_end_daymonthyear != "*" else "Day=*"
        
        output_params = {
            'account_id_param': f'{self.account_id}',
            'object_name': f'{self.object_name}',
            'start_year_param': start_year_param,
            'end_year_param': end_year_param,
            'start_month_param': start_month_param,
            'end_month_param': end_month_param,
            'start_day_param': start_day_param,
            'end_day_param' : end_day_param,
            'offset_param': self.page_number,
            'fetch_next_param': self.page_size
        }
        print(output_params)
        return output_params

    @staticmethod
    def extract_year(date):
        return date.split('-')[0].zfill(4) if date != "*" else "*"

    @staticmethod
    def extract_month(date):
        return date.split('-')[1].zfill(2) if date != "*" else "*"
    
    @staticmethod
    def extract_day(date):
        return date.split('-')[2].zfill(2) if date != "*" else "*"

# # Example usage
# connection_string = (
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     "Server=tcp:synw-smb-sfda-dev-ondemand.sql.azuresynapse.net,1433;"
#     "DATABASE=smbuat;"
#     "UID=funcuser;"
#     "PWD=Smuser@098!!!;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )
# logging.basicConfig(level=logging.DEBUG)
# # Create SqlDataFetcher instance
# sql_data_fetcher = SqlDataFetcher(connection_string)

# query_params = QueryParameters(
#     account_id="0013000001Gu6vIAAR",
#     object_name="Service_Work_Order__c",
#     date_start_daymonthyear="1/1/2014",
#     date_end_daymonthyear="30/12/2025",
#     page_number=0,
#     page_size=2
# )
# query_params_data = query_params.transform()

# # Define your parameters
# json_data, flag, count = sql_data_fetcher.execute_sql_query(query_params_data, flag=0)

# # Handle the result based on the flag value
# if flag is True:
#     print("Query executed successfully. Data found.", f"The count would be {count}")
# elif flag is False:
#     print("Query executed successfully. No data found.", f"The count would be {count}")
# else:
#     print(f"{json_data}\n", f"The count would be {count}")
