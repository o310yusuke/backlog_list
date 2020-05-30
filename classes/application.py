# coding: utf-8

import tkinter as tk
from tkinter import font
from tkinter import ttk

class Application(tk.Frame):
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
        self.create_result()

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

        label_target_pj = tk.Label(setting_frame, text=u'対象PJID：')
        entry_target_pj = tk.Entry(setting_frame, width=10)
        # label_target_pj.pack(side='left')
        label_target_pj.pack()
        entry_target_pj.pack()

        label_connecting_way = tk.Label(setting_frame, text=u'接続方法：')
        label_connecting_way.pack()

        # APIKeyパターン
        checkbox_apikey = tk.Checkbutton(
            setting_frame, text=u'API Key', command=None
        )
        checkbox_apikey.pack(anchor=tk.W)
        # labelframe_apikey = tk.LabelFrame(setting_frame, labelwidget=checkbox_apikey)
        # labelframe_apikey.pack(anchor=tk.W)
        entry_apikey = tk.Entry(setting_frame, width=20)
        entry_apikey.pack(anchor=tk.W)

        # ID/PWパターン
        checkbox_idpw = tk.Checkbutton(
            setting_frame, text=u'ID/PW', command=None
        )
        checkbox_idpw.pack(anchor=tk.W)
        label_id = tk.Label(setting_frame, text=u'ID：')
        entry_id = tk.Entry(setting_frame, width=10)
        label_pw = tk.Label(setting_frame, text=u'PW：')
        entry_pw = tk.Entry(setting_frame, width=20)
        label_id.pack()
        entry_id.pack()
        label_pw.pack()
        entry_pw.pack()

        # ボタン配置
        button_search = tk.Button(text=u'検索', command=None)
        button_search.pack()

        button_exit = tk.Button(text=u'終了', command=None)
        button_exit.pack()

    def create_result(self):
        result_frame = tk.Frame(self.master)
        result_frame.pack(anchor=tk.W, padx=2, pady=5)

        area_title = tk.Label(result_frame, text=u'◆検索結果◆')
        area_title.pack(anchor=tk.W)

        label_result_count = tk.Label(result_frame, text=u'合計：' + u'件')
        label_result_count.pack()

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




root = tk.Tk()
root.geometry('500x500')
app = Application(master=root, title=u'Backlog期限切れチケット抽出ツール')
app.mainloop()
