
# function_app.py
 
import azure.functions as func
import json
from validation import  Validation
from sql_data_fetcher import SqlDataFetcher , QueryParameters
import logging
 
# Define the connection string
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
 
# Create an instance of the SqlDataFetcher class
data_fetcher = SqlDataFetcher(connection_string)
 
# FunctionApp initialization
# app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
# FunctionApp initialization without authentication
app = func.FunctionApp()
 
# HTTP trigger route
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Validate 'Account__c' parameter presence
        account_id = req.params.get('Account__c')
        if not account_id:
            return func.HttpResponse(
                json.dumps({"message": "Account__c is required."}),
                mimetype="application/json",
                status_code=400
            )

        # Get query parameters
        query_params = QueryParameters(
            account_id=account_id,
            object_name=req.params.get('object_name', None),
            date_start_monthyear=req.params.get('Date_Start_MonthYear', '*'),
            date_end_monthyear=req.params.get('Date_End_MonthYear', '*'),
            page_number=int(req.params.get('Page_Number', 0)),
            page_size=int(req.params.get('Page_Size', 10))
        )

        # Initialize Validation
        validator = Validation(query_params)

        # Handle Account ID Request if applicable
        if query_params.object_name is None or query_params.object_name.lower() == 'none':
            result = handle_account_id_request(query_params)

        # Handle Complex Request with validations
        else:
            validation_result = validate_query_params(validator)
            if validation_result is not None:
                return func.HttpResponse(
                    json.dumps({"message": "Validation failed", "errors": validation_result}),
                    mimetype="application/json",
                    status_code=400
                )
            result = execute_query(query_params)

        query_result = {
            "account_id": query_params.account_id,
            "object_name": query_params.object_name,
            "date_start_monthyear": query_params.date_start_monthyear,
            "date_end_monthyear": query_params.date_end_monthyear,
            "page_number": query_params.page_number,
            "page_size": query_params.page_size,
            "data": result  # Add your actual query result here
        }

        return func.HttpResponse(json.dumps(query_result), mimetype="application/json", status_code=200)

    except ValueError as ve:
        return func.HttpResponse(
            json.dumps({"message": str(ve)}),
            mimetype="application/json",
            status_code=400
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"message": f"An unexpected error occurred. {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )
 
# Handle Account ID Request
def handle_account_id_request(query_params):
    if query_params.object_name is None or query_params.object_name.lower() == 'none':
        # If object_name is "None," set it to "Service_Work_Order__c"
        query_params.object_name = "Service_Work_Order__c"
        query_params_data = query_params.transform()
 
    if data_fetcher.execute_sql_query(params=query_params_data, flag=1):
        # Return a success message for existing data
        return f"Data for Account_id {query_params.account_id} exists in Database."
    else:
        # Return a message for no data found
        return f"No data found for Account_id {query_params.account_id} in Database."
 
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
        data_result = data_fetcher.execute_sql_query(query_params_data, flag=0)
        
        # Log the type and content of the data result for debugging
        logging.info(f"Data result type: {type(data_result)}")
        logging.info("Data result content:")
        logging.info(data_result)

        # Check if the result contains data
        if data_result:
            logging.info("Data found, processing...")
            return data_result
        else:
            # Construct and return a message for no data found
            no_data_message = f"No data found for Account_id {query_params.account_id} in Database ."
            logging.info(no_data_message)
            return no_data_message

    except Exception as ex:
        # Log the exception for debugging purposes
        error_message = f"Error in execute_query: {str(ex)}"
        logging.error(error_message)
        # Optionally, you can decide whether to re-raise the exception or handle it differently
        raise Exception(error_message)
