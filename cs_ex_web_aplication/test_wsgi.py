#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
dbname = 'database.db'
#dbname = ':memory:'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists users (id int, name varchar(64))'
cur.execute(create_table)
con.commit()
cur.close()
con.close()

def application(environ,start_response):
    # HTML（共通ヘッダ部分）
    html = '<html lang="ja">\n' \
           '<head>\n' \
           '<meta charset="UTF-8">\n' \
           '<title>WSGI テスト</title>\n' \
           '<link rel="stylesheet" href="default.css">\n' \
           '</head>\n'

    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
    if ('v1' not in form) or ('v2' not in form):
        # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）

        # HTML（入力フォーム部分）
        html += '<body>\n' \
                '<div class="form1">\n' \
                '<form>\n' \
                '学生番号（整数） <input type="text" name="v1"><br>\n' \
                '氏名　（文字列） <input type="text" name="v2"><br>\n' \
                '<input type="submit" value="登録">\n' \
                '</form>\n' \
                '</div>\n' \
                '</body>\n'
    else:
        # 入力フォームの内容が空でない場合

        # フォームデータから各フィールド値を取得
        v1 = form.getvalue("v1", "0")
        v2 = form.getvalue("v2", "0")

        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        # SQL文（insert）の作成と実行
        sql = 'insert into users (id, name) values (?,?)'
        cur.execute(sql, (int(v1),v2))
        con.commit()

        # SQL文（select）の作成
        sql = 'select * from users'

        # SQL文の実行とその結果のHTML形式への変換
        html += '<body>\n' \
                '<div class="ol1">\n' \
                '<ol>\n'
        for row in cur.execute(sql):
            html += '<li>' + str(row[0]) + ',' + row[1] + '</li>\n'
       	html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">登録ページに戻る</a>\n' \
                '</body>\n'

        # カーソルと接続を閉じる
        cur.close()
        con.close()


    html += '</html>\n'
    html = html.encode('utf-8')

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 test_wsgi.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 test_wsgi.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()
