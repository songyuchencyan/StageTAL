#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import re
import os
import time


def getlexique(listefichierconll,input_path,outfile_path,outfile=None,outfile_newwords=None,lexique_ori=False,lexique_newwords=False,combine=False):
    if lexique_ori:
        liste_lexique_ori = []
        lexique = open(outfile_path+"/"+outfile,"w")
        lexique.write('mot' + "\t" + 'cat' + "\t" + 'trait' + "\t" + 'lemme' + "\t" + 'commentaires' + "\n")
        for fichier in listefichierconll:
            fichier_conll = open(path_input + "/" + fichier,"r")
            # Lire le fichier conll ligne par ligne 按行读取文件
            for ligne in fichier_conll:
                if ligne[0]!="#" and ligne!="\n" and ligne!="":
                    ligne = ligne.split("\t")
                    mot = ligne[1]
                    lemme = ligne[2]
                    cat = ligne[3]
                    trait = ligne[5]
                    terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme + "\n"
                    liste_lexique_ori.append(terme) # 将所有词条写入列表
            fichier_conll.close()
            liste_lexique_ori_tri = list(set(liste_lexique_ori))    # 去重
            liste_lexique_ori_tri.sort()     # 排序
            
            for ele in liste_lexique_ori_tri:
                lexique.write(ele)
        lexique.close()
    if lexique_newwords:
        liste_lexique_newwords = []
        for fichier in listefichierconll:
            fichier_conll = open(path_input + "/" + fichier,"r")
            # Lire le fichier conll ligne par ligne
            for ligne in fichier_conll:
                if ligne[0]!="#" and ligne!="\n" and ligne!="":
                    ligne = ligne.split("\t")
                    mot = ligne[1]
                    lemme = ligne[2]
                    cat = ligne[3]
                    trait = ligne[5]
                    terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme + "\n"
                    voir_lexique_ori = open(outfile_path+"/"+outfile,"r")
                    contenu = ""
                    for line in voir_lexique_ori:
                        contenu = contenu+line  # 将旧词典的所有内容写入此变量，即一个长字符串
                    if terme not in contenu:    # 如果该词条不在旧词典里，将该词条写入新词典
                        liste_lexique_newwords.append(terme)
            fichier_conll.close()
            liste_lexique_newwords_tri = list(set(liste_lexique_newwords))
            liste_lexique_newwords_tri.sort()     
            lexique_new = open(outfile_path+"/"+outfile_newwords,"w")
            lexique_new.write('mot' + "\t" + 'cat' + "\t" + 'trait' + "\t" + 'lemme' + "\t" + 'commentaires' + "\n")
            for ele in liste_lexique_newwords_tri:
                lexique_new.write(ele)
    if combine:
        f1 = open(outfile_path+"/"+outfile_newwords,"r")
        f2 = open(outfile_path+"/"+outfile,"a")
        for lines in f1:
            if lines != "mot\tcat\ttrait\tlemme\tcommentaires\n":   # 不写入新词典的开头行
                f2.write(lines)
        f1.close()
        f2.close()



if __name__ == "__main__":

    while 1:
        choix=input("""Qu'est-ce que vous voulez faire ?

=> Si vous voulez construire un dictionnaire qui contient tous les mots, tapez "A";
=> Si vous voulez construire un dictionniare qui ne contient que les mots nouveaux, tapez "B";
=> Si vous voulez concaténer les mots nouveaux dans l'ancien dictionnaire, tapez "C".
=> Si vous ne voulez rien faire, tapez "T".

Veuillez prendre votre choix, merci :  
""")
        if choix.upper()=='T':
            print("Merci, au revoir !")
            break
        elif choix.upper()=='A':
            listefichierconll = input("Veuillez insérer le nom des fichiers conll (les noms doit être séparés par le virgule) : ")
            listefichierconll = listefichierconll.split(",")
            path_input = input("Veuillez insérer le chemin de ces fichiers conll : ")
            outfile = input("Veuillez nommer votre dictionnaire : ")
            outfile_path = input("Veuillez insérer le chemin de votre dictionnaire : ")
            getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords=None,lexique_ori=True,lexique_newwords=False,combine=False)
            print("Votre dictionnaire est bien construit !\n\n")
            
        elif choix.upper()=='B':
            listefichierconll = input("Veuillez insérer le nom des fichiers conll (les noms doit être séparés par le virgule) : ")
            listefichierconll = listefichierconll.split(",")
            path_input = input("Veuillez insérer le chemin de ces fichiers conll : ")
            outfile = input("Veuillez insérer le nom de votre ancien dictionnaire : ")
            outfile_newwords = input("Veuillez nommer le nouveau dictionnaire : ")
            outfile_path = input("Veuillez insérer le chemin de vos dictionnaires : ")
            getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords,lexique_ori=False,lexique_newwords=True,combine=False) 
            print("Votre nouveau dictionnaire est bien construit !\n\n")
            
        elif choix.upper()=='C':
            listefichierconll = ""
            path_input =""
            outfile = input("Veuillez insérer le nom de votre ancien dictionnaire : ")
            outfile_newwords = input("Veuillez insérer le nom du dictionnaire qui contient des mots nouveaux : ")
            outfile_path = input("Veuillez insérer le chemin de vos dictionnaires : ")
            getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords,lexique_ori=False,lexique_newwords=False,combine=True)  
            print("\nLa mise à jour de l'ancien dictionnaire est bien finie, les mots nouveaux sont ajpouté dans l'ancien dictionnaire !\n\n")
            

"""
Infos nécessaires : 
    listefichierconll = ["zh_hk-sud-test.conllu"]   # fichiers conll à traiter
    path_input = "E:/TAL/Stage/arborator/projects/Scripts/test" # path du dossier qui contient des fichiers conll 
    outfile_path = "E:/TAL/Stage/arborator/projects/Scripts"    # dossier où se trouve les lexiques
    outfile = "lexique.tsv"      # lexique complète
    outfile_newwords = "lexique_newwords.tsv"    # lexique pour les nouveaux mots
"""
"""
Mode d'emploi : 
    # pour construire un lexique, soit le premier lexique, soit un lexique qui contient tous les mots
      getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords=None,lexique_ori=True,lexique_newwords=False,combine=False)
    # pour construire un lexique qui ne contient que les nouveaux mots
      getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords,lexique_ori=False,lexique_newwords=True,combine=False)             
    # pour concaténer les nouveaux mots dans le lexique
      getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords,lexique_ori=False,lexique_newwords=False,combine=True)   
"""




