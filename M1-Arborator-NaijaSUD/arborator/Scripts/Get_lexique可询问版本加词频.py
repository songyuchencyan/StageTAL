#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import re
import os
import time


def getlexique(listefichierconll,input_path,outfile_path,outfile=None,outfile_newwords=None,lexique_ori=False,lexique_newwords=False,combine=False):
    if lexique_ori:
        liste_lexique_ori = []
        lexique = open(outfile_path+"/"+outfile,"w")
        lexique.write('mot' + "\t" + 'cat' + "\t" + 'trait' + "\t" + 'lemme' + "\t" + 'fréquence' + "\t" + 'commentaires' + "\n")
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
                    terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme
                    liste_lexique_ori.append(terme)
            fichier_conll.close()
            liste_lexique_ori.sort()
            fre_dic = {}    # key为词条，value为词频
            for eles in liste_lexique_ori:
                fre_dic[eles] = liste_lexique_ori.count(eles)   # 计算列表中元素的出现次数，作为词频
            for terme_info,fre in fre_dic.items():
                lexique.write(terme_info + "\t" + str(fre) + "\n")
        lexique.close()
    if lexique_newwords:
        liste_lexique_newwords = [] # 包含所有新词
        liste_lexique_not_newwords = [] # 包含所有在旧词典出现的词
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
                    terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme
                    voir_lexique_ori = open(outfile_path+"/"+outfile,"r")
                    contenu = ""
                    for line in voir_lexique_ori:
                        contenu = contenu+line
                    if terme not in contenu:
                        liste_lexique_newwords.append(terme)
                    else:
                        liste_lexique_not_newwords.append(terme)
            fichier_conll.close()
            liste_lexique_newwords.sort()
            liste_lexique_not_newwords.sort()  
            fre_dic_newwords = {}
            fre_dic_not_newwords = {}
            for eles1 in liste_lexique_newwords:
                fre_dic_newwords[eles1] = liste_lexique_newwords.count(eles1)   # 计算新词词频
            for eles2 in liste_lexique_not_newwords:
                fre_dic_not_newwords[eles2] = liste_lexique_not_newwords.count(eles2)   # 计算旧词词频，为合并词典时进行旧词词频数叠加
            lexique_new = open(outfile_path+"/"+outfile_newwords,"w")
            lexique_new.write('mot' + "\t" + 'cat' + "\t" + 'trait' + "\t" + 'lemme' + "\t" + 'fréquence'+ "\t" + 'commentaires' + "\n")
            for terme_info1,fre1 in fre_dic_newwords.items():
                lexique_new.write(terme_info1 + "\t" + str(fre1) + "\n")
            lexique_notnew = open(outfile_path+"/"+"lexique_notnew.tsv","w")
            for terme_info2,fre2 in fre_dic_not_newwords.items():
                lexique_notnew.write(terme_info2 + "\t" + str(fre2) + "\n")
    if combine:
        f1 = open(outfile_path+"/"+outfile_newwords,"r")
        f2 = open(outfile_path+"/"+outfile,"a")
        for lines in f1:
            if lines != "mot\tcat\ttrait\tlemme\tfréquence\tcommentaires\n":
                f2.write(lines)
        f1.close()
        f2.close()
        choix1 = input("""Est-ce que les mots nouveaux mots dans le nouveaux dictionnaire viennent du fichier conll que vous avez utilisé pour construire l'ancien lexique ? 
        Tapez 'oui' ou 'non' :  """)
        if choix1.lower() == "non": # 如果是全新的conll文件，需要对旧词进行词频更新，即叠加
            f3 = open(outfile_path+"/"+"lexique_notnew.tsv","r")    # 打开只包含已有词的词典
            contenu_re = "" 
            for line in f3:
                line = line.split("\t")
                line_re = line[0:4]
                line_re = "\t".join(line_re)
                f4 = open(outfile_path+"/"+outfile,"r") # 打开旧词典，注意必须在循环里打开，如在外面，会导致读完的行不再重新读取。
                for ligne in f4:
                    if line_re in ligne:
                        ligne = ligne.split("\t")
                        fre_re = str(int(line[4])+int(ligne[4]))    # 将两次运行输入的不同conll文件中，相同的词汇进行词频叠加
                        terme_re = line_re + "\t" + fre_re + "\n"   # 生成新的词条
                f4.close()
                contenu_re = contenu_re + terme_re  # 包含已更新词频的所有旧词条
            f3.close()
            
            f5 = open(outfile_path+"/"+outfile,"w")
            f6 = open(outfile_path+"/"+outfile_newwords,"r")
            f5.write("mot\tcat\ttrait\tlemme\tfréquence\tcommentaires\n")
            f5.write(contenu_re)    # 重写旧词典，即更新了词频
            for ligne_f6 in f6:
                f5.write(ligne_f6)  # 写入新词词条
            f6.close()
            f5.close()
            print("\nLes mots nouveaux sont ajouté dans l'ancien dictionnaire, et la fréquence est renouvelée !\n")
        else:
            print("les mots nouveaux sont ajouté dans l'ancien dictionnaire !\n")



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
            print("\nLa mise à jour de l'ancien dictionnaire est bien finie !\n\n")
            

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




