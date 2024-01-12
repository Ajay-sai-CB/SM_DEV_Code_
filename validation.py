from datetime import datetime

VALID_OBJECT_NAMES = [
    "Service_Work_Order__c",
    "Invoice__c",
    "Invoice_Item__c",
    "Payment__c",
    "Payroll_Item__c",
    "Applied_Payment__c",
    "Applied_Coupon__c",
    "Apex_Log__c",
    "Work_Order_Service__c",
    "Work_Order_Teammate__c",
    "Work_Order_Room__c"
]

class Validation:
    def __init__(self, query_params):
        self.query_params = query_params

    def validate_account_id(self):
        if not self.query_params.account_id:
            return False, "Account_Id is required."
        return True, ""

    def validate_object_name(self):
        if self.query_params.object_name not in VALID_OBJECT_NAMES:
            return False, f"Invalid object_name: {self.query_params.object_name}"
        return True, ""

    def validate_date_range(self):
        if self.query_params.date_start_daymonthyear == '*' or self.query_params.date_end_daymonthyear == '*':
            return True, ""

        try:
            start_date = datetime.strptime(self.query_params.date_start_daymonthyear, "%Y-%m-%d")
            end_date = datetime.strptime(self.query_params.date_end_daymonthyear, "%Y-%m-%d")

            if start_date > end_date:
                return False, "Start date must be earlier than end date."

            # Check if the month and day are valid for a month with 30 days
            if start_date.month == 2 and start_date.day > 28:
                return False, "Invalid start date for February."
            if end_date.month == 2 and end_date.day > 28:
                return False, "Invalid end date for February."
                
            if start_date.month in [4, 6, 9, 11] and start_date.day > 30:
                return False, f"Invalid start date for {start_date.strftime('%B')}."
            if end_date.month in [4, 6, 9, 11] and end_date.day > 30:
                return False, f"Invalid end date for {end_date.strftime('%B')}."

        except ValueError:
            return False, "Invalid date format. Please use DD/MM/YYYY."
        return True, ""

    def validate_page_number(self):
        if not isinstance(self.query_params.page_number, int) or self.query_params.page_number < 0:
            return False, "Invalid Page_Number. It should be a non-negative integer."
        return True, ""

    def validate_page_size(self):
        if not isinstance(self.query_params.page_size, int) or self.query_params.page_size <= 0:
            return False, "Invalid Page_Size. It should be a positive integer."
        return True, ""
