import os
import shutil

from LogFile import LogFile
from SPLUNKInterface import SPLUNKInterface

from Transcribers.OCRFeeder import ImageFeeder
from Validator import Validator
from Transcribers.AudioTranscriber import AudioRecognition
from Cleanser import Cleanser

class IngestionFunctionality:
    def __init__(self, splunk=None, enforcement_action_report=None, table_manager=None, validator=None, logFiles=[],
                 event_config = None):
        self.splunk = splunk
        self.enforcement_action_report = enforcement_action_report
        self.event_config = event_config
        self.event_config.starttime = "2000-02-20 00:00:00"
        self.event_config.endtime = "2021-03-02 00:00:00"
        self.validator = Validator(self.event_config.starttime, self.event_config.endtime)
        self.logFiles = logFiles
        self.table_manager = table_manager
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
        if not os.path.exists(folder_path):
            print(folder_path, " doesn't exist!")
            return

        new_path = self.get_temp_path(folder_path)

        # Creates the new directory if it doesn't exist yet
        if not os.path.exists(new_path):
            print("made new folder: ", new_path)
            os.mkdir(new_path)

        for f in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, f)):
                if not (any(x.name == f for x in self.logFiles)):
                    # Check if it's an audio file
                    if ".wav" in f:
                        audio_name = AudioRecognition.audio_transcribe(folder_path, new_path, f)
                        self.logFiles.append(LogFile(audio_name, os.path.join(new_path, audio_name)))

                    elif (".png" in f) or (".jpg" in f) or (".jpeg" in f):
                        # If Image file transcribe it with the OCR
                        image_name = ImageFeeder.OCR_transcription(folder_path, new_path, f)
                        self.logFiles.append(LogFile(image_name, os.path.join(new_path, image_name)))

                    else:
                        # Copy the file into the hidden directory and appends it to the logFile list
                        shutil.copy(os.path.join(folder_path, f), new_path)
                        self.logFiles.append(LogFile(f, new_path + "/" + f))
        self.table_manager.populate_log_file_table(self.logFiles)

    def cleanse_files(self):
        for log_file in self.logFiles:
            Cleanser.reader(log_file.get_name(), log_file.get_folder_path())

    def ingest_directory_to_splunk(self, directory, index, splunk, sourcetype="", source=""):
        if not os.path.exists(directory):
            print(directory, " doesn't exist!")
            return

        self.read_log_files_from_directory(directory)
        self.cleanse_files()
        self.validate_files()

        for log_file in self.logFiles:
            if log_file.is_validated():
                splunk.add_file_to_index(log_file.get_path(), index)
                log_file.mark_ingested()
                self.table_manager.populate_log_file_table(self.logFiles)

    def validate_files(self):
        for log_file in self.logFiles:
            print("\nValidating: \n", log_file.get_path())
            self.validator.validate_file(log_file)
            # Validate "file" (this is the filepath) send enforcement
            # action report as parameter to make sure we append the lines
            # maybe return a list of validated files that are set to be ingested to Splunk?
            if log_file.is_invalid():
                print("File invalid. With first errors:")
                print("Line: ")
                print(log_file.errors[0][0])
                print("Error: ")
                print(log_file.errors[0][1])

                # Send signal of Enforcement action report changes (this will be connected to the UI)
            else:
                log_file.mark_validated()
                print("\nFile valid.\n")

            self.table_manager.populate_log_file_table(self.logFiles)

    def validate_file_anyway(self, index, splunk):
        marked = 0
        for i in range(len(self.logFiles)):
            if self.logFiles[i].is_marked():
                marked = i
                break

        if self.logFiles[marked].is_validated():
            return

        self.logFiles[marked].mark_validated()
        self.logFiles[marked].errors = []
        splunk.add_file_to_index(self.logFiles[marked].get_path(), index)
        self.logFiles[marked].mark_ingested()
        self.table_manager.populate_log_file_table(self.logFiles)
        self.table_manager.populate_enforcement_action_report_table(self.logFiles[marked])
