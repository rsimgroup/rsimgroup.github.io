import os
import json


class BookKeeping:
    '''
    This class keeps the bookkeeping information of a webpage, including all files pertained to the webpage
    '''
    def __init__(self, time_stamp_directory_path):
        self._time_stamp_directory_path = time_stamp_directory_path

    def get_timestamp_path(self):
        return os.path.join(self._time_stamp_directory_path, "timestamp.json")

    def updateTimeStamp(self, dump_file_path='', content_file_path='', script_file_path='', base_file_path='', data_file_path=''):

        with open(self.get_timestamp_path(), "r") as f:
            try:
                timestamp = json.load(f)
            except ValueError:
                timestamp = {}
        if data_file_path != '':
            timestamp[data_file_path] = os.path.getmtime(dump_file_path)
        if dump_file_path != '':
            timestamp[dump_file_path] = os.path.getmtime(dump_file_path)
        if content_file_path != '':
            timestamp[content_file_path] = os.path.getmtime(content_file_path)
        if script_file_path != '':
            timestamp[script_file_path] = os.path.getmtime(script_file_path)
        if base_file_path != '':
            timestamp[base_file_path] = os.path.getmtime(base_file_path)
        with open(self.get_timestamp_path(), "w") as f:
            json.dump(timestamp, f)

    def isModified(self, dump_file_path='', content_file_path='', script_file_path='', base_file_path='', data_file_path=''):

        with open(self.get_timestamp_path(), "r") as f:
            try:
                timestamp = json.load(f)
            except ValueError:
                timestamp = {}

        file_time_dict = {}
        try:
            if data_file_path != '':
                file_time_dict[data_file_path] = os.path.getmtime(dump_file_path)
            if dump_file_path != '':
                file_time_dict[dump_file_path] = os.path.getmtime(dump_file_path)
            if script_file_path != '':
                file_time_dict[script_file_path] = os.path.getmtime(script_file_path)
            if content_file_path != '':
                file_time_dict[content_file_path] = os.path.getmtime(content_file_path)
            if base_file_path != '':
                file_time_dict[base_file_path] = os.path.getmtime(base_file_path)
        except FileNotFoundError:
            return True

        not_in_flag = 0
        updated_flag = 0
        for file_path, curr_file_time in file_time_dict.items():
            if file_path not in timestamp:
                not_in_flag = 1
                timestamp[file_path] = curr_file_time
            elif timestamp[file_path] < curr_file_time:
                updated_flag = 1
                timestamp[file_path] = curr_file_time

        with open(self.get_timestamp_path(), "w") as f:
            json.dump(timestamp, f)

        if not_in_flag or updated_flag:
            return True
        else:
            return False
