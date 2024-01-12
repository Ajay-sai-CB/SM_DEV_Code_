# **Azure Function: http\_trigger**

**Description:** This Azure Function acts as an HTTP trigger to query data from a SQL Server database based on specified parameters. It's designed to handle requests for retrieving records from different objects within the database, allowing users to filter data based on account\_id, object\_name, date range, and pagination settings.

**Trigger:** HTTP Trigger

**Input:**

- Account\_Id (required): Identifies the target account for data retrieval.
- Object\_Name (optional): Specifies the object name for the data query (default is "Service\_Work\_Order\_\_c").
- Date\_Start\_YearMonthDay (optional): Specifies the start date in the format "YYYY-MM-DD" for date range filtering (default is "\*").
- Date\_End\_YearMonthDay (optional): Specifies the end date in the format "YYYY-MM-DD" for date range filtering (default is "\*").
- Page\_Number (optional): Specifies the page number for paginated results (default is 0).
- Page\_Size (optional): Specifies the page size for paginated results (default is 10).

**Output:** JSON response containing queried data, count, and status code. Key information includes:

- Account\_Id
- Object\_Name
- Date\_Start\_YearMonthDay
- Date\_End\_YearMonthDay
- Page\_Number
- Page\_Size
- Data
- Count

**Environment Variables:**

- CONNECTION\_STRING: The connection string for accessing the SQL Server database.

**Dependencies:**

- azure.functions: Azure Functions library for Python.
- json: JSON encoding and decoding library.
- validation: Module containing classes and methods for input validation.
- sql\_data\_fetcher: Module containing the SqlDataFetcher class for executing SQL queries.
- logging: Standard Python logging module for logging messages.

**Usage:** Make an HTTP GET request to the function endpoint with the required parameters. The function processes the request, performs data validation, executes the SQL query, and returns a JSON response.

**Example:** HTTP GET Request:

curl --location 'https://func3-smb-sfda-dev.azurewebsites.net/api/http_trigger?code=kO22fotvdTrjdGpjcqg46e0z47T8A-OKY-_WcutP8Y8kAzFujM3VGw%3D%3D&Account_Id=0013000001HFpNSAA1&Object_Name=Service_Work_Order__c&Date_Start_YearMonthDay=2015-1-1&Date_End_YearMonthDay=2020-12-31&Page_Number=0&Page_Size=10'

