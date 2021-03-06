# coding: utf-8

import datetime
import tkinter as tk
from tkinter import font, ttk

import requests

from classes.settings_file_controller import SettingsFileController


class Application(tk.Frame):
    # プライベート変数
    _entry_spacename = None
    _entry_target_pj = None
    _entry_apikey = None

    _message_frame = None

    _host = 'https://{spacename}.backlog.jp'

    _settings_dic = None
    _label_result_count = None
    _label_result_count_strvar = None
    _treeview_result = None

    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.master = master
        self.title = title
        self.pack()
        self.application_settings()
        self.read_settings_file()
        self.call_widgets()

    def application_settings(self):
        # アプリヘッダにタイトルを表示
        self.master.title(self.title)
        # アプリ全体のフォントサイズを指定
        self.master.option_add('*font', font.Font(size=10))

    def read_settings_file(self):
        controller = SettingsFileController()
        self._settings_dic = controller.readSettings()

    # master上に各フレームを配置
    def call_widgets(self):
        self.create_header()
        self.create_setting()
        self.create_button()
        self.create_error_msg()
        self.create_result()

    # ----------
    # 以下は、各パーツの設定

    def create_header(self):
        header_frame = tk.Frame(self.master)
        header_frame.pack(anchor=tk.W, padx=2)

        # アプリタイトルのフォント設定
        font_title = font.Font(size=14, weight='bold', underline=1)
        label_title = tk.Label(
            header_frame,
            text=self.title,
            font=font_title
        )
        label_title.pack(side='top', anchor=tk.W)

    def create_setting(self):
        setting_frame = tk.Frame(self.master)
        setting_frame.pack(anchor=tk.W, padx=2, pady=5)

        area_title = tk.Label(setting_frame, text=u'◆設定◆')
        area_title.pack(anchor=tk.W)

        # 入力欄エリア
        inputarea_frame = tk.Frame(setting_frame)
        inputarea_frame.pack(anchor=tk.W)

        ## スペース名入力エリア
        target_spacename_frame = tk.Frame(inputarea_frame)
        target_spacename_frame.pack(anchor=tk.W, padx=10, pady=2)

        label_spacename = tk.Label(target_spacename_frame, text=u'対象スペース名：')
        self._entry_spacename = tk.Entry(target_spacename_frame, width=20)
        label_spacename.pack(side='left')
        self._entry_spacename.pack(side='left')
        if (self._settings_dic != None):
            self._entry_spacename.insert(
                tk.END, 
                self._settings_dic.get('spacename')
            )

        ## 対象PJID入力エリア
        target_pj_inputarea_frame = tk.Frame(inputarea_frame)
        target_pj_inputarea_frame.pack(anchor=tk.W, padx=10, pady=2)

        label_target_pj = tk.Label(target_pj_inputarea_frame, text=u'対象PJID：')
        self._entry_target_pj = tk.Entry(target_pj_inputarea_frame, width=10)
        label_target_pj.pack(side='left')
        self._entry_target_pj.pack(side='left')
        if (self._settings_dic != None):
            self._entry_target_pj.insert(
                tk.END, 
                self._settings_dic.get('target_pj')
            )

        ## APIKey入力エリア
        apikey_inputarea_frame = tk.Frame(inputarea_frame)
        apikey_inputarea_frame.pack(anchor=tk.W, padx=10, pady=2)

        label_apikey = tk.Label(apikey_inputarea_frame, text=u'API Key：')
        label_apikey.pack(side='left')
        self._entry_apikey = tk.Entry(apikey_inputarea_frame, width=40)
        self._entry_apikey.pack(side='left')
        if (self._settings_dic != None):
            self._entry_apikey.insert(
                tk.END, 
                self._settings_dic.get('apikey')
            )

    def create_button(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(fill='x', padx=2, pady=5)
        # ボタン配置
        button_search = tk.Button(
            button_frame, text=u'検索', bg='#D4E6F1',
            command=self._command_search
        )
        button_search.pack(side='left', padx=10)

        button_exit = tk.Button(
            button_frame, text=u'終了', bg='#ABB2B9',
            command=self._command_exit
        )
        button_exit.pack(side='right', padx=10)

    def create_error_msg(self):
        self._message_frame = tk.Frame(self.master)
        self._message_frame.pack(anchor=tk.W, padx=2, pady=5)

    def create_result(self):
        result_frame = tk.Frame(self.master)
        result_frame.pack(anchor=tk.W, padx=2, pady=5)

        area_title = tk.Label(result_frame, text=u'◆検索結果◆　※一覧表示条件50件')
        area_title.pack(anchor=tk.W)

        self._label_result_count_strvar = tk.StringVar()
        self._label_result_count_strvar.set(u'合計：')
        self._label_result_count = tk.Label(result_frame, textvariable=self._label_result_count_strvar)
        self._label_result_count.pack(anchor=tk.W)

        # 検索結果テーブル
        treeview_frame = tk.Frame(result_frame)
        treeview_frame.pack(anchor=tk.W)
        self._treeview_result = ttk.Treeview(treeview_frame, height=20)
        self._treeview_result['columns'] = (1,2,3,4,5,6)
        self._treeview_result['show'] = 'headings'
        self._treeview_result.column(1, width=30)
        self._treeview_result.column(2, width=140)
        self._treeview_result.column(3, width=580)
        self._treeview_result.column(4, width=80)
        self._treeview_result.column(5, width=120)
        self._treeview_result.column(6, width=120)
        self._treeview_result.heading(1, text=u'No')
        self._treeview_result.heading(2, text=u'チケット番号')
        self._treeview_result.heading(3, text=u'タイトル')
        self._treeview_result.heading(4, text=u'期限')
        self._treeview_result.heading(5, text=u'担当者')
        self._treeview_result.heading(6, text=u'作成者')
        self._treeview_result.pack()

        # 縦スクロールバー
        yscrollbar = tk.Scrollbar(treeview_frame, orient= tk.VERTICAL, command= self._treeview_result.yview)
        yscrollbar.place(relheight=0.95,relx=0.99,rely=0.05)
        self._treeview_result.configure(yscroll= yscrollbar.set)


    # ----------
    # 以下は、各パーツの動作
    def _command_exit(self):
        self.master.quit()


    def _command_search(self):
        self._destroy_error_msgs()
        self._treeview_result.delete(*self._treeview_result.get_children())
        if(self._check_entry()):
            # 入力エラーなし
            self._save_settings()
            self._get_issues()
        else:
            # 入力エラーあり
            pass

    def _destroy_error_msgs(self):
        children = self._message_frame.winfo_children()
        for child in children:
            child.destroy()

    def _check_entry(self):
        error_msgs = []

        # 入力チェック
        trimed_spacename = self._entry_spacename.get().strip()
        if(len(trimed_spacename) == 0):
            error_msgs.append(u'対象スペース名が未入力')

        trimed_target_pj = self._entry_target_pj.get().strip()
        if(len(trimed_target_pj) == 0):
            error_msgs.append(u'対象PJIDが未入力')

        trimed_apikey = self._entry_apikey.get().strip()
        if(len(trimed_apikey) == 0):
            error_msgs.append(u'ApiKeyが未入力')

        for error_msg in error_msgs:
            label_msg = tk.Label(
                self._message_frame,
                text=u'・' + error_msg,
                fg='#E91E63'
            )
            label_msg.pack(anchor=tk.W)

        result_flag = tk.BooleanVar()
        if(len(error_msgs) == 0):
            # 入力エラーなし
            result_flag.set(True)
        else:
            # 入力エラーあり
            result_flag.set(False)

        return result_flag.get()

    def _save_settings(self):
        trimed_spacename = self._entry_spacename.get().strip()
        trimed_target_pj = self._entry_target_pj.get().strip()
        trimed_apikey = self._entry_apikey.get().strip()

        self._settings_dic['spacename'] = trimed_spacename
        self._settings_dic['target_pj'] = trimed_target_pj
        self._settings_dic['apikey'] = trimed_apikey

        controller = SettingsFileController()
        controller.writeSettings(self._settings_dic)

    def _get_issues(self):
        trimed_spacename = self._entry_spacename.get().strip()
        trimed_target_pj = self._entry_target_pj.get().strip()
        trimed_apikey = self._entry_apikey.get().strip()

        response_issues = self._get_issues_apikey(
            spacename=trimed_spacename, 
            pjid=trimed_target_pj, 
            apikey=trimed_apikey
        )

        results_issues = response_issues.json()
        if (response_issues.status_code == 200):
            response_count = self._get_count_apikey(
                spacename=trimed_spacename, 
                pjid=trimed_target_pj, 
                apikey=trimed_apikey
            )
            result_count = response_count.json().get('count')
            result_count_label = u'合計： {result_count}'
            self._label_result_count_strvar.set(result_count_label.format(result_count=result_count))

            # 結果を表形式で表示する
            for index, result in enumerate(results_issues):
                self._treeview_result.insert('', 0,
                    values=(
                        result_count - index,
                        result['issueKey'],
                        result['summary'],
                        result['dueDate'][0:10],
                        result['assignee']['name'],
                        result['createdUser']['name']
                    )
                )
            pass
        else:
            self._destroy_error_msgs()

            errors = results_issues.get('errors')
            for error in errors:
                label_msg = tk.Label(
                    self._message_frame,
                    text=u'・' + error.get('message'),
                    fg='#E91E63'
                )
                label_msg.pack(anchor=tk.W)
            pass


    def _get_count_apikey(self, spacename=None, pjid=None, apikey=None):
        url_count = '/api/v2/issues/count'

        today = datetime.date.today()

        params = {
            'apiKey' : apikey,
            'projectId[]' : pjid,
            'statusId[]' : [1,2,3], # 完了以外
            'dueDateUntil' : today,
            'sort' : 'dueDate',
        }
        host = self._host.format(spacename=spacename)

        headers = {
            'Content-Type': 'application/json'
        }
        response_count = requests.get(host + url_count, params=params, headers=headers)
        return response_count


    def _get_issues_apikey(self, spacename=None, pjid=None, apikey=None):
        url_issues = '/api/v2/issues'

        today = datetime.date.today()

        params = {
            'apiKey' : apikey,
            'projectId[]' : pjid,
            'statusId[]' : [1,2,3], # 完了以外
            'dueDateUntil' : today,
            'sort' : 'dueDate',
            'count' : 50
        }
        host = self._host.format(spacename=spacename)

        headers = {
            'Content-Type': 'application/json'
        }
        response_issues = requests.get(host + url_issues, params=params, headers=headers)
        return response_issues




root = tk.Tk()
root.geometry('1080x720')
app = Application(master=root, title=u'Backlog期限切れチケット抽出ツール')
app.mainloop()
