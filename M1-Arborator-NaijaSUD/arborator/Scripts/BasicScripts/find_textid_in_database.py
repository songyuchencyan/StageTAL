name = "P_ABJ_GWA_06_%"	# 通过特定格式开头的文件名开头查询rowid	
import sqlite3  
conn = sqlite3.connect("arborator.db.sq以lite")  
c = conn.cursor() 
cursor = c.execute('''SELECT rowid FROM texts WHERE textname LIKE "{}"'''.format(name))    # 在texts表中，rowid即为textid
for row in cursor:
    print(row[0])
conn.close()


