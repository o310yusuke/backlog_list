
import json
import os
import unittest

import classes.settings_file_controller as target_module


class TestFileController(unittest.TestCase):
    _targetClass = None

    _settings_json = {
        'spacename' : 'testSpaceName',
        'target_pj' : '99999',
        'apikey' : 'testapikey',
    }

    def setUp(self):
        self._targetClass = target_module.SettingsFileController()

    def tearDown(self):
        self._targetClass.removeSettings()

    def test_readSettings_fine_notexist(self):
        json_dic = self._targetClass.readSettings()
        self.assertIsNone(json_dic)

    def test_readSettings_file_exist(self):
        self._targetClass.writeSettings(
            self._settings_json
        )
        json_dic = self._targetClass.readSettings()
        self.assertEqual(
            json_dic.get('spacename'), 
            self._settings_json.get('spacename')
        )
        self.assertEqual(
            json_dic.get('target_pj'),
            self._settings_json.get('target_pj')
        )
        self.assertEqual(
            json_dic.get('apikey'),
            self._settings_json.get('apikey')
        )
        

    def test_writeSettings(self):
        self._targetClass.writeSettings(
            self._settings_json
        )


if __name__ == "__main__":
    unittest.main()
