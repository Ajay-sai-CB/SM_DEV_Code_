# function_app.py

import azure.functions as func
import json
from code.validation_code.validation import QueryParameters, Validation
from code.sql_data_fetcher_code.sql_data_fetcher import SqlDataFetcher

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
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# HTTP trigger route
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Validate 'Account__c' parameter presence
        account_id = req.params.get('Account__c')
        if not account_id:
            # Return a 400 Bad Request response for missing 'Account__c' parameter
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

        # Initialize Validation with query parameters
        validator = Validation(query_params)

        # Handle Account ID Request if applicable
        if query_params.object_name is None or query_params.object_name.lower() == 'none':
            result = handle_account_id_request(query_params)

        # Handle Complex Request with validations
        else:
            validation_result = handle_object_request(query_params, validator)

            if validation_result["status"] == "validation_failed":
                # Return a 400 Bad Request response for validation failure
                return func.HttpResponse(
                    json.dumps({"message": "Validation failed", "errors": validation_result["error_messages"]}),
                    mimetype="application/json",
                    status_code=400
                )
            result = validation_result

        query_result = {
            "account_id": query_params.account_id,
            "object_name": query_params.object_name,
            "date_start_monthyear": query_params.date_start_monthyear,
            "date_end_monthyear": query_params.date_end_monthyear,
            "page_number": query_params.page_number,
            "page_size": query_params.page_size,
            "data": [result]  # Add your actual query result here
        }

        # Return a 200 OK response with the query result
        return func.HttpResponse(json.dumps(query_result), mimetype="application/json", status_code=200)

    except ValueError as ve:
        # Handle specific validation errors with a 400 Bad Request response
        return func.HttpResponse(
            json.dumps({"message": str(ve)}),
            mimetype="application/json",
            status_code=400
        )

    except Exception as e:
        # Log the exception and return a 500 Internal Server Error response
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

    if data_fetcher.fetch_data(query_params=query_params, flag=1):
        # Return a success message for existing data
        return f"Data for Account_id {query_params.account_id} exists in JSON data."
    else:
        # Return a message for no data found
        return f"No data found for Account_id {query_params.account_id} in JSON data."

# Handle Complex Request
def handle_object_request(query_params, validator):
    # Validate parameters using the Validation class
    is_valid_account_id, error_message_account_id = validator.validate_account_id()
    is_valid_object_name, error_message_object_name = validator.validate_object_name()
    is_valid_page_number, error_message_page_number = validator.validate_page_number()
    is_valid_page_size, error_message_page_size = validator.validate_page_size()
    is_valid_date_range, error_message_date_range = validator.validate_date_range()

    # Check if any validation failed
    if not all([is_valid_account_id, is_valid_object_name, is_valid_page_number, is_valid_page_size, is_valid_date_range]):
        # Return validation error message
        error_messages = {
            "account_id": error_message_account_id,
            "object_name": error_message_object_name,
            "page_number": error_message_page_number,
            "page_size": error_message_page_size,
            "date_range": error_message_date_range
        }
        return {"status": "validation_failed", "error_messages": error_messages}

    # Fetch data using the QueryParameters object and set flag to 0
    data_result = data_fetcher.fetch_data(query_params, flag=0)
    if data_result:
        # Return the data if available
        return data_result
    else:
        # Return a message for no data found
        return f"No data found for Account_id {query_params.account_id} in JSON data."
