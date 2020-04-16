import os
import shutil

from LogFile import LogFile
from SPLUNKInterface import SPLUNKInterface
from Transcribers.OCRFeeder import ImageFeeder


class IngestionFunctionality:

    def __init__(self, splunk=None, enforcement_action_report=None, validator=None, logFiles=[]):
        self.splunk = splunk
        self.enforcement_action_report = enforcement_action_report
        self.validator = validator
        self.logFiles = logFiles
        self.start_date = "2/20/2020 06:00:00"
        self.end_date = "3/02/2020 06:00:00"
        print("initialized log files as ", logFiles)

    def add_splunk(self, splunk):
        self.splunk = splunk

    def get_temp_path(self, filepath):
        filepath_split = filepath.split("/")
        filepath_split[len(filepath_split)-1] = "_"+filepath_split[len(filepath_split)-1]
        separator = "/"
        new_path = separator.join(filepath_split)
        print("old path is: ", filepath)
        print("new path is: ", new_path)
        return new_path


    def read_log_files_from_directory(self, folder_path):
        new_path = self.get_temp_path(folder_path)

        # Creates the new directory if it doesn't exist yet
        if not os.path.exists(new_path):
            print("made new folder: ", new_path)
            os.mkdir(new_path)

        for f in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, f)):
                if not (any(x.name == f for x in self.logFiles)):
                    # Check if it's an audio or image file
                    if (".mp3" in f) or (".wav" in f) or (".png" in f) or (".jpg" in f) or (".jpeg" in f):
                        print("Transcribing ... ", f)
                        # TODO: Transcribe here
                        OCRTranscription(folder_path, new_path, f)


                    else:
                        # Copy the file into the hidden directory and appends it to the logFile list
                        print("Added file directly  ", f)
                        shutil.copy(os.path.join(folder_path, f), new_path)
                        self.logFiles.append(LogFile(f, new_path + "/" + f))

    def ingest_directory_to_splunk(self, directory, index, splunk, sourcetype="", source=""):
        self.read_log_files_from_directory(directory)
        self.validate_files(self.start_date, self.end_date)
        #print("called ingest_directory_to_splunk")
        #for log_file in self.logFiles:
            #splunk.add_file_to_index(log_file.get_path(), index)

    def validate_files(self, start_date, end_date):
        for log_file in self.logFiles:
            print(LogFile.get_path(log_file))
            # Validate "file" (this is the filepath) send enforcement
            # action report as parameter to make sure we append the lines
            # maybe return a list of validated files that are set to be ingested to Splunk?
            print("Validating: ", log_file.get_path())

        # Send signal of Enforcement action report changes (this will be connected to the UI)

        for log_file in self.logFiles:
            if log_file.is_validated():
                splunk.add_file_to_index(f, index)
