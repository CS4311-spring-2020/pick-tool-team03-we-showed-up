import re
from dateutil.parser import parse
from datetime import datetime as dt

class Validator:
    """This class validated text file using the timestamps in the log files and a time range."""


    def __init__(self, start_date, end_date):
        self.start_date = dt.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        self.end_date = dt.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        self.expressions = []
        with open('./IngestionSubProcesses/ValidationFormats.txt',"r") as formats:
            for format in formats:
                expression = format.rstrip("\n")
                self.expressions.append(expression)
        self.date_time_styles = []
        with open('./IngestionSubProcesses/ValidationConverter.txt',"r") as styles:
            for style in styles:
                date_time_style = style.rstrip("\n")
                self.date_time_styles.append(date_time_style)
        pass


    def validate_file(self, log_file):
        """Takes a signuar file and validates each timestamp in every line compared to the start and end dates initialized.
        Errors in log files can be grouped into invalid, no timestamp, and valid. The errors will be saves for every line in the file."""
        line_number = 1
        for line in open(log_file.get_path()):
            invalid_file_info = []
            errormessage = ""
            timestamp = ""
            #check if timestamp exists.
            style_num = 0
            for expression in self.expressions:
                timestamp = re.search(expression,line)
                if timestamp is not None:
                    timestamp = timestamp.group(0)
                    log_entry_time = dt.strptime(timestamp, self.date_time_styles[style_num])
                    #compare timestamp to user timestamp
                    if not (self.start_date <= log_entry_time <= self.end_date):
                        errormessage = "Timestamp invalid."
                    break
                style_num = style_num + 1
            if not timestamp:
                 errormessage = "Timestamp does not exist."
            if errormessage:
                 invalid_file_info.append(line_number)
                 invalid_file_info.append(errormessage)
                 log_file.add_errors(invalid_file_info)
                 log_file.mark_invalid()
            line_number = line_number + 1

        return log_file
