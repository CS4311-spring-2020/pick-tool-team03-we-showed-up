# This Python file uses the following encoding: utf-8
import os
import subprocess
import splunklib.client as client
import splunklib.results as results
import json as json
import LogEntry


class SPLUNKInterface:


    def __init__(self):
        # starting splunk session (need to login)
        # subprocess.run(["./splunk start", event_name])
        self.event_name = ""
        self.path = ""
        self.index = ""
        self.askUsernamePassword()
        self.splunkClient = client.connect(username=self.username, password=self.password)
        if len(self.index) > 1:
            self.get_entries()



    # creating a new index (event)
    # on CLI ./splunk add index "event name"ArithmeticError
    def createEvent(self, event_name):
        self.event_name = event_name
        self.splunkClient.indexes.create(name=event_name)
        print("index ", self.event_name, " added")

    def addFilesMonitorDirectory(red_path, blue_path, white_path,  root_path):
        subprocess.run(["./splunk add oneshot", red_path])
        #keep on adding files, but need to know if you need to sleep between path ingestions
        subprocess.run(["add monitor [-source]", path])

    def exportLogs(self):
        # https://docs.splunk.com/Documentation/Splunk/8.0.2/Search/ExportdatausingCLI
        # example : splunk search [eventdata] -preview 0 -maxout 0 -output [rawdata|json|csv|xml] > [myfilename.log] ...
        # will retrieve json files
        return

    def get_entries(self, keyword=""):
        kwargs_export = {"earliest_time": "-1000h",
                         "latest_time": "now",
                         "search_mode": "normal"}
        search_query_export = "search index=" + self.index
        export_search_results = self.splunkClient.jobs.export(search_query_export, **kwargs_export)
        reader = results.ResultsReader(export_search_results)

        r_list = []
        # r_iter = iter(reader)

        for result in reader:
            if isinstance(result, dict):
                print(result)
                #entry = self.entry_from_dict(result)
                #print("Added Entry #", entry.number, " Content is: ", entry.content)
                #r_list.append(entry)

        return r_list

    def entry_from_dict(self, dict_entry):
        log_entry = LogEntry(number=int(dict_entry['_serial']),
                 timestamp=dict_entry['_time'],
                 content=dict_entry['_raw'],
                 host=dict_entry['host'],
                 source=dict_entry['source'],
                 sourcetype=dict_entry['sourcetype'])
        return log_entry

    def askUsernamePassword(self):
        self.username = input("Splunk Username:")
        self.password = input("Splunk Password:")
        self.index = input("Index name:")