import sqlite3  
print("进行中。。。请耐心等待谢谢")
conn = sqlite3.connect("arborator.db.sqlite")  
c = conn.cursor() 
# c.execute('''UPDATE features SET value="_" WHERE attr="misc"''')    #更改misc的value
c.execute('''DELETE FROM features WHERE attr = "misc"''')    #删除misc条目
c.execute('''DELETE FROM features WHERE attr = "xpos"''')    #删除misc条目
conn.commit()
conn.close()
print("本次操作已完成，感谢您的使用！")