Response Status: 200 OK
```
{
    "Account_Id": "0013000001HFpNSAA1",
    "Object_Name": "Service_Work_Order__c",
    "Date_Start_YearMonthDay": "2015-1-1",
    "Date_End_YearMonthDay": "2020-12-31",
    "Page_Number": 0,
    "Page_Size": 10,
    "Data": "[{\"Year_p\": \"Year=2015\", \"Month_p\": \"Month=01\", \"Day_p\": \"Day=16\", \"Id\": \"a0Z30000008LBUqEAO\", \"IsDeleted\": false, \"Name\": \"WO-6375266\", \"RecordTypeId\": null, \"CreatedDate\": \"2014-06-28 12:03:29\", \"CreatedById\": \"00530000009WGjPAAW\", \"LastModifiedDate\": \"2024-01-10 09:26:59\", \"LastModifiedById\": \"0058I0000032JPJQA2\", \"SystemModstamp\": \"2024-01-10 09:26:59\", \"LastActivityDate\": null, \"LastViewedDate\": null, \"LastReferencedDate\": null, \"Service_Agreement__c\": \"a0Y3000000AoUMhEAN\", \"Additional_Services_Windows_Cleaning__c\": 0.0, \"Amount_Due__c\": null, \"Balance__c\": 0.0, \"Cancellation_Reason__c\": null, \"Count__c\": 1.0, \"Customer_Address__c\": \"27w183 Chestnut Ln Winfield IL 60190\", \"Customer_Mobile__c\": \"(630) 306-9899\", \"Customer_Name__c\": \"Frank Acton\", \"Customer_Phone__c\": \"(630) 253-4755\", \"Date_Saturday__c\": null, \"Day_of_Visit_Formula__c\": \"Friday\", \"Day_of_Visit__c\": null, \"Discounts_All__c\": 0.0, \"Discounts_First_Time__c\": 0.0, \"Discounts_R1__c\": 0.0, \"Discounts_R2__c\": 0.0, \"Discounts__c\": 0.0, \"Driving_Directions__c\": null, \"ETL_ID__c\": null, \"Fee_Adjustment__c\": null, \"Fee_Amount__c\": null, \"Fee_Balance__c\": null, \"Fee_Received__c\": null, \"Fee_Sales_Tax__c\": 0.0, \"Fee_Sub_Total__c\": 0.0, \"First_Time_In_Discount__c\": null, \"First_Time_In_Grand_Total__c\": 0.0, \"First_Time_In_Sales_Tax__c\": 0.0, \"First_Time_In_Sub_Total__c\": null, \"First_Time_in_Fee__c\": null, \"Home_Entry_Method__c\": \"Customer is Home\", \"Location_Code__c\": \"4663\", \"Location_Id__c\": \"a0L3000000QLut9\", \"Lockout_Amount__c\": null, \"Lockout_Fee__c\": null, \"Lockout__c\": false, \"MMA_Discount_All__c\": null, \"MMA_Discount_R1__c\": null, \"MMA_Discount_R2__c\": null, \"MMA_Discount__c\": null, \"MMA_First_Time_In_Discount__c\": null, \"MapQuest_Miles__c\": 0.0, \"Not_Before__c\": \"24:00\", \"Open_Date__c\": null, \"Open_Record__c\": 0.0, \"Original_Schedule_Date__c\": null, \"Out_by__c\": \"13:00\", \"Payroll_Amount__c\": 0.0, \"Payroll_Items__c\": 0.0, \"Price__c\": null, \"Quarters__c\": null, \"Rescheduled_Reason__c\": \"Skip Early\", \"Rotation__c\": \"Rotation 1\", \"Sales_Rep_Discount_All__c\": null, \"Sales_Rep_Discount_R1__c\": null, \"Sales_Rep_Discount_R2__c\": null, \"Sales_Rep_Discount__c\": null, \"Sales_Tax__c\": 0.0, \"Service_Date__c\": \"2015-01-16 00:00:00\", \"Service_Type__c\": \"House\", \"Service_Zone__c\": \"240\", \"Services__c\": null, \"Special_Attention__c\": null, \"Status__c\": \"Final - Cancelled\", \"Sub_Total_All__c\": 0.0, \"Sub_Total_First_Time__c\": 0.0, \"Sub_Total_R1__c\": 0.0, \"Sub_Total_R2__c\": 0.0, \"Sub_Total__c\": 0.0, \"Time_In_Text__c\": null, \"Time_In__c\": null, \"Time_Out_Hours__c\": null, \"Time_Out_Minutes__c\": null, \"Time_Out_Text__c\": null, \"Time_Out__c\": null, \"Time_Spent_New__c\": null, \"Time_Spent_Text__c\": null, \"Time_Spent__c\": null, \"Time__c\": \"08:00\", \"Time_in_Hours__c\": null, \"Time_in_Minutes__c\": null, \"Total_Amount_Due__c\": 0.0, \"Total_Due_Trigger__c\": 0.0, \"Total_Grand_Total_All__c\": 0.0, \"Total_Grand_Total_R1__c\": 0.0, \"Total_Grand_Total_R2__c\": 0.0, \"Total_Revenue__c\": \"Total Revenue\", \"Total_Sales_Tax_All__c\": 0.0, \"Total_Sales_Tax_R1__c\": 0.0, \"Total_Sales_Tax_R2__c\": 0.0, \"Total_Sub_Total_All__c\": null, \"Total_Sub_Total_R1__c\": null, \"Total_Sub_Total_R2__c\": null, \"Total__c\": 0.0, \"Type__c\": \"2-Week\", \"Use_Sales_Tax_Rate__c\": null, \"Verified__c\": false, \"Visit_Order__c\": 0.0, \"Work_Team__c\": \"a0i30000009jLiSAAU\", \"per_Qtr__c\": 0.0, \"No_of_team_members_worked__c\": 2.0, \"Total_Rooms__c\": 0.0, \"isFirst__c\": false, \"Total_Miles__c\": 0.0, \"Customer_Start_Date__c\": \"2013-05-24 00:00:00\", \"Autogenerated__c\": true, \"Total_Quarters__c\": 0.0, \"Actual_Quarters__c\": null, \"Legacy_Other_Services__c\": false, \"Account__c\": \"0013000001HFpNSAA1\", \"Customer_Id__c\": \"0013000001HFpNS\", \"Time_In_Out__c\": null, \"Service_Date_Day__c\": \"Friday\", \"Redo_Work_Order__c\": false, \"One_Time__c\": false, \"Service_Agreement_Room_Count__c\": 16.0, \"Commission_Paid__c\": false, \"Customer_Number__c\": \"0000362639\", \"Service_Type_Report__c\": null, \"Employee_Payroll__c\": 0.0, \"Captain__c\": \"Unassigned\", \"Mate__c\": \"Ruthie Leach\", \"Rescheduled_Reason_Trim__c\": \"Skip Early\", \"Service_Type2__c\": \"House\", \"Branch_Code__c\": null, \"Mileage_Sum__c\": 0.0, \"Mileage__c\": 0.0, \"Within_Commission_Date__c\": false, \"After_Service_Agreement_Start_Date2__c\": true, \"Processed_Rooms_Services__c\": true, \"Work_Order_Rooms__c\": \"[{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSA5AAM\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSA5AAM\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTeEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAKAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAKAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTtEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSA7AAM\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSA7AAM\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTgEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSA8AAM\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSA8AAM\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CThEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSA9AAM\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSA9AAM\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTiEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAAAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAAAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTjEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSABAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSABAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTkEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSACAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSACAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTlEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSADAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSADAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTmEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAEAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAEAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTnEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAFAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAFAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CToEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAGAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAGAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTpEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAHAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAHAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTqEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAIAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAIAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTrEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSAJAA2\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSAJAA2\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTsEAN\\\",\\\"Cleaned__c\\\":true},{\\\"attributes\\\":{\\\"type\\\":\\\"Work_Order_Room__c\\\",\\\"url\\\":\\\"/services/data/v31.0/sobjects/Work_Order_Room__c/a0e30000003nSA6AAM\\\"},\\\"Work_Order__c\\\":\\\"a0Z30000008LBUqEAO\\\",\\\"Special_Attention__c\\\":false,\\\"Id\\\":\\\"a0e30000003nSA6AAM\\\",\\\"Room_and_Condition__c\\\":\\\"a0X3000000B6CTfEAN\\\",\\\"Cleaned__c\\\":true}]\", \"Work_Order_Services__c\": \"[]\", \"Key__c\": \"0\", \"Regular_Cleaning_Total__c\": 0.0, \"Week_of_Month__c\": \"3\", \"Week_of_Month_Matches_SA__c\": false, \"Day_of_Week_Matches_SA__c\": true, \"Teammate_Names__c\": null, \"Member_Count__c\": 2.0, \"Member_Count_Mismatch__c\": true, \"Surcharge__c\": 0.0, \"NPS_Count__c\": 1.0, \"NPS__c\": null, \"Service_Agreement_Time__c\": \"08:00\", \"Payment_Verified__c\": null, \"Pricing_Verified__c\": null, \"Production_Verified__c\": null, \"Team_Member_Miles__c\": 0.0, \"Team_Member_Quarters__c\": 0.0, \"Time_In_Numeric__c\": null, \"Time_Out_Numeric__c\": null, \"Team_Member_Count__c\": 2.0, \"Service_Agreement_Time_Mismatch__c\": false, \"Original_Service_Date__c\": null, \"Original_Work_Order__c\": null, \"Rescheduled_Work_Order__c\": false, \"Captain_Matches__c\": false, \"Customer_Assigned_Captain__c\": null, \"Work_Team_Captain__c\": \"Unassigned\", \"Dispatch_Assign__c\": null, \"Dispatch_Completed_Time__c\": null, \"Dispatch_Departed_Time__c\": null, \"Dispatch_Rating_Message__c\": null, \"Dispatch_Rating__c\": null, \"Dispatch_Send_Update__c\": null, \"Dispatch_Send__c\": null, \"Dispatch_Started_Time__c\": null, \"Dispatch_Status_Reason__c\": null, \"Dispatch_Status__c\": null, \"Dispatch_Driver_Answer__c\": null, \"PO_Number_Service_Agr__c\": null, \"One_Time_Cleaning__c\": null, \"Ismarked__c\": true, \"IsArchived__c\": false, \"AccountId\": \"0013000001HFpNSAA1\"}]",
    "Count": 1
}
```

