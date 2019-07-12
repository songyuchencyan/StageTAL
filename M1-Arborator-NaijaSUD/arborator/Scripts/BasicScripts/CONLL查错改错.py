# -*- coding: utf-8 -*-
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







f=open("P_WAZP_07_Imonirhuas.Life.Story_PRO.most.recent.trees.with.feats.conllu_reordered",'r')
w=open("E:/TAL/Stage/arborator/projects/NaijaSUD/export/Correction/CORRIGER_P_WAZP_07_Imonirhuas.Life.Story_PRO.most.recent.trees.with.feats.conllu_reordered","w")
cat = open("cat_erreur.txt","a")
filename = str(f).replace("<_io.TextIOWrapper name='","")
filename = filename.replace("' mode='r' encoding='cp65001'>","")
cat.write("\n\n\n" + filename + "\n\n")
n=0
while 1:
    line=f.readline()
    n=n+1
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
                        cat.write(str(cat_double) + "\n")
                        cat.write(str(n) + " : " + line + " ne sait pas correspondre à laquelle\n\n")
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
                print(n,list_line,"mot pas dans lexique")
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

