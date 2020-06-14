# coding: utf-8

import json
import os


class SettingsFileController:
    
    _work_dir_path = ''
    _SETTING_FILE_NAME = 'settings.json'
    _settings_file_path = ''

    def __init__(self):
        self._work_dir_path = os.getcwd()
        self._settings_file_path = self._work_dir_path + '/' + self._SETTING_FILE_NAME

    def readSettings(self):
        json_dic = None

        try:
            with open(self._settings_file_path, 'r') as settings_file:
                json_dic = json.load(settings_file)
        except FileNotFoundError as error:
            print(error)

        return json_dic

    def writeSettings(self, json_dic):
        with open(self._settings_file_path, 'w') as settings_file:
            json.dump(json_dic, settings_file, indent=4)

    def removeSettings(self):
        if os.path.isfile(self._settings_file_path):
            os.remove(self._settings_file_path)
        else:
            print('file not exist....')
