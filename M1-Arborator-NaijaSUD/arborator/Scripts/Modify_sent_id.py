import sqlite3  
conn = sqlite3.connect("arborator.db.sqlite")  
c = conn.cursor() 
cursor = c.execute("SELECT rowid,nr,sentence,textid FROM sentences WHERE not EXISTS( SELECT sentenceid FROM sentencefeatures WHERE sentencefeatures.sentenceid=sentences.rowid)")
#插入rowid不在sent_id的句子 Inserer les phrases de 'sentences' dont le rowid n'est pas dans 'sentencefeatures'
for row in cursor:
    c = conn.cursor() #必须每次都重新连一次
    sentenceid = row[0]
    sent_id = row[1]
    texte = row[2]
    textid = row[3]
    c.execute("INSERT INTO sentencefeatures VALUES (?,?,?)",(sentenceid,"text",texte))
    c.execute("INSERT INTO sentencefeatures VALUES (?,?,?)",(sentenceid,"sent_id",sent_id))
#重命名sent_id  renommer sent_id
c.execute("""update sentencefeatures
set value=
(select texts.textname from texts where texts.rowid=(select sentences.textid from sentences where sentences.rowid=sentencefeatures.sentenceid) )
||
"_"
||
(select sentences.nr from sentences where sentences.rowid=sentencefeatures.sentenceid)
where attr="sent_id"
and sentencefeatures.sentenceid in (select rowid from sentences);""")
#nettoyer du sent_id, supprimer '_TRANS.eaf.csv' et '.eaf.csv'
#删除sent_id中的"_TRANS.eaf.csv"
c.execute("""update sentencefeatures 
    set value=replace(value,"_TRANS.eaf.csv","") 
    where attr="sent_id";""")
#删除sent_id中的".eaf.csv"(主要在以PRO结尾的文件)
c.execute("""update sentencefeatures 
    set value=replace(value,".eaf.csv","") 
    where attr="sent_id";""")
conn.commit()
conn.close() 
