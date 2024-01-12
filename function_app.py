# Import required modules
import azure.functions as func
import json
from validation import Validation
from sql_data_fetcher import SqlDataFetcher, QueryParameters
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

# Define the connection string
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "Server=tcp:synw-smb-sfda-dev-ondemand.sql.azuresynapse.net,1433;"
    "DATABASE=smbuat;"
    "UID=funcuser;"
    "PWD=Smuser@098!!!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)
# Create an instance of the SqlDataFetcher class
data_fetcher = SqlDataFetcher(connection_string)

# FunctionApp initialization without authentication
app = func.FunctionApp()

def log_error_and_return_response(error_message, status_code):
    logging.error(error_message)
    return func.HttpResponse(
        json.dumps({"message": error_message}),
        mimetype="application/json",
        status_code=status_code
    )

# HTTP trigger route
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Validate 'Account__c' parameter presence
        account_id = req.params.get('Account__c')
        if not account_id:
            return log_error_and_return_response("Account__c is required.", 400)

        # Get query parameters
        query_params = QueryParameters(
            account_id=account_id,
            object_name=req.params.get('object_name', None),
            date_start_daymonthyear=req.params.get('Date_Start_MonthYear', '*'),
            date_end_daymonthyear=req.params.get('Date_End_MonthYear', '*'),
            page_number=int(req.params.get('Page_Number', 0)),
            page_size=int(req.params.get('Page_Size', 10))
        )
        # Initialize Validation
        validator = Validation(query_params)

        # Handle Account ID Request if applicable
        if query_params.object_name is None or query_params.object_name.lower() == 'none':
            result, count_result = handle_account_id_request(query_params)

        # Handle Complex Request with validations
        else:
            validation_result = validate_query_params(validator)
            if validation_result is not None:
                # Log validation errors
                return log_error_and_return_response(f"Validation failed: {validation_result}", 400)
            result, count_result = execute_query(query_params)

        query_result = {
            "account_id": query_params.account_id,
            "object_name": query_params.object_name,
            "date_start_daymonthyear": query_params.date_start_daymonthyear,
            "date_end_daymonthyear": query_params.date_end_daymonthyear,
            "page_number": query_params.page_number,
            "page_size": query_params.page_size,
            "data": result,  # Add your actual query result here
            "count": count_result
        }

        # Log the final query result
        # logging.info(f"Final query result: {query_result}")

        return func.HttpResponse(json.dumps(query_result), mimetype="application/json", status_code=200)

    except ValueError as ve:
        # Log validation errors
        return log_error_and_return_response(f"Validation error: {ve}", 400)

    except Exception as e:
        # Log unexpected errors
        return log_error_and_return_response(f"An unexpected error occurred: {str(e)}", 500)


def handle_account_id_request(query_params):
    if query_params.object_name is None or query_params.object_name.lower() == 'none':
        query_params.object_name = "Service_Work_Order__c"
        query_params_data = query_params.transform()

    flag, count_result = data_fetcher.execute_sql_query(params=query_params_data, flag=1)

    if count_result == 0:
        no_data_message = {"IsPresent": False}
        # logging.info(no_data_message)
        return no_data_message, count_result
    else:
        return {"IsPresent": True}, count_result



def validate_query_params(validator):
    validation_results = {
        "account_id": validator.validate_account_id(),
        "object_name": validator.validate_object_name(),
        "date_range": validator.validate_date_range(),
        "page_number": validator.validate_page_number(),
        "page_size": validator.validate_page_size()
    }

    errors = {key: value[1] for key, value in validation_results.items() if not value[0]}
    if errors:
        return errors
    return None


def execute_query(query_params):
    try:
        # Transform query parameters
        query_params_data = query_params.transform()

        # Fetch data using the SqlDataFetcher instance with flag set to 0
        json_data, count_result = data_fetcher.execute_sql_query(query_params_data, flag=0)

        # Log the type and content of the data result for debugging
        # logging.info(f"Data result type: {type(json_data)}")
        # logging.info("Data result content:")
        # logging.info(json_data)

        # Check if the count_result is greater than 0
        if count_result > 0:
            if not json_data:
                # Construct and return a message indicating count and correct Page_Size/Page_Number
                message = f"NO Data found. Total count: {count_result}. Adjust Page_Size and Page_Number accordingly."
                logging.info(message)
                return message, count_result
            else:
                logging.info("Data found, processing...")
                return json_data, count_result
        else:
            # Construct and return a message for no data found
            no_data_message = f"No data found for Account_id {query_params.account_id} in Database."
            logging.info(no_data_message)
            return no_data_message, count_result

    except Exception as ex:
        # Log the exception for debugging purposes
        error_message = f"Error in execute_query: {str(ex)}"
        logging.error(error_message)
        # Optionally, you can decide whether to re-raise the exception or handle it differently
        raise Exception(error_message)