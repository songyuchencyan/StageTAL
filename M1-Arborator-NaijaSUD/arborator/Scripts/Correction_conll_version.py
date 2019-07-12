# -*- coding: utf-8 -*-
"""整个文件一行一行处理"""

def correction_sans_ambiguïté(dic_path,dic_nom,conll_folder_path,conll_corrigé_folder_path,nomfichierconll,listefichierconll=False,répertoirefichierconll=False):
    import os
    # 转换路径格式
    dic_path = dic_path.replace("\\","/")
    conll_folder_path = conll_folder_path.replace("\\","/")
    conll_corrigé_folder_path = conll_corrigé_folder_path.replace("\\","/")

    # 创建核对文件夹
    path_vérification = dic_path + "/Vérification"
    isExists=os.path.exists(path_vérification)
    if not isExists:
        os.makedirs(path_vérification) 


    ###### 获取词典列表 ######
    # 注意！词典每行的mot,cat,trait这三栏均不能为空！
    dictionnaire = open(dic_path + '/' + dic_nom,'r')
    lexique=[]
    for ligne_dictionnaire in dictionnaire:
        if ligne_dictionnaire != "" and ligne_dictionnaire != "\n":
            ligne_dictionnaire = ligne_dictionnaire.replace(" \n","")
            ligne_dictionnaire = ligne_dictionnaire.replace("   \n","")
            ligne_dictionnaire = ligne_dictionnaire.replace("\n","")
            liste_ligne_dictionnaire = ligne_dictionnaire.split('\t')
            list_lexi=[]
            list_lexi.append(liste_ligne_dictionnaire[0])
            list_lexi.append(liste_ligne_dictionnaire[1])
            # 重新排序trait：含有多个用"|"分开的trait
            a=liste_ligne_dictionnaire[2]
            if "|" in a:
                b=a.split("|")
                c=sorted(b)
                d="|".join(c)
                list_lexi.append(d)
            else:
                list_lexi.append(liste_ligne_dictionnaire[2])
            lexique.append(list_lexi)
        else:
            break
    dictionnaire.close()
    # print(lexique)
    mot = [x for [x,y,z] in lexique]    # 获取词的列表
    mot_catégorie=[[x,y] for [x,y,z] in lexique]  # 获取词和词类的列表


    if répertoirefichierconll:  # 读取目录里的所有文件
        import os
        file_list = os.listdir(conll_folder_path)
    if listefichierconll:   # 读取指定文件
        file_list = nomfichierconll.split(",")


    for files in file_list:
        text_name = str(files)
        f = open(conll_folder_path + "/" + text_name,"r")   
        ###### 改写文件名 ######
        # text_name = str(text_name.replace(".most.recent.trees.conll10",".conll"))
        # text_name = text_name.replace(".","-")
        # text_name = text_name.replace("-eaf-csv",".eaf.csv")
        # text_name = str(text_name.replace("-conll",".conll"))
        w = open(conll_corrigé_folder_path + "/" + text_name,"w")
        position_mot = open(dic_path + "/Vérification/" + "position_mot.txt","a")
        cat_ambiguïté = open(dic_path + "/Vérification/" + "erreurs_ambiguïté.txt","a")
        position_mot.write("\n\n\n" + text_name + "\n\n")
        cat_ambiguïté.write("\n\n\n" + text_name + "\n\n")
        n=0 # 获取文件行数
        for ligne_conll in f:
            n=n+1
            if ligne_conll != "":
                if ligne_conll[0] == "#" or ligne_conll == "\n":
                    w.write(ligne_conll)
                elif ligne_conll[0] != "#" and ligne_conll != "\n":
                    liste_ligne_conll = ligne_conll.split()
                    upper = liste_ligne_conll[1].upper()
                    title = liste_ligne_conll[1].title() 
                    if liste_ligne_conll[1] in mot:
                        if [liste_ligne_conll[1],liste_ligne_conll[3]] in mot_catégorie:
                            r=liste_ligne_conll[5]  # 重新排序trait：含有多个用"|"分开的trait
                            if "|" in r:
                                m=r.split("|")
                                l=sorted(m)
                                o="|".join(l)
                            if [liste_ligne_conll[1],liste_ligne_conll[3],liste_ligne_conll[5]] or [liste_ligne_conll[1],liste_ligne_conll[3],o] in lexique :
                                w.write(ligne_conll)
                            else:
                                for terme in lexique:
                                    if liste_ligne_conll[1] == terme[0] and liste_ligne_conll[3] == terme[1]:
                                        liste_ligne_conll[5] = terme[2]
                                        liste_ligne_conll_str = "\t".join(liste_ligne_conll)
                                print(liste_ligne_conll_str)
                                w.write(liste_ligne_conll_str)    
                                w.write("\n")            
                        else:
                            ###### 发现新的cat（有可能是错误也有可能是新的正确的cat，由于太多故省略） ######
                            # cat_à_vérifier = open("cat_à_vérifier.txt",'a')
                            # terme_cat_à_vérifier = liste_ligne_conll[1] + "\t" + liste_ligne_conll[3] + "\t" + liste_ligne_conll[5] + "\n"
                            # check_cat_à_vérifier = open("cat_à_vérifier.txt",'r')
                            # termes_cat = check_cat_à_vérifier.readlines()
                            # if terme_cat_à_vérifier in termes_cat :
                            #     pass
                            # else :
                            #     cat_à_vérifier.write(terme_cat_à_vérifier) 
                            cat_multiple = []
                            for terme in lexique:
                                if liste_ligne_conll[1] == terme[0]:
                                    cat_multiple.append(terme)
                            if len(cat_multiple) == 1:
                                liste_ligne_conll[3]=cat_multiple[0][1]
                                liste_ligne_conll[5]=cat_multiple[0][2]
                                liste_ligne_conll_str="\t".join(liste_ligne_conll)
                                w.write(liste_ligne_conll_str)
                                w.write("\n")   
                            else:
                                cat_ambiguïté.write("Dans le dictionnaire il y a : " + str(cat_multiple) + "\n")
                                cat_ambiguïté.write("On trouve à la ligne " + str(n) + " : " + ligne_conll + " => Il faut vérifier manuellement pour savoir si cette catégorie est correcte.\n\n")
                                w.write(ligne_conll)
                    elif upper in mot:
                        for terme in lexique:
                            if upper == terme[0]:
                                liste_ligne_conll[1] = terme[0]
                                liste_ligne_conll[3] = terme[1]
                                liste_ligne_conll[5] = terme[2]
                                liste_ligne_conll_str = "\t".join(liste_ligne_conll)
                                w.write(liste_ligne_conll_str)
                                w.write("\n")
                    elif title in mot:
                        for terme in lexique:
                            if title == terme[0]:
                                liste_ligne_conll[1] = terme[0]
                                liste_ligne_conll[3] = terme[1]
                                liste_ligne_conll[5] = terme[2]
                                liste_ligne_conll_str = "\t".join(liste_ligne_conll)
                                w.write(liste_ligne_conll_str)
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
                        position_mot.write("A la ligne '" + str(n) + "' on trouve : " + ligne_conll + "\nLe mot n'est pas dans le dictionnaire, ça peut être un mot nouveau, ou ça peut être une erreur orthographique. Si c'est une erreur orthographique, il faut corriger manuellement.\n\n")
                        w.write(ligne_conll)
                        mot_à_vérifier = open(dic_path + "/Vérification/" + "mot_à_vérifier.txt",'a')
                        terme_mot_à_vérifier = liste_ligne_conll[1] + "\t" + liste_ligne_conll[3] + "\t" + liste_ligne_conll[5] + "\n"
                        check_mot_à_vérifier = open(dic_path + "/Vérification/" + "mot_à_vérifier.txt",'r')
                        termes_mot = check_mot_à_vérifier.readlines()
                        if terme_mot_à_vérifier in termes_mot:  # 避免重复写入新词
                            pass
                        else :
                            mot_à_vérifier.write(terme_mot_à_vérifier)
                        mot_à_vérifier.close() 
                        check_mot_à_vérifier.close()  
            else:
                break
        print("La correction de " + text_name + "est bien finie.")
        position_mot.close()
        cat_ambiguïté.close
        f.close()
        w.close()
    print("La correction est tout finie !\n")
    print("""Vous allez trouver 3 fichiers dans le dossier 'Vérification' : 
    => 'mot_à_vérifier.txt', ce fichier contient des mots nouveaux qui ne sont pas dans votre dictionniare, soit c'est un mot nouveau, soit c'est une erreur orthographique que vous devez corriger manuellement dans le ficheir conll.
    => 'position_mot.txt', ce fichier indique la position d"un mot détecté qui ne sont pas dans votre dictionnaire, vous pouvez l'utiliser pour la correction manuelle.
    => 'erreurs_ambiguïté.txt', ce fichier contient des erreurs d'ambiguïté qui doivent être corrigé manuellement. Ça veut dire on a trouvé une nouvelle catégorie d"un mot, mais dans votre dictionnaire, ce mot a plusieurs catégories, on ne sais pas laquelle est correcte.""")

