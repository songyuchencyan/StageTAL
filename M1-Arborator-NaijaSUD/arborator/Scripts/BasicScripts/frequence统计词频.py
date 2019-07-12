#!/usr/bin/env python  
# -*- coding: UTF-8 -*-  
import os
folder_path = "E:/TAL/Stage/arborator/projects/NaijaSUD/export/Correction/P_PRO_Corrigés"
file_list = os.listdir(folder_path)
#print(file_list)
for files in file_list:
    filename = files.replace("CORRIGER_","")
    filename = filename.replace(".most.recent.trees.with.feats.conllu_reordered","")
    mots_liste = []
    f = open("./Correction/P_PRO_Corrigés/"+files,"r")
    for ligne in f:
        if "# elan_id = " not in ligne and "# sent_id =" not in ligne and "# sent_translation =" not in ligne and "# text =" not in ligne and ligne != "\n" and ligne != "":
            terme = ligne.split("\t")
            if len(terme) >= 2:
                mots_liste.append(terme[1])
    fre_dic = {}
    for ele in set(mots_liste):
        fre_dic[ele] = mots_liste.count(ele)
    fre_dic_sort = sorted(fre_dic.items(),key = lambda x:x[1],reverse = True)
    w = open("E:/TAL/Stage/arborator/projects/NaijaSUD/export/Frequence/"+filename+".txt","w")
    nb_mot = len(set(mots_liste))
    w.write("nombre de mots distincts : " + str(nb_mot) + "\n")
    for mot in fre_dic_sort:
        w.write(str(mot[0])+"\t"+str(mot[1])+"\n")