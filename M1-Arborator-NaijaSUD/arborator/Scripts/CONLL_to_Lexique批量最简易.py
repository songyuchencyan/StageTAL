#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import re
import os
import time
time_start=time.time()


##### 读取目录里的文件 Lire tous les fichiers du répertoire #####
# folder_path = "E:/TAL/Stage/arborator/projects/Scripts/test"  # 目标文件目录
# file_list = os.listdir(folder_path)
# 读取该目录里所有文件
liste_noms_fichiers = ["P_ABJ_GWA_03_Cost.of.living.in.Abuja_PRO.eaf.csv.most.recent.trees.conll10","P_ABJ_GWA_06_Ugo.lifestory_PRO.most.recent.trees.conll10"]
folder_path = "E:/TAL/Stage/arborator/projects/Scripts/test"
# for files in file_list:
for fichier in liste_noms_fichiers:
    fichier_conll = open(folder_path + "/" + fichier,"r")
    # Lire le fichier conll ligne par ligne
    for ligne in fichier_conll:
        if ligne[0]!="#" and ligne!="\n" and ligne!="":
            ligne = ligne.split("\t")
            mot = ligne[1]
            lemme = ligne[2]
            cat = ligne[3]
            trait = ligne[5]
            terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme + "\n"
            lexique = open("E:/TAL/Stage/arborator/projects/Scripts/Lexique.txt","a")
            voir_lexique = open("E:/TAL/Stage/arborator/projects/Scripts/Lexique.txt","r")
            contenu = voir_lexique.readlines()    
            if terme not in contenu:
                lexique.write(terme)
                lexique.close()




time_end=time.time()
print('totally cost',time_end-time_start)
            
        
