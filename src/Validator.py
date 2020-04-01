import re
from dateutil.parser import parse
from datetime import datetime as dt

class Validator:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.expressions = []
        with open('ValidationFormats.txt',"r") as formats:
            for format in formats:
                expression = format.rstrip("\n")
                self.expressions.append(expression)
        self.date_time_styles = []
        with open('ValidationConverter.txt',"r") as styles:
            for style in styles:
                date_time_style = style.rstrip("\n")
                self.date_time_styles.append(date_time_style)
        pass

    #This method takes a singular log file and validates the timestamp.
    def validate_file(self, log_file):

        invalid_file_info = []

        line_number = 0
        for line in open(log_file.get_path()):
            errormessage = ""
            timestamp = ""
            #check if timestamp exists.
            style_num = 0
            for expression in self.expressions:
                timestamp = re.search(expression,line)
                if timestamp is not None:
                    timestamp = timestamp.group(0)
                    time = dt.strptime(timestamp, self.date_time_styles[style_num])
                    #print(time)
                    #compare timestamp to user timestamp
                    #errormessage = "Timestamp invalid."
                    break
                style_num = style_num + 1
            if not timestamp:
                 errormessage = "Timestamp does not exist."
                 #sprint(errormessage)
            if errormessage:
                 invalid_file_info.append(line_number)
                 invalid_file_info.append(errormessage)
            #else:
                 #print("success on line number:" + str(line_number))
                 #print(timestamp)
            line_number = line_number + 1

        return log_file
