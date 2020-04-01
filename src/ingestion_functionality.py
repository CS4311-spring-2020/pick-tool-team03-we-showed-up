import os
from SPLUNKInterface import SPLUNKInterface


class IngestionFunctionality:

    def __init__(self, splunk=None, enforcement_action_report=None, validator=None):
        self.splunk = splunk
        self.enforcement_action_report = enforcement_action_report
        self.validator = validator
        pass

    def add_splunk(self, splunk):
            self.splunk = splunk

    def get_file_paths_from_folder(self, folder_path):
        files = []
        for f in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, f)):
                files.append(folder_path + "/" + f)

        print(files)
        return files

    def ingest_directory_to_splunk(self, folder_path, index,  splunk, sourcetype="", source=""):
        files = self.get_file_paths_from_folder(folder_path)
        for file in files:
            splunk.add_file_to_index(file, index)

    def validate_files(self, folder_path, start_date, end_date, index):
        files = self.get_file_paths_from_folder(folder_path)
        for file in files:
            # Validate "file" (this is the filepath) send enforcement
            # action report as parameter to make sure we append the lines
            # maybe return a list of validated files that are set to be ingested to Splunk?
            validated_files = files  # remove this when completed

        # Send signal of Enforcement action report changes (this will be connected to the UI)

        for f in validated_files:
            splunk.add_file_to_index(f, index)