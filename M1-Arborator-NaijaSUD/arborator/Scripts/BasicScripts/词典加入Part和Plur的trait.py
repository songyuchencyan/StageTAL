f = open("mot.txt","r")
mots = open("mot_1.txt","w")
liste = []
for lignen in f:
    if lignen != "":
        ligne = lignen.replace("\n","")
        terme = ligne.split("\t")
        liste.append(terme)

for ele in liste:
    if "VerbForm=Part" in ele[2] :
        terme = ele[3]+"\t"+"VERB"+"\t"+"_"+"\t"+""+"\t"+""+"\n"
        mots.write(terme)
    if "Number=Plur" in ele[2] :
        terme = ele[3]+"\t"+"NOUN"+"\t"+"_"+"\t"+""+"\t"+""+"\n"
        mots.write(terme)

