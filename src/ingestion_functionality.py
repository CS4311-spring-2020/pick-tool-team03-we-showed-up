import os
from SPLUNKInterface import SPLUNKInterface


class IngestionFunctionality:

    def __init__(self):
        pass

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