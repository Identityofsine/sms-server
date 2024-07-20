from datetime import datetime as Date
def convert_to_datetime(date_string):
    # Define the format that matches the input string
    date_format = "%Y%m%dT%H%M%S"
    
    # Parse the string into a datetime object
    datetime_obj = Date.strptime(date_string, date_format)
    
    return datetime_obj

#export functions

__all__ = ["convert_to_datetime"]

