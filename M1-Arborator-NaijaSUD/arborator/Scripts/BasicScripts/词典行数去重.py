f = open("Lexiquepourcorrection_new.txt","r")
mots = open("mot.txt","w")
liste = []
for lignen in f:
    if lignen != "":
        ligne = lignen.replace("\n","")
        terme = ligne.split("\t")
        if "_" in terme[2]:
            terme[2]="_"
        liste.append(terme[0:3])
print(liste)
liste_sans_doublon = []
for ele in liste:
    if ele not in liste_sans_doublon:
        liste_sans_doublon.append(ele)

for mot in liste_sans_doublon:
    if mot[2] == "":
        print(mot[2])
        mots.write(str(mot[0])+"\t"+str(mot[1])+"\t"+"_"+"\n")
    else:
        mots.write(str(mot[0])+"\t"+str(mot[1])+"\t"+str(mot[2])+"\n") 