**SQL Database External Data Source Setup:**
```
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'cb@12345'
GO

CREATE DATABASE SCOPED CREDENTIAL [SynapseCred]
WITH IDENTITY = 'Managed Identity'
GO

CREATE EXTERNAL DATA SOURCE SynapseDtSource
WITH
  (  LOCATION = 'https://smpocdatalake01.dfs.core.windows.net/archive-data',
    CREDENTIAL =  [SynapseCred]
)
GO

CREATE VIEW Invoice
AS
SELECT
  top 100  *
FROM
    OPENROWSET(
        BULK 'Invoice/*/**',
        data_source = 'SynapseDtSource',
        FORMAT = 'PARQUET'
    ) AS [result]
GO
```

**Creating a View:**
```
CREATE VIEW YourViewName AS
SELECT TOP 100 result.filepath(1) as [Year_p], result.filepath(2) as [Month_p], result.filepath(3) as [Day_p], *
FROM OPENROWSET(
    BULK 'Object=Invoice/*/*/*/**',
    DATA_SOURCE = 'SynapseArch6DtSource',
    FORMAT = 'PARQUET'
) AS [result];

**Python Script for Data Query:**

def _build_data_query(self, params):
    return f"""
        SET ANSI_WARNINGS OFF;
        SELECT * FROM {params['object_name']}
        WHERE {'Year_p >= ' + f"'{params['start_year_param']}' AND " if params['start_year_param'] != 'Year=*' else ''}
        {'Year_p <= ' + f"'{params['end_year_param']}' AND " if params['end_year_param'] != 'Year=*' else ''}
        {'Month_p >= ' + f"'{params['start_month_param']}' AND " if params['start_month_param'] != 'Month=*' else ''}
        {'Month_p <= ' + f"'{params['end_month_param']}' AND " if params['end_month_param'] != 'Month=*' else ''}
        {'Day_p >= ' + f"'{params['start_day_param']}' AND " if params['start_day_param'] != 'Day=*' else ''}
        {'Day_p <= ' + f"'{params['end_day_param']}' AND " if params['end_day_param'] != 'Day=*' else ''}
        AccountId = '{params['account_id_param']}'
        ORDER BY AccountId
        OFFSET {params['offset_param']} ROWS
        FETCH NEXT {params['fetch_next_param']} ROWS ONLY;
        SET ANSI_WARNINGS ON;
    """

```
**function\_app.py**

