#!/usr/bin/env python  
# -*- coding: UTF-8 -*- 
"""
python 2 运行，py -2 文件.py
用途：通过比较NaijaSUD数据库中的conll文本 和 本地经过修改的conll文件，只向NaijaSUD数据库中添加修改过的句子，即在原句子上新增一个annotator，以yuchen命名。
"""

import sys
sys.path.append("E:/TAL/Stage/arborator")
import os
import re
import codecs, collections, re
from lib.conll import conll2tree
from lib.database import SQL
import sqlite3
from time import mktime, time, asctime, localtime
from lib.conll import conllFile2trees
try: 	import jellyfish
except: pass
def simpleEnterSentences(sql, trees, dbtextname, annotatorName, sentencefeatures={}):
	"""
	takes a list of trees (nodedics)
	puts them into the database
	if preserveSampleWithSameName: add _ to names to create new name of sample
	"""
	ti = time()
	db,cursor=sql.open()

	###### 获取textid ######
	textid = sql.enter(cursor, "texts",["textname"],(dbtextname,))
	print "textid",textid, 

	###### 获取userid ######
	userid = sql.enter(cursor, "users",["user"],(annotatorName,))
	sql.realname(annotatorName, cursor)
	if not userid:
		print "the user is not in the database"
		return
	
	for i,tree in enumerate(trees): # for every sentence
		#sentence=" ".join([tree[j].get("t","") for j in sorted(tree)])
		print sentence
		#cursor.execute("select rowid from sentences,texts  where nr=? and sentence=?;",
		sentenceid = sql.getUniqueId(cursor, "sentences", ["nr","sentence","textid"], [scounter,sentence,textid])
		print "found sentenceid",sentenceid
		if not sentenceid:
			sentenceid = sql.enter(cursor, "sentences",["nr","sentence","textid"],(scounter,sentence,textid,))
			#print "made sentenceid",sentenceid
		sql.enter(cursor, "sentencesearch",["nr","sentence","textid"],(scounter,sentence,textid,))
		if sentencefeatures == True:
			for a,v in tree.sentencefeatures.iteritems():
				sql.enter(cursor, "sentencefeatures",["sentenceid","attr","value"],(sentenceid,a,v,))
		elif sentencefeatures:	
			for a,v in sentencefeatures[i].iteritems():
				sql.enter(cursor, "sentencefeatures",["sentenceid","attr","value"],(sentenceid,a,v,))
		#print tree
		ws, sent, treeid = sql.enterTree(cursor, tree, sentenceid, userid)
		#print "ws, sent, treeid",ws, sent, treeid	
	db.commit()
	db.close()	
	print "entered",sql.getNumberTokensPerText(textid, recompute=True),"tokens"
	return textid



if __name__ == "__main__":
	dbpath = "E:/TAL/Stage/arborator/projects"
	sql = SQL("NaijaSUD")
	###### 读取改错文件夹文件 ######
	folder_path = "E:/TAL/Stage/arborator/projects/NaijaSUD/export/Correction/correction_newest"
	file_list = os.listdir(folder_path)
	for files in file_list:
		phrase = ""
		f = open("E:/TAL/Stage/arborator/projects/NaijaSUD/export/Correction/correction_newest/"+files,"r")
		###### 统一新旧文件名字 ######
		conll10 = str(files)
		conll10 = conll10.replace(".conll",".most.recent.trees.conll10")
		conll10 = conll10.replace("-",".")
		###### 通过统一后的新文件名（已改错）打开旧文件名（未改错）
		f_ori = open("E:/TAL/Stage/arborator/projects/NaijaSUD/export/newest_conll10/"+conll10,"r")
		contenu = ""
		for ligne in f_ori:
			contenu = contenu + ligne
		textename = files.replace(".conll","")
		for chaque_ligne in f:
				if chaque_ligne != "\n":
					phrase = phrase + chaque_ligne
				else:	
					if phrase not in contenu:	# 如果在已改错文件中的句子与旧文件不同，说明此句已修改，将会写入数据库
						sentence = re.findall("# text = (.+)\n",phrase)	# 通过# text = 获取句子文本
						sentence = str(sentence[0])
						scounter = re.findall("sent_id = P_.+PRO_(\d+)",phrase)
						scounter = int(scounter[0])	# 通过sent_id获取句子序号
						w = open("chaque_phrase.conll","w")
						w.write(phrase)
						w.close()
						trees = conllFile2trees("test.conll", encoding="utf-8")
						simpleEnterSentences(sql, trees, textename, "yuchen")
					phrase=""
		f.close()
		f_ori.close()  