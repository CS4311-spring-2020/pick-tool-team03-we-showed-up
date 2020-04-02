import fileinput
import csv
import os.path


class Cleanser:
    # Read file
    def reader(filename, filepath):
        filetype = filename[-3:]
        if filetype == "txt" or filetype == "log":
            with open(os.path.join(filepath, filename), "r") as file:
                data = [line.rstrip('\n') for line in file]
            Cleanser.write(data, filename, filepath)

        elif filetype == "csv":
            data_csv = []
            with open(os.path.join(filepath, filename), "r") as file_csv:
                reader_csv = csv.reader(file_csv, delimiter=',')
                for row in reader_csv:
                    data_csv.append(row)
            Cleanser.write(data_csv, filename, filepath)

    # Write final result
    def write(lineList, filename, filepath):
        # Check type of file
        filetype = filename[-3:]

        # Cleanse .txt file
        # NOTE: general unwanted characters are cleansed, but there are still a few that need to be added
        if (filetype == "txt"):
            # Path of new file.
            # NOTE: The file specified in filename has a copy with termination "temp.txt"
            # This is done to allow multiple testing
            file = os.path.join(filepath, filename)
            # Unwanted characters
            unwanted_chars = ["i[", "[C", "[K", "[A", "[[", "[0", "[5C", "1P", "@", ";", " -", "\r"]

            # Write to new file while cleansing
            with open(file, "w") as outputFile:
                # Cleanse and write to new file
                for line in lineList:
                    for character in unwanted_chars:
                        line = line.replace(character, "")
                    # Remove unicode
                    line = line.replace(u"\u0007", u"")
                    line = line.replace(u"\u0008", u"")
                    line = line.replace(u"\u001B", u"")
                    # Check for empty lines
                    if line.strip() != "":
                        outputFile.write(line + "\n")

        # Cleanse .log file
        elif (filetype == "log"):
            # Path of new file.
            # NOTE: The file specified in file name has a copy with termination "temp.log"
            # This is done to allow multiple testing
            file = os.path.join(filepath, filename)
            with open(file, "w") as outputFile:
                for line in lineList:
                    if line.strip() != "":
                        outputFile.write(line + "\n")

        # Cleanse .csv file
        elif (filetype == "csv"):
            # Path of new file.
            # NOTE: The file specified in filename could not be rewritten and a temporary file was made with termination "temp.csv"
            # This is done to allow multiple testing
            file = os.path.join(filepath, filename)
            with open(file, "w") as outputFile:
                for line in lineList:
                    for i in line:
                        if i.strip() != "":
                            outputFile.write(i + ", ")
                    outputFile.write("\n")


# Testing
# reader("exp-t1to4-datafile-csv.csv", r"C:\Users\diego\PycharmProjects\tutorial\SWII_Scripts")
# reader("secure.log", r"C:\Users\diego\PycharmProjects\tutorial\SWII_Scripts")
# reader("20_CSI_C_input.txt", r"C:\Users\diego\PycharmProjects\tutorial\SWII_Scripts")
# reader("01_input.txt", r"C:\Users\diego\PycharmProjects\tutorial\SWII_Scripts")
