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
            # Lire le fichier conll ligne par ligne
            for ligne in fichier_conll:
                if ligne[0]!="#" and ligne!="\n" and ligne!="":
                    ligne = ligne.split("\t")
                    mot = ligne[1]
                    lemme = ligne[2]
                    cat = ligne[3]
                    trait = ligne[5]
                    terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme + "\n"
                    liste_lexique_ori.append(terme)
            fichier_conll.close()
            liste_lexique_ori_tri = list(set(liste_lexique_ori))
            liste_lexique_ori_tri.sort()     
            
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
                        contenu = contenu+line
                    if terme not in contenu:
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
            if lines != "mot\tcat\ttrait\tlemme\tcommentaires\n":
                f2.write(lines)
        f1.close()
        f2.close()



if __name__ == "__main__":

    listefichierconll = ["zh_hk-sud-test.conllu"]   # fichiers conll à traiter
    path_input = "E:/TAL/Stage/arborator/projects/Scripts/test" # path du dossier qui contient des fichiers conll 
    outfile_path = "E:/TAL/Stage/arborator/projects/Scripts"    # dossier où se trouve les lexiques
    outfile = "lexique.tsv"      # lexique complète
    outfile_newwords = "lexique_newwords.tsv"    # lexique pour les nouveaux mots
    getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords=None,lexique_ori=True,lexique_newwords=False,combine=False)


'''
Mode d'emploi : 
    # pour construire un lexique, soit le premier lexique, soit un lexique qui contient tous les mots
    

    # pour construire un lexique qui ne contient que les nouveaux mots
    getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords,lexique_ori=False,lexique_newwords=True,combine=False)             

    # pour concaténer les nouveaux mots dans le lexique
    # getlexique(listefichierconll,path_input,outfile_path,outfile,outfile_newwords,lexique_ori=False,lexique_newwords=False,combine=True)   
'''
           


