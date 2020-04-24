import fileinput
import csv
import os.path


class Cleanser:
    """This class cleanses a text file from all non alphabetical, numerical, and punctuational characters."""


    def reader(filename, filepath):
        """Takes a text file froma file path and reads the data."""
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


    def write(lineList, filename, filepath):
        """Modifies the text file as it it writing it as a new file.
        The format of filename is specified as: filenametemp.text"""
        filetype = filename[-3:]
        # Cleanse .txt file
        if (filetype == "txt"):
            file = os.path.join(filepath, filename)
            unwanted_chars = ["i[", "[C", "[K", "[A", "[[", "[0", "[5C", "1P", "@", ";", " -", "\r"]
            # Cleanses file as it is being written
            with open(file, "w") as outputFile:
                for line in lineList:
                    for character in unwanted_chars:
                        line = line.replace(character, "")
                    line = line.replace(u"\u0007", u"")
                    line = line.replace(u"\u0008", u"")
                    line = line.replace(u"\u001B", u"")
                    if line.strip() != "":
                        outputFile.write(line + "\n")
        # Cleanse .log file
        elif (filetype == "log"):
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
