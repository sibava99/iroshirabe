#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

#色差計算用のモジュールをインポート
from skimage import color
import numpy as np

# データベースファイルのパスを設定
dbname = 'colors_name.db'
#dbname = ':memory:'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists color_table(name text,hurigana text,code text,R int,G int,B int,counter int)'
cur.execute(create_table)
con.commit()
cur.close()
con.close()

def ciede2000(code,rgbtable):
	#カラーコードをrgb形式にした後lab形式に変換する
	piclab = color.rgb2lab((np.array([int(code[1:3],16),int(code[3:5],16),int(code[5:7],16)],np.int8)).reshape(1,1,3))
	#ciede2000のスコアの最低値を記録
	print(piclab)
	minimum = 1e10
	min_code = '#000000'
	for row in rgbtable:
		rlab = color.rgb2lab((np.array([row[1],row[2],row[3]],np.int8)).reshape(1,1,3))
		delta = color.deltaE_ciede2000(piclab,rlab)
		if (delta < minimum):
			minimum = delta
			min_code = row[0]
			print(minimum,min_code)
	return min_code
			
			

def application(environ,start_response):
	# HTML（共通ヘッダ部分）
	css = ((open('wacolor.css')).read())
	html = '<html lang="ja">\n' \
		   '<head>\n' \
		   '<meta charset="UTF-8">\n' \
		   '<title>和色検索</title>\n' \
		   '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300&display=swap" rel="stylesheet">\n' \
		   '<link href="https://fonts.googleapis.com/earlyaccess/hannari.css" rel="stylesheet">\n' \
		  '<style>'+ str(css) + '</style>\n' \
		   '</head>\n'

	# フォームデータを取得
	form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
	if ('v1' not in form):
		# 入力フォームの内容が空の場合（初めてページを開いた場合も含む）
		con = sqlite3.connect(dbname)
		cur = con.cursor()
		con.text_factory = str
		sql = 'select * from color_table where counter >= 1 order by counter desc '
		print(sql)
		# HTML（入力フォーム部分）
		html += '<body>\n' \
				'<div class="top_wrap">\n' \
				'<div class="title">いろしらべ</div>\n' \
				'<form>\n' \
				'色 <input type="color" name="v1">\n' \
				'<input type="submit" value="登録">\n' \
				'</form>\n'\
				'<div class="explain">このサイトはカラーピッカーにより指定された色に最も近い日本の伝統色を713色のデータベースの中から検索します</div>\n' \
				'<ol>'
		
		for row in cur.execute(sql):
			html += '<li style = "background-color: ' + str(row[2]) + ';">' + str(row) + '</li>\n'	
		
		html += '</ol>\n'\
			'</div>\n' \
			'</body>\n'
		cur.close()
		con.close
	else:
		# 入力フォームの内容が空でない場合

		# フォームデータから各フィールド値を取得
		v1 = form.getvalue("v1", "0")

		# データベース接続とカーソル生成
		con = sqlite3.connect(dbname)
		cur = con.cursor()
		con.text_factory = str

		# SQL文（insert）の作成と実行
		# sql = 'insert into users (id, name) values (?,?)'
		# cur.execute(sql, (int(v1),v2))
		# con.commit()

		# SQL文（select）の作成
		sql = 'select code,R,G,B from color_table'
		ret_color = ciede2000(v1,cur.execute(sql))
		cur.execute( 'select * from color_table where code = ?' ,(ret_color,))
		cinf = cur.fetchone()
		cur.execute('update color_table set counter = counter + 1 where code = ?',(ret_color,))
		con.commit()
		# SQL文の実行とその結果のHTML形式への変換
		html += '<body>\n' \
			'<div class="container">\n'
		html += '<div class="text">\n'
		html += '<p class="kanji">' + str(cinf[0]) + '</p>\n'
		html += '<p class="hurigana">' + str(cinf[1]) + '</p>\n'
		html += '<p class="rgb">' + str(cinf[2]) + '</p>\n'
		html += '</div>\n'
		html += '<div class="color" style="background-color: ' + str(ret_color) +';">' + str(ret_color) + '</div>\n'
		html += '</div>\n'\
			'<cent><a href="/">戻る</a></cent>\n'\
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
