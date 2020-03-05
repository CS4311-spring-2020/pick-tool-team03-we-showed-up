# This Python file uses the following encoding: utf-8
import os
import subprocess
import splunklib.client as client
import splunklib.results as results
from logentry import LogEntry


class SPLUNKInterface:

    def __init__(self):
        # starting splunk session (need to login)
        # subprocess.run(["./splunk start", event_name])

        #Event Data.. should we make a class?
        self.event_name = "main"
        self.event_description = ""
        self.askUsernamePassword()
        self.path = ""
        self.splunkClient = client.connect(username=self.username, password=self.password)
        if len(self.event_name) > 1:
            self.logentries = self.get_entries()

    # creating a new index (event)
    # need to add date time-frames
    def createEvent(self, event_name, event_description):
        for index in self.splunkClient.indexes.list():
            if (event_name == index.name):
                return 1
        self.event_name = event_name
        self.splunkClient.indexes.create(name=event_name)
        self.event_description = event_description

    #open an event
    def open_event(self, event_name):
        self.event_name = event_name
        self.event_description = "Event description for " + event_name + "goes here"
        return self.event_description

    def getIndexList(self):
        index_list = []
        for i in self.splunkClient.indexes.list():
            index_list.append(i.name)
        return index_list


    def addFilesMonitorDirectory(red_path, blue_path, white_path,  root_path):
        subprocess.run(["./splunk add oneshot", red_path])
        #keep on adding files, but need to know if you need to sleep between path ingestions
        subprocess.run(["add monitor [-source]", path])

    def get_entries(self, keyword=""):
        kwargs_export = {"earliest_time": "-1000h",
                         "latest_time": "now",
                         "search_mode": "normal"}
        search_query_export = "search index=" + self.event_name
        export_search_results = self.splunkClient.jobs.export(search_query_export, **kwargs_export)
        reader = results.ResultsReader(export_search_results)

        r_list = []
        # r_iter = iter(reader)

        for result in reader:
            if isinstance(result, dict):
                #print(result)
                entry = self.entry_from_dict(result)
                print("Added Entry #", entry.serial, " Content is: ", entry.content)
                r_list.append(entry)

        return r_list

    def entry_from_dict(self, dict_entry):
        log_entry = LogEntry(serial=int(dict_entry['_serial']),
                             timestamp=dict_entry['_time'],
                             content=dict_entry['_raw'],
                             host=dict_entry['host'],
                             source=dict_entry['source'],
                             sourcetype=dict_entry['sourcetype'])
        return log_entry

    def askUsernamePassword(self):

        self.username = input("Splunk Username:")
        self.password = input("Splunk Password:")

    def add_file_to_index(self, filepath, index):
        try:
            curr_ind = self.splunkClient.indexes[index]
            curr_ind.upload(filepath)
            print("Uploaded to index: ", index)
        except Exception as e:
            print("Failed to upload, error ", str(e))
