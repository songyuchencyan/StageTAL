#!/usr/bin/env python  
# -*- coding: UTF-8 -*-  
import sqlite3  
print("进行中。。。可能要好几分钟呢哦，请耐心等待谢谢。")
conn = sqlite3.connect("arborator.db.sqlite")  
c = conn.cursor() 
cursor = c.execute("SELECT treeid, nr, attr, value FROM features")


for row in cursor:
    c = conn.cursor() #必须每次都重新连一次 il faut reconnecter lors de chaque boucle
    liste = list(row)
    if "misc" in liste and "|" in liste[3]: 
        ali = liste[3].split("|")
        start = str(ali[0])
        startali = 'startali'
        end = str(ali[1])
        endali = 'endali'
        treeid1 = int(liste[0])
        nr1 = int(liste[1])
        # print([treeid1,nr1,"startali",start])
        c.execute("INSERT INTO features VALUES (?,?,?,?)",(treeid1,nr1,startali,start))
        c.execute("INSERT INTO features VALUES (?,?,?,?)",(treeid1,nr1,endali,end))
    conn.commit()
conn.close()
print("本次操作已完成，感谢您的使用！")


 