**Overview:** This script serves as an Azure Functions application written in Python. Its primary purpose is to handle HTTP triggers for querying data from a SQL Server database.

**Modules and Dependencies:**

- **azure.functions** : Imports necessary functions for Azure integration.
- **json** : Handles JSON data.
- **validation** : Imports the **Validation** class for parameter validation.
- **sql\_data\_fetcher** : Imports the **SqlDataFetcher** class for executing SQL queries.
- **logging** : Configures logging for debugging purposes.

**Configuration:**

- **connection\_string** : The connection string for the SQL Server database.

**Initialization:**

- **data\_fetcher** : An instance of the **SqlDataFetcher** class initialized with the connection string.
- **app** : Initialization of the FunctionApp without authentication.

**Helper Functions:**

- **log\_error\_and\_return\_response** : A function that logs errors and returns an HTTP response.
- **handle\_account\_id\_request** : Handles account ID requests and responds based on the result.
- **validate\_query\_params** : Validates various query parameters using the **Validation** class.
- **execute\_query** : Executes SQL queries and handles the results.

**HTTP Trigger Function:**

- **http\_trigger** : An HTTP trigger function that extracts parameters from the request and invokes appropriate functions based on conditions.

**sql\_data\_fetcher.py**

**Overview:** This module defines the **SqlDataFetcher** class, responsible for executing SQL queries using the **pyodbc** library.

**Class: SqlDataFetcher**

- **\_\_init\_\_** : Initializes the class with a connection string.
- **execute\_sql\_query** : Executes SQL queries based on parameters.

**Private Methods:**

- **\_build\_count\_query** : Builds a SQL query for counting records.
- **\_build\_data\_query** : Builds a SQL query for fetching data.

**QueryParameters Class**

**Overview:** A class representing parameters used in SQL queries.

- **transform** : A method transforming parameters for SQL queries.
- **extract\_year** , **extract\_month** , **extract\_day** : Helper methods for extracting date components.

**validation.py**

**Overview:** This module defines the **Validation** class for validating query parameters.

**Class: Validation**

- **Methods** : **validate\_account\_id** , **validate\_object\_name** , **validate\_date\_range** , **validate\_page\_number** , **validate\_page\_size** : Validating different aspects of query parameters.

**Constants:**

- **VALID\_OBJECT\_NAMES** : A list of valid object names for querying.

