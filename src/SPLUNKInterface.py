# This Python file uses the following encoding: utf-8
import os
import subprocess
import splunklib.client as client
import splunklib.results as results
from EventSession import EventSession
from LogEntry import LogEntry
from PyQt5 import QtCore
import threading
import time


class SPLUNKInterface(QtCore.QThread):
    updated_entries = QtCore.pyqtSignal()

    def __init__(self, event_session=EventSession()):
        super().__init__()
        self.event_session = event_session

        self.username = ""
        self.password = ""

        self.count = 0
        self.count_changed = False
        self.connected = False

        self.keyword = ""
        self.earliest_time = "-30y"
        self.latest_time = "now"

        if len(self.username) < 1:
            return
        self.splunkClient = client.connect(username=self.username, password=self.password)
        if len(self.event_session.get_event_name()) > 1:
            self.event_session.log_entries = self.get_entries()
            self.count = self.splunkClient.indexes[self.event_session.get_event_name()].totalEventCount
        self.connected = True

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_earliest_time(self, earliest_time):
        self.earliest_time = earliest_time

    def set_latest_time(self, latest_time):
        self.latest_time = latest_time

    def connect_client(self, username="", password=""):
        try:
            self.username = username
            self.password = password

            self.splunkClient = client.connect(username=self.username, password=self.password)
            if len(self.event_session.get_event_name()) > 1:
                self.event_session.log_entries = self.get_entries()
                self.count = self.splunkClient.indexes[self.event_session.get_event_name()].totalEventCount
            self.connected = True
            print("Succesfully connected to SPLUNK: ", username)
            thread = threading.Thread(target=self.automatic_update_check)
            thread.start()
            return True
        except Exception as e: 
            print(e)
            print("Login error to SPLUNK")
            return False

    # creating a new index (event)
    # need to add date time-frames
    def createEvent(self, event_name):
        try:
            for index in self.splunkClient.indexes.list():
                if event_name == index.name:
                    return 1
        except AttributeError:
            return 2

        try:
            self.splunkClient.indexes.create(name=event_name)
        except:
            return 3

    #open an event
    def open_event(self, event_name):
        self.event_session.set_event_name(event_name)
        return self.event_name

    def getIndexList(self):
        index_list = []
        for i in self.splunkClient.indexes.list():
            index_list.append(i.name)
        return index_list


    def addFilesMonitorDirectory(red_path, blue_path, white_path,  root_path):
        subprocess.run(["./splunk add oneshot", red_path])
        #keep on adding files, but need to know if you need to sleep between path ingestions
        subprocess.run(["add monitor [-source]", root_path])

    def get_entries(self):
        kwargs_export = {"earliest_time": self.earliest_time,
                         "latest_time": self.latest_time,
                         "search_mode": "normal"}
        print("kwargs is: ", kwargs_export)
        search_query_export = "search " + self.keyword + " index=" + self.event_session.get_event_name()
        export_search_results = self.splunkClient.jobs.export(search_query_export, **kwargs_export)
        reader = results.ResultsReader(export_search_results)

        r_list = []

        for result in reader:
            if isinstance(result, dict):
                entry = self.entry_from_dict(result)
                print("Added Entry #", entry.serial, " Content is: ", entry.content)
                r_list.append(entry)

        return r_list

    def refresh_log_entries(self):
        self.event_session.log_entries = self.get_entries()

    def entry_from_dict(self, dict_entry):
        log_entry = LogEntry(serial=int(dict_entry['_cd'].replace(":", "")),
                             timestamp=dict_entry['_time'],
                             content=dict_entry['_raw'],
                             host=dict_entry['host'],
                             source=dict_entry['source'],
                             sourcetype=dict_entry['sourcetype'])
        return log_entry

    def add_file_to_index(self, filepath, index):
        try:
            curr_ind = self.splunkClient.indexes[index]
            curr_ind.upload(filepath)
            print("Uploaded to index: ", index)
        except Exception as e:
            print("Failed to upload, error ", str(e))

    def automatic_update_check(self):
        print("started automatic check for entries")
        self.update_entries(bypass_check=True)
        while True:
            time.sleep(10)
            print("update check")
            self.update_entries()

    def update_entries(self, bypass_check=False):
        if not self.connected:
            return 0
        if (self.count_changed and self.count == self.splunkClient.indexes[self.event_session.get_event_name()].totalEventCount) or bypass_check:
            try:
                self.refresh_log_entries()
                self.count_changed = False
                print("entries refreshed")
                self.updated_entries.emit()
                return 1
            except Exception as e:
                print("Unable to refresh log entries, error is: ", str(e))
                return 0

        if not self.count == self.splunkClient.indexes[self.event_session.get_event_name()].totalEventCount:
            self.count_changed = True
            self.count = self.splunkClient.indexes[self.event_session.get_event_name()].totalEventCount
            print("Updated total count atm is: ", self.count)

        return 0