if __name__ == "__main__":
    while 1:
        choix=input("""Qu'est-ce que vous voulez faire ?

=> Si vous voulez corriger tous les fichers conll dans un dossier, tapez "A";
=> Si vous voulez corriger les fichiers conll que vous sélectionnez, tapez "B";
=> Si vous ne voulez rien faire, tapez "T".

Veuillez prendre votre choix, merci :  
""")
        if choix.upper()=='T':
            print("Merci, au revoir !")
            break
        elif choix.upper()=='A':
            dic_path = input("Veuillez insérer le chemin de votre dictionnaire : ")
            dic_nom = input ("Veuillez insérer le nom du dictionniare (format txt ou tsv) : ")
            conll_folder_path = input("Veuillez insérer le chemin de votre dossier des fichiers conll : ")
            conll_corrigé_folder_path = input("Veuillez insérer le chemin de votre dossier où vous voulez mettre les conll corrigés (ce dossier ne peut pas être à l'intérieur du dossier des fichiers conll): ")
            correction_sans_ambiguïté(dic_path,dic_nom,conll_folder_path,conll_corrigé_folder_path,nomfichierconll=None,listefichierconll=False,répertoirefichierconll=True)
        elif choix.upper()=='B':
            dic_path = input("Veuillez insérer le chemin de votre dictionnaire : ")
            dic_nom = input ("Veuillez insérer le nom du dictionniare (format txt ou tsv) : ")
            conll_folder_path = input("Veuillez insérer le chemin de votre dossier des fichiers conll : ")
            nomfichierconll = input("Veuillez insérer le nom des fichiers conll (les noms doit être séparés par le virgule) : ")
            conll_corrigé_folder_path = input("Veuillez insérer le chemin de votre dossier où vous voulez mettre les conll corrigés (ce dossier ne peut pas être à l'intérieur du dossier des fichiers conll): ")
            correction_sans_ambiguïté(dic_path,dic_nom,conll_folder_path,conll_corrigé_folder_path,nomfichierconll,listefichierconll=True,répertoirefichierconll=False)
    


