import os
from SPLUNKInterface import SPLUNKInterface
from LogFile import LogFile


class IngestionFunctionality:

    def __init__(self, splunk=None, enforcement_action_report=None, validator=None, logFiles=[]):
        self.splunk = splunk
        self.enforcement_action_report = enforcement_action_report
        self.validator = validator
        self.logFiles = logFiles
        print("initialized log files as ", logFiles)

    def add_splunk(self, splunk):
        self.splunk = splunk

    def get_file_paths_from_folder(self, folder_path):
        for f in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, f)):
                print("trying to add file", f)
                if not (any(x.name == f for x in self.logFiles)):
                    if (".mp3" in f) or (".wav" in f) or (".png" in f) or (".jpg" in f) or (".jpeg" in f):
                        print("Transcribing ... ", f)
                        # TODO: Transcribe here

                    else:
                        print("Added file directly  ", f)
                        self.logFiles.append(LogFile(f, folder_path + "/" + f))

    def ingest_directory_to_splunk(self, directory, index, splunk, sourcetype="", source=""):
        self.get_file_paths_from_folder(directory)
        print("called ingest_directory_to_splunk")
        for log_file in self.logFiles:
            splunk.add_file_to_index(log_file.get_path(), index)

    def validate_files(self, start_date, end_date, index):
        for log_file in self.logFiles:
            # Validate "file" (this is the filepath) send enforcement
            # action report as parameter to make sure we append the lines
            # maybe return a list of validated files that are set to be ingested to Splunk?
            print("Validating: ", log_file.get_path())

        # Send signal of Enforcement action report changes (this will be connected to the UI)

        for log_file in self.logFiles:
            if log_file.is_validated():
                splunk.add_file_to_index(f, index)
