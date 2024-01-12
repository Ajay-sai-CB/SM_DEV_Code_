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

def handle_account_id_request(query_params):
    query_params.object_name = query_params.object_name or "Service_Work_Order__c"
    query_params_data = query_params.transform()

    flag, count_result = data_fetcher.execute_sql_query(params=query_params_data, flag=1)

    if count_result == 0:
        return {"IsPresent": False}, count_result, 400
    else:
        return {"IsPresent": True}, count_result, 200

def validate_query_params(validator):
    validation_results = {key: validator_func() for key, validator_func in {
        "account_id": validator.validate_account_id,
        "object_name": validator.validate_object_name,
        "date_range": validator.validate_date_range,
        "page_number": validator.validate_page_number,
        "page_size": validator.validate_page_size
    }.items()}

    errors = {key: value[1] for key, value in validation_results.items() if not value[0]}
    return errors if errors else None

def execute_query(query_params):
    try:
        query_params_data = query_params.transform()
        json_data, count_result = data_fetcher.execute_sql_query(query_params_data, flag=0)

        if count_result > 0:
            if not json_data:
                message = f"NO Data found. Total count: {count_result}. Adjust Page_Size and Page_Number accordingly."
                return message, count_result, 400
            else:
                return json_data, count_result, 200
        else:
            no_data_message = f"No data found for Account_id {query_params.account_id} in Database."
            return no_data_message, count_result, 400

    except Exception as ex:
        error_message = f"Error in execute_query: {str(ex)}"
        logging.error(error_message)
        raise Exception(error_message)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        account_id = req.params.get('Account_Id')
        if not account_id:
            return log_error_and_return_response("Account_Id is required.", 400)

        query_params = QueryParameters(
            account_id=account_id,
            object_name=req.params.get('Object_Name', None),
            date_start_daymonthyear=req.params.get('Date_Start_YearMonthDay', '*'),
            date_end_daymonthyear=req.params.get('Date_End_YearMonthDay', '*'),
            page_number=int(req.params.get('Page_Number', 0)),
            page_size=int(req.params.get('Page_Size', 10))
        )

        validator = Validation(query_params)

        if query_params.object_name is None or query_params.object_name.lower() == 'none':
            result, count_result, status = handle_account_id_request(query_params)
        else:
            validation_result = validate_query_params(validator)
            if validation_result is not None:
                return log_error_and_return_response(f"Validation failed: {validation_result}", 400)
            result, count_result, status = execute_query(query_params)

        query_result = {
            "Account_Id": query_params.account_id,
            "Object_Name": query_params.object_name,
            "Date_Start_YearMonthDay": query_params.date_start_daymonthyear,
            "Date_End_YearMonthDay": query_params.date_end_daymonthyear,
            "Page_Number": query_params.page_number,
            "Page_Size": query_params.page_size,
            "Data": result,
            "Count": count_result
        }

        return func.HttpResponse(json.dumps(query_result), mimetype="application/json", status_code=status)

    except ValueError as ve:
        return log_error_and_return_response(f"Validation error: {ve}", 400)

    except Exception as e:
        return log_error_and_return_response(f"An unexpected error occurred: {str(e)}", 500)
