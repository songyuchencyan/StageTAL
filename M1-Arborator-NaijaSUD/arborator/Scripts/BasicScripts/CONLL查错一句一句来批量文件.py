#!/usr/bin/env python  
# # -*- coding: utf-8 -*-
import re
import sqlite3  


##### Get dictionnary #####
txt=open('Lexiquepourcorrection_new.txt','r')
lexique=[]
sss=0
while 1:
    line_lexi_s = txt.readline()
    line_lexi_n = line_lexi_s.replace(" \n","")
    line_lexi = line_lexi_n.replace("\n","")
    if line_lexi != "":
        list_line_lexi = line_lexi.split('\t')
        list_lexi=[]
        list_lexi.append(list_line_lexi[0])
        list_lexi.append(list_line_lexi[1])
        a=list_line_lexi[2]
        if "|" in a:
            b=a.split("|")
            c=sorted(b)
            d="|".join(c)
            list_lexi.append(d)
        else:
            list_lexi.append(list_line_lexi[2])
        lexique.append(list_lexi)
    else:
        break
token=[x for [x,y,z] in lexique]
token_categorie=[[x,y] for [x,y,z] in lexique]



##### 读取目录里的文件 #####
import os
folder_path = "E:/TAL/Stage/arborator/projects/NaijaSUD/export/newest_conll10"
file_list = os.listdir(folder_path)
#print(file_list)
for files in file_list:
    f = open("E:/TAL/Stage/arborator/projects/NaijaSUD/export/newest_conll10/"+files,"r")

    #############################################################################
    ''' Find textname and textid'''
    text_name = str(f)
    text_name = text_name.replace("<_io.TextIOWrapper name='./test/","") 
    text_name = text_name.replace("' mode='r' encoding='cp65001'>","") 
    text_name = str(text_name.replace(".most.recent.trees.conll10",""))
    text_name = str(text_name.replace(".most.recent.trees.with.feats.conllu",""))
    text_name = str(text_name.replace(".most.recent.trees.with.feats.conllu_reordered",""))
    textnameid = re.findall("P_.+\d+_",text_name)
    textnameid = str(textnameid[0])+"%" # %为sql中的通配符

    import sqlite3  
    conn = sqlite3.connect("arborator.db.sqlite")  
    c = conn.cursor() 
    cursor = c.execute('''SELECT rowid,textname FROM texts WHERE textname LIKE "{}"'''.format(textnameid))    
    for row in cursor:
        textid = str(row[0])
        textname = str(row[1])
    conn.close()
    print(textname,textid)
    #############################################################################



    ##### start correction #####
    w=open("E:/TAL/Stage/arborator/projects/NaijaSUD/export/Correction/"+textname+".conll","a")
    cat = open("cat_erreur.txt","a")
    faute_mot=open("mot_manque.txt",'a')
    cat.write("\n\n\n" + "#" + textname + "\n\n")
    faute_mot.write("\n\n\n" + "#" + textname + "\n\n")
    phrase=""
    for chaque_ligne in f:
        if chaque_ligne != "\n":
            phrase = phrase + chaque_ligne
        else:
            ##### find sent_id #####
            sent_id = re.findall("sent_id.+PRO_(\d+)",phrase)
            sent_id = "".join(sent_id)
            ##### find sent_id #####
            f1 = open("test.txt","w")
            f1.write(phrase)
            f1.close() # 必须要关上，不然紧接着f2读不出来或者会错位。
            phrase = ""
            f2 = open("test.txt","r")
            while 1:
                line=f2.readline()
                if line != "":
                    if line[0]=="#" or line[0]=="\n":
                        w.write(line)
                    elif line[0] != "#" and line != "\n":
                        list_line = line.split()
                        upper = list_line[1].upper()
                        title = list_line[1].title()
                        if list_line[1] in token:
                            if [list_line[1],list_line[3]] in token_categorie:
                                r=list_line[5]
                                if "|" in r:
                                    m=r.split("|")
                                    l=sorted(m)
                                    o="|".join(l)
                                if [list_line[1],list_line[3],list_line[5]] in lexique or [list_line[1],list_line[3],list_line[5]] in lexique :
                                    w.write(line)
                                else:
                                    for liste in lexique:
                                        if list_line[1]==liste[0] and list_line[3]==liste[1]:
                                            list_line[5]=liste[2]
                                            list_line_ch="\t".join(list_line)
                                    w.write(list_line_ch)    
                                    w.write("\n")            
                            else:
                                faute_cat=open("cat_à_vérifier.txt",'a')
                                fautes_cat=list_line[1] + "\t" + list_line[3] + "\t" + list_line[5] + "\n"
                                fauteread_cat=open("cat_à_vérifier.txt",'r')
                                fautereadd_cat=fauteread_cat.readlines()
                                if fautes_cat in fautereadd_cat :
                                    pass
                                else :
                                    faute_cat.write(fautes_cat) 
                                cat_double = []
                                for liste in lexique:
                                    if list_line[1]==liste[0]:
                                        cat_double.append(liste)
                                if len(cat_double) == 1:
                                    list_line[3]=cat_double[0][1]
                                    list_line[5]=cat_double[0][2]
                                    list_line_ch="\t".join(list_line)
                                    w.write(list_line_ch)
                                    w.write("\n")   
                                else:
                                    sent_idid = sent_id
                                    link = "https://arborator.ilpga.fr/editor.cgi?project=NaijaSUD&textid="+textid+"&opensentence="+sent_idid
                                    cat.write(str(link))
                                    cat.write("\n")
                                    cat.write(str(cat_double) + "\n")
                                    cat.write(line + " ne sait pas correspondre à laquelle\n\n\n")
                                    w.write(line)
                        elif upper in token:
                            for liste in lexique:
                                if upper==liste[0]:
                                    list_line[1]=liste[0]
                                    list_line[3]=liste[1]
                                    list_line[5]=liste[2]
                                    list_line_ch="\t".join(list_line)
                                    w.write(list_line_ch)
                                    w.write("\n")
                        elif title in token:
                            for liste in lexique:
                                if title==liste[0]:
                                    list_line[1]=liste[0]
                                    list_line[3]=liste[1]
                                    list_line[5]=liste[2]
                                    list_line_ch="\t".join(list_line)
                                    w.write(list_line_ch)
                                    w.write("\n")
                        # elif list_line[1]=="anoder":
                        #     list_line[1]="anoda"
                        #     list_line[3]="DET"
                        #     list_line[5]="_"
                        #     list_line_ch="\t".join(list_line)
                        #     print(list_line_ch)
                        #     w.write(list_line_ch)
                        #     w.write("\n")
                        else:
                            print(list_line,"mot pas dans lexique")
                            w.write(line)
                            faute=open("mot_manque.txt",'a')
                            fautes=list_line[1] + "\t" + list_line[3] + "\t" + list_line[5] + "\n"
                            fauteread=open("mot_manque.txt",'r')
                            fautereadd=fauteread.readlines()
                            if fautes in fautereadd :
                                pass
                            else :
                                faute.write(fautes) 
                else:
                    break
            w.write("\n")