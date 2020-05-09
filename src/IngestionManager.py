import os
import shutil
from LogFile import LogFile
from EventSession import EventSession
from IngestionSubProcesses.OCRFeeder import ImageFeeder
from IngestionSubProcesses.AudioTranscriber import AudioRecognition
from IngestionSubProcesses.Validator import Validator
from IngestionSubProcesses.Cleanser import Cleanser


class IngestionManager:
    """This class manages the ingestion process of a log file. It is instantiated when the program initializes.
    This class ingests files into the instance of SPLUNK that the user last signed into.
    """

    def __init__(self, splunk=None, enforcement_action_report=None, table_manager=None, validator=None,
                 event_session=EventSession()):
        self.splunk = splunk
        self.enforcement_action_report = enforcement_action_report
        self.event_session = event_session
        self.event_session.set_start_and_end_times(start_time="2000-02-20 00:00:00", end_time="2021-03-02 00:00:00")
        self.validator = Validator(self.event_session.get_start_time(), self.event_session.get_end_time())
        self.table_manager = table_manager

    def add_splunk(self, splunk):
        """Replaces the current instance of splunk with a new instance."""
        self.splunk = splunk

    def get_temp_path(self, filepath):
        """Creates a new path to store processed transcribed, cleansed, and validated/unvalidated files.
        For example, for filepath, a new file path name will be returned using the following convention: _filepath
        """
        filepath_split = filepath.split("/")
        filepath_split[len(filepath_split)-1] = "_"+filepath_split[len(filepath_split)-1]
        separator = "/"
        new_path = separator.join(filepath_split)
        print("old path is: ", filepath)
        print("new path is: ", new_path)
        return new_path

    def read_log_files_from_directory(self, folder_path):
        """Reads all log file names from a folder path into an array and sends the log files to the table manager
        to populate the log file table. At the point of reading, If the log file is not a text file, this method
        sends the log files to the appropriate transcriber.
        """
        # If a folder path was incorrect, the process should not
        if not os.path.exists(folder_path):
            print(folder_path, " doesn't exist!")
            return

        # Retrieves the new path name created using the existing path name
        new_path = self.get_temp_path(folder_path)

        # Creates a new directory if it doesn't exist yet
        if not os.path.exists(new_path):
            print("made new folder: ", new_path)
            os.mkdir(new_path)

        for f in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, f)):
                if not (any(x.name == f for x in self.event_session.log_files)):
                    # Check if it's an audio file
                    if ".wav" in f:
                        audio_name = AudioRecognition.audio_transcribe(folder_path, new_path, f)
                        self.event_session.log_files.append(LogFile(audio_name, os.path.join(new_path, audio_name)))
                    elif (".png" in f) or (".jpg" in f) or (".jpeg" in f):
                        # If Image file transcribe it with the OCR
                        image_name = ImageFeeder.OCR_transcription(folder_path, new_path, f)
                        self.event_session.log_files.append(LogFile(image_name, os.path.join(new_path, image_name)))
                    else:
                        # Copy the file into the hidden directory and appends it to the logFile list
                        shutil.copy(os.path.join(folder_path, f), new_path)
                        self.event_session.log_files.append(LogFile(f, new_path + "/" + f))
        # Sends the log file list to the table manager to populate the log file table.
        self.table_manager.populate_log_file_table(self.event_session.log_files)

    def cleanse_files(self):
        """Sends all files to be cleansed."""
        for log_file in self.event_session.log_files:
            Cleanser.reader(log_file.get_name(), log_file.get_folder_path())

    def validate_files(self):
        """Sends each log file to the validator and updates the log file table with the status of validation."""
        for log_file in self.event_session.log_files:
            print("\nValidating: \n", log_file.get_path())
            self.validator.validate_file(log_file)
            if log_file.is_invalid():
                print("File invalid. With first errors: ", "Line: ", log_file.errors[0][0], " Error: ", log_file.errors[0][1])
            else:
                log_file.mark_validated()
                print("\nFile valid.\n")

            # Update the log file table with the validation status of each log file
            self.table_manager.populate_log_file_table(self.event_session.log_files)

    def ingest_directory_to_splunk(self, directory, index, splunk, sourcetype="", source=""):
        """Begins the ingestion process using the helper methods to read files, transcribe, cleanse,
        then validate above."""
        # Returns if the directory to ingest does not exist.
        if not os.path.exists(directory):
            print(directory, " doesn't exist!")
            return

        self.read_log_files_from_directory(directory)
        self.cleanse_files()
        self.validate_files()

        # Sends validated files to SPLUNK, and updates the ingestion status of each file to the lo file table.
        for log_file in self.event_session.log_files:
            if log_file.is_validated():
                splunk.add_file_to_index(log_file.get_path(), index)
                log_file.mark_ingested()
                self.table_manager.populate_log_file_table(self.event_session.log_files)

    def validate_file_anyway(self, index, splunk):
        """Validates the invalid log files into SPLUNK. Will only run at the users request."""
        marked = 0
        for i in range(len(self.event_session.log_files)):
            if self.event_session.log_files[i].is_marked():
                marked = i
                break

        if self.event_session.log_files[marked].is_validated():
            return

        # This is to mark statuses on the log file table
        self.event_session.log_files[marked].mark_validated()
        self.event_session.log_files[marked].errors = []
        splunk.add_file_to_index(self.event_session.log_files[marked].get_path(), index)
        self.event_session.log_files[marked].mark_ingested()
        self.table_manager.populate_log_file_table(self.event_session.log_files)
        self.table_manager.populate_enforcement_action_report_table(self.event_session.log_files[marked])

    def start_ingestion(self):
        event_name = self.event_session.get_event_name()
        root_path = self.event_session.get_root_path()
        red_folder = self.event_session.get_red_team_path()
        blue_folder = self.event_session.get_blue_team_path()
        white_folder = self.event_session.get_white_team_path()

        self.ingest_directory_to_splunk(root_path, event_name, self.splunk)

        if red_folder == "":
            red_folder = root_path + "/red"
            self.event_session.set_red_team_path(red_folder)
        self.ingest_directory_to_splunk(red_folder, event_name, self.splunk)

        if blue_folder == "":
            blue_folder = root_path + "/blue"
            self.event_session.set_blue_team_path(blue_folder)
        self.ingest_directory_to_splunk(blue_folder, event_name, self.splunk)

        if white_folder == "":
            white_folder = root_path + "/white"
            self.event_session.set_white_team_path(white_folder)
        self.ingest_directory_to_splunk(white_folder, event_name, self.splunk)