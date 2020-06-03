# coding: utf-8

import datetime
import tkinter as tk
from tkinter import font, ttk

import requests

class Application(tk.Frame):
    # プライベート変数
    _flag_apike = None
    _flag_idpw = None

    _checkbox_apikey = None
    _checkbox_idpw = None

    _entry_target_pj = None
    _entry_apikey = None
    _entry_id = None
    _entry_pw = None

    _message_frame = None

    _host = 'https://xxxxxxxxxx.backlog.jp'

    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.master = master
        self.title = title
        self.pack()
        self.application_settings()
        self.call_widgets()

    def application_settings(self):
        # アプリヘッダにタイトルを表示
        self.master.title(self.title)
        # アプリ全体のフォントサイズを指定
        self.master.option_add('*font', font.Font(size=10))

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

        ## 対象PJID入力エリア
        target_pj_inputarea_frame = tk.Frame(inputarea_frame)
        target_pj_inputarea_frame.pack(anchor=tk.W)

        label_target_pj = tk.Label(target_pj_inputarea_frame, text=u'対象PJID：')
        self._entry_target_pj = tk.Entry(target_pj_inputarea_frame, width=10)
        label_target_pj.pack(side='left')
        self._entry_target_pj.pack(side='left')

        ## 接続方法エリア
        connecting_way_frame = tk.Frame(inputarea_frame)
        connecting_way_frame.pack(anchor=tk.W)
        label_connecting_way = tk.Label(connecting_way_frame, text=u'接続方法：')
        label_connecting_way.pack(side='left', anchor=tk.NW)

        ### 接続方法入力エリア
        connecting_way_inputarea_frame = tk.Frame(connecting_way_frame)
        connecting_way_inputarea_frame.pack(side='left', padx=5)

        #### APIKey入力エリア
        ##### APIKeyパターン
        apikey_inputarea_labelframe = tk.LabelFrame(
            connecting_way_inputarea_frame,
            text=u'apikey',
            padx=10, pady=10,
        )
        self._flag_apike = tk.BooleanVar()
        self._checkbox_apikey = tk.Checkbutton(
            apikey_inputarea_labelframe, 
            text=u'API Key', var=self._flag_apike,
            command=self._command_checkbutton
        )
        apikey_inputarea_labelframe['labelwidget'] = self._checkbox_apikey
        apikey_inputarea_labelframe.pack(anchor=tk.W)

        label_apikey = tk.Label(apikey_inputarea_labelframe, text=u'API Key：')
        label_apikey.pack(side='left')
        self._entry_apikey = tk.Entry(apikey_inputarea_labelframe, width=40)
        self._entry_apikey.pack(side='left')

        #### ID/PW入力エリア
        ##### ID/PWパターン
        idpw_inputarea_labelframe = tk.LabelFrame(
            connecting_way_inputarea_frame,
            text=u'id/pw',
            padx=10, pady=10,
        )
        self._flag_idpw = tk.BooleanVar()
        self._checkbox_idpw = tk.Checkbutton(
            idpw_inputarea_labelframe,
            text=u'ID/PW', var=self._flag_idpw,
            command=self._command_checkbutton
        )
        idpw_inputarea_labelframe['labelwidget'] = self._checkbox_idpw
        idpw_inputarea_labelframe.pack(anchor=tk.W)

        label_id = tk.Label(idpw_inputarea_labelframe, text=u'ID：')
        self._entry_id = tk.Entry(idpw_inputarea_labelframe, width=20)
        label_pw = tk.Label(idpw_inputarea_labelframe, text=u'PW：')
        self._entry_pw = tk.Entry(idpw_inputarea_labelframe, width=20)
        label_id.pack(side='left')
        self._entry_id.pack(side='left')
        label_pw.pack(side='left')
        self._entry_pw.pack(side='left')

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

        area_title = tk.Label(result_frame, text=u'◆検索結果◆')
        area_title.pack(anchor=tk.W)

        label_result_count = tk.Label(result_frame, text=u'合計：' + u'件')
        label_result_count.pack(anchor=tk.W)

        # 検索結果テーブル
        treeview_result = ttk.Treeview(result_frame)
        treeview_result['columns'] = (1,2,3,4,5)
        treeview_result['show'] = 'headings'
        treeview_result.heading(1, text=u'チケット番号')
        treeview_result.heading(2, text=u'タイトル')
        treeview_result.heading(3, text=u'期限')
        treeview_result.heading(4, text=u'担当者')
        treeview_result.heading(5, text=u'作成者')

        treeview_result.pack()

        # test data
        treeview_result.insert('', 'end', 
            values=('PJ-NAME_0001', '【インフラ】テスト環境構築', '2020/04/05', '太郎', '花子')
        )

    # ----------
    # 以下は、各パーツの動作
    def _command_exit(self):
        self.master.quit()

    def _toggle_apikey_normal(self):
        # apikey選択状態なので、apikeyを活性化
        self._entry_apikey.configure(state='normal')
        self._checkbox_apikey.configure(state='normal')

    def _toggle_apikey_disabled(self):
        # apiley非選択状態なので、apikeyを非活性
        self._entry_apikey.configure(state='disabled')
        self._checkbox_apikey.configure(state='disabled')

    def _toggle_idpw_normal(self):
        self._entry_id.configure(state='normal')
        self._entry_pw.configure(state='normal')
        self._checkbox_idpw.configure(state='normal')

    def _toggle_idpw_disabled(self):
        self._entry_id.configure(state='disabled')
        self._entry_pw.configure(state='disabled')
        self._checkbox_idpw.configure(state='disabled')

    def _command_checkbutton(self):
        if(self._flag_apike.get() == False and self._flag_idpw.get() == False):
            self._toggle_apikey_normal()
            self._toggle_idpw_normal()
        elif(self._flag_apike.get() == True and self._flag_idpw.get() == False):
            self._toggle_apikey_normal()
            self._toggle_idpw_disabled()
        elif(self._flag_apike.get() == False and self._flag_idpw.get() == True):
            self._toggle_apikey_disabled()
            self._toggle_idpw_normal()
        elif(self._flag_apike.get() == True and self._flag_idpw.get() == True):
            print(u'想定外のエラーが発生')
        else:
            print(u'発生するはずのない条件分岐')

    def _command_search(self):
        self._destroy_error_msgs()
        if(self._check_entry()):
            # 入力エラーなし
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
        trimed_target_pj = self._entry_target_pj.get().strip()
        if(len(trimed_target_pj) == 0):
            error_msgs.append(u'対象PJIDが未入力')

        if(self._flag_apike.get() == True and self._flag_idpw.get() == False):
            # API
            trimed_apikey = self._entry_apikey.get().strip()
            if(len(trimed_apikey) == 0):
                error_msgs.append(u'ApiKeyが未入力')
        elif(self._flag_apike.get() == False and self._flag_idpw.get() == True):
            # ID/PW
            trimed_id = self._entry_id.get().strip()
            if(len(trimed_id) == 0):
                error_msgs.append(u'IDが未入力')

            trimed_pw = self._entry_pw.get().strip()
            if(len(trimed_pw) == 0):
                error_msgs.append(u'PWが未入力')
        elif(self._flag_apike.get() == False and self._flag_idpw.get() == False):
            error_msgs.append(u'接続方法が未選択')
        else:
            error_msgs.append(u'想定外のエラーが発生')

        for error_msg in error_msgs:
            label_msg = tk.Label(
                self._message_frame,
                text=u'・' + error_msg,
                fg='#E91E63'
            )
            label_msg.pack()

        result_flag = tk.BooleanVar()
        if(len(error_msgs) == 0):
            # 入力エラーなし
            result_flag.set(True)
        else:
            # 入力エラーあり
            result_flag.set(False)

        return result_flag.get()

    def _get_issues(self):
        trimed_target_pj = self._entry_target_pj.get().strip()

        results = []
        if(self._flag_apike.get() == True and self._flag_idpw.get() == False):
            # APIKey選択時
            trimed_apikey = self._entry_apikey.get().strip()
            results = self._get_issues_apikey(pjid=trimed_target_pj, apikey=trimed_apikey)
        elif(self._flag_apike.get() == False and self._flag_idpw.get() == True):
            # ID/PW選択時
            trimed_id = self._entry_id.get().strip()
            trimed_pw = self._entry_pw.get().strip()
            results = self._get_issues_idpw(pjid=trimed_target_pj, id=trimed_id, pw=trimed_pw)
        else:
            print(u'想定外のエラー')

        # 結果を表形式で表示する
        for index, result in enumerate(results):
            print('◆ ' + str(index+1) + '件目')
            print(result['issueKey'] + '：' + result['summary'])
            print('担当者：' + result['assignee']['name'] + '/ 作成者：' + result['createdUser']['name'])
            print('対応期限：' + result['dueDate'])
            print('----------------------------------------')
        pass

    def _get_count_apikey(self, pjid=None, apikey=None):
        url_count = '/api/v2/issues/count'

        today = datetime.date.today()

        params = {
            'apiKey' : apikey,
            'projectId[]' : pjid,
            'statusId[]' : [1,2,3], # 完了以外
            'dueDateUntil' : today,
            'sort' : 'dueDate',
        }

        response_count = requests.get(self._host + url_count, params=params)
        return response_count.json()


    def _get_issues_apikey(self, pjid=None, apikey=None):
        url_issues = '/api/v2/issues'

        today = datetime.date.today()

        params = {
            'apiKey' : apikey,
            'projectId[]' : pjid,
            'statusId[]' : [1,2,3], # 完了以外
            'dueDateUntil' : today,
            'sort' : 'dueDate',
        }

        response_issues = requests.get(self._host + url_issues, params=params)
        return response_issues.json()

    def _get_issues_idpw(self, pjid=None, id=None, pw=None):
        return 'idpw'



root = tk.Tk()
root.geometry('1080x680')
app = Application(master=root, title=u'Backlog期限切れチケット抽出ツール')
app.mainloop()
