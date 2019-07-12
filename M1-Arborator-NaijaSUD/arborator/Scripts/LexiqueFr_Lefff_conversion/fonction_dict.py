###### Lefff转换为SUD/UD格式 ######
cat_trans = {'coo':"CCONJ", 'adv': "ADV", 'auxEtre':'AUX', 'cldr':'PRON', 'cln':'PRON', 'cld':'PRON', 'ilimp':'PRON', 'prel':'PRON', 'clg':'PRON', 'clr':'PRON', 'cll':'PRON', 'pres':'INTJ', 'np':'PROPN', 'advneg':'ADV', 'cla':'PRON', 'pri':'PRON', 'pro':'PRON', 'adj':'ADJ', 'prep':'ADP', 'clar':'PRON', 'clneg':'ADV','det':'DET', 'auxAvoir':'AUX', 'csu':'SCONJ', 'nc':'NOUN','v':'VERB'}
traits_trans = {
          'P':['VerbForm=Fin','Tense=Pres','Mood=Ind'],
          'F':['VerbForm=Fin','Tense=Fut','Mood=Ind'],
          'I':['VerbForm=Fin','Tense=Imp','Mood=Ind'],
          'J':['VerbForm=Fin','Tense=Past','Mood=Ind'],
          'C':['VerbForm=Fin','Tense=Pres','Mood=Cnd'],
          'Y':['VerbForm=Fin','Tense=Pres','Mood=Imp'],
          'S':['VerbForm=Fin','Tense=Pres','Mood=Sub'],
          'T':['VerbForm=Fin','Tense=Imp','Mood=Sub'],
          'K':['VerbForm=Part','Tense=Past','Voice=Pass'],
          'G':['VerbForm=Part','Tense=Pres'],
          'W':['VerbForm=Inf'],
          '1':['Person=1'],
          '2':['Person=2'],
          '3':['Person=3'],
          'm':['Gender=Masc'],
          'f':['Gender=Fem'],
          's':['Number=Sing'],
          'p':['Number=Plur'],
          'e':["_"]
          }
lefff = open("lefff_rerenettoye.txt","r")
Lexique = open("Dictionnaire.txt","w")
for ligne_n in lefff:
    ligne = ligne_n.replace("\n","")
    terme = ligne.split("\t")
    mot = terme[0]
    lemme = terme[2]
    cat_lefff = terme[1]
    trait_lefff = terme[3]
    if cat_lefff in cat_trans.keys():
        cat = cat_trans[cat_lefff]
        if trait_lefff == "":
            Lexique.write(mot+"\t"+cat+"\t"+"_"+"\t"+lemme+"\n")
        else:
            trait_lexi=[]
            for ele in trait_lefff:
                if ele in traits_trans.keys():
                    ele_trait = traits_trans[ele]
                    trait_lexi = trait_lexi + ele_trait
                else:
                    print(ligne)
            trait = "|".join(trait_lexi)
            Lexique.write(mot+"\t"+cat+"\t"+trait+"\t"+lemme+"\n")       



##### 排序 ######
f_lexique = open("Lexique_fr.txt","r")
lexique = []
for ligne in f_lexique:
    terme = ligne.split("\t")
    lexique.append(terme)
lexi_unique = [list(t) for t in set(tuple(_) for _ in lexique)]
lexi_unique.sort(key=lambda x: x[0])
f_lexique_ranger = open("Lexique_fr_ranger.txt","w")
for ele in lexi_unique:
        terme = "\t".join(ele)
        f_lexique_ranger.write(terme)
f_lexique.close()
f_lexique_ranger.close()



###### 将空项换为"_" ######
f_lexique = open("Dictionnaire.txt","r")
f_lexique_re = open("Dictionnaire_complet.txt","w")
lexique = []
for ligne in f_lexique:
    terme = ligne.split("\t")
    if terme[2]=="":
        terme[2]="_"
        mot = "\t".join(terme)
        f_lexique_re.write(mot)
    else:
        f_lexique_re.write(ligne)
f_lexique.close()
f_lexique_re.close()
        


###### 不写入带有空格的词组 ######
import re
lefff = open("lefff-3.4.mlex","r")
lefff_nettoye = open("lefff_nettoye.txt","w")
for ligne in lefff:
    terme = ligne.split('\t')
    terme0 = terme[0]
    terme0_list = terme0.split(" ")
    if len(terme0_list) == 1:
        lefff_nettoye.write(ligne)



###### 获取leff所有cat ######
lefff_nettoye = open("lefff_nettoye.txt","r")
cat_all=[]
for ligne in lefff_nettoye:
    terme = ligne.split('\t')
    cat_all.append(terme[1])
cat=list(set(cat_all))
print(cat)



###### 不写入advPref类的词 ######
lefff_nettoye = open("lefff_renettoye.txt","r")
lefff_renettoye = open("lefff_rerenettoye.txt","w")
cat_all=[]
for ligne in lefff_nettoye:
    if "advPref" in ligne:
        pass
    else:
        lefff_renettoye.write(ligne)



###### 获取词典所有的cat和trait
f_lexique = open("Lexique_fr_ranger.txt","r")
lexique = []
catégories_all = []
trait_all = []
for ligne in f_lexique:
    terme = ligne.split("\t")
    catégories_all.append(terme[1])
    trait_all.append(terme[2])
catégorie = list(set(catégories_all))
trait = list(set(trait_all))

classer_cat = open("cat.txt","w")
for cate in catégorie:
    classer_cat.write(cate)
classer_trait = open("trait.txt","w")
for tra in trait:
    classer_trait.write(tra+"\n")

# lexi_unique = [list(t) for t in set(tuple(_) for _ in lexique)]
# lexi_unique.sort(key=lambda x: x[0])
# f_lexique_ranger = open("Lexique_fr_ranger.txt","w")
# for ele in lexi_unique:
#         terme = "\t".join(ele)
#         f_lexique_ranger.write(terme)

f_lexique.close()
#f_lexique_ranger.close()
    


###### 找出属于列表中的词类的词 ######
Lexique = open("Dictionnaire.txt","r")
lemma_none_lefff_cat = ['adj','adjPref','adv','advneg','auxAvoir','auxEtre','caimp','cfi','cla','clar','cld','cldr','clg','cll','cln','clneg','clr','coo','csu','det','etr','ilimp','nc','ncpred','np','poncts','ponctw','prel']
mot = []
for ligne_n in Lexique:
    ligne = ligne_n.replace("\n","")
    terme = ligne.split("\t")
    a=len(terme)-1
    if terme[a] in lemma_none_lefff_cat:
        mot.append(terme[0])
mot1=set(mot)
print(mot1)
'''
{"l'", 'je', "m'", 'nous', 'tu', 'vs', 'elle', 'lui', 'ils', 'se', 'leur', "ch'", 'moi', 'te', 'le', 'y', 'en', 'les', 'la', "s'", 'on', 'vous', 'il', 'elles', "l'on", 'toi', 'me', "t'", "j'"}
'''
dic = {}
'''
ch'     PRON    Person=1|Number=Sing    cln
elle    PRON    Person=3|Gender=Fem|Number=Sing cln
elles   PRON    Person=3|Gender=Fem|Number=Plur cln
en      PRON            clg
en      PRON            cll
il      PRON    Person=3|Gender=Masc|Number=Sing        cln
il      PRON    Person=3|Gender=Masc|Number=Sing        ilimp
ils     PRON    Person=3|Gender=Masc|Number=Plur        cln
j'      PRON    Person=1|Number=Sing    cln
je      PRON    Person=1|Number=Sing    cln
l'      PRON    Person=3|Gender=Fem|Number=Sing cla
l'      PRON    Person=3|Gender=Masc|Number=Sing        cla
l'on    PRON    Person=3|Number=Sing    cln
la      PRON    Person=3|Gender=Fem|Number=Sing cla
le      PRON    Person=3|Gender=Masc|Number=Sing        cla
les     PRON    Person=3|Number=Plur    cla
leur    PRON    Person=3|Number=Plur    cld
lui     PRON    Person=3|Number=Sing    cld
m'      PRON    Person=1|Number=Sing    cla
m'      PRON    Person=1|Number=Sing    cld
m'      PRON    Person=1|Number=Sing    clr
me      PRON    Person=1|Number=Sing    cla
me      PRON    Person=1|Number=Sing    cld
me      PRON    Person=1|Number=Sing    clr
moi     PRON    Person=1|Number=Sing    cla
moi     PRON    Person=1|Number=Sing    cld
nous    PRON    Person=1|Number=Plur    cla
nous    PRON    Person=1|Number=Plur    cld
nous    PRON    Person=1|Number=Plur    cln
nous    PRON    Person=1|Number=Plur    clr
on      PRON    Person=3|Number=Sing    cln
s'      PRON    Person=3|Number=Plur    clar
s'      PRON    Person=3|Number=Sing    clar
s'      PRON    Person=3|Number=Plur    cldr
s'      PRON    Person=3|Number=Sing    cldr
s'      PRON    Person=3|Number=Plur    clr
s'      PRON    Person=3|Number=Sing    clr
se      PRON    Person=3|Number=Plur    clar
se      PRON    Person=3|Number=Sing    clar
se      PRON    Person=3|Number=Plur    cldr
se      PRON    Person=3|Number=Sing    cldr
se      PRON    Person=3|Number=Plur    clr
se      PRON    Person=3|Number=Sing    clr
t'      PRON    Person=2|Number=Sing    cla
t'      PRON    Person=2|Number=Sing    cld
t'      PRON    Person=2|Number=Sing    cln
t'      PRON    Person=2|Number=Sing    clr
te      PRON    Person=2|Number=Sing    cla
te      PRON    Person=2|Number=Sing    cld
te      PRON    Person=2|Number=Sing    clr
toi     PRON    Person=2|Number=Sing    cla
toi     PRON    Person=2|Number=Sing    cld
tu      PRON    Person=2|Number=Sing    cln
vous    PRON    Person=2|Number=Plur    cla
vous    PRON    Person=2|Number=Plur    cld
vous    PRON    Person=2|Number=Plur    cln
vous    PRON    Person=2|Number=Plur    clr
vs      PRON    Person=2|Number=Plur    cla
vs      PRON    Person=2|Number=Plur    cld
vs      PRON    Person=2|Number=Plur    cln
vs      PRON    Person=2|Number=Plur    clr
y       PRON            cld
y       PRON            cll
'''



###### 通过conll文件构建词典 ######
f_conll = open("sud.french.sequoia.parser.trees.conll10","r")
f_lexique = open("Lexique_fr.txt","a")

lexi_initial=[]
for ligne in f_conll:
    if ligne[0] != "#" and ligne != "\n":
        lignenew = ligne.replace(" ","\t")
        lignenew_list = lignenew.split("\t")
        token = lignenew_list[1]
        lemma = "" if lignenew_list[2] == token else lignenew_list[2]
        pos = lignenew_list[3]
        trait = lignenew_list[5]
        lexi_initial.append([token,pos,trait,lemma])

lexi_unique = [list(t) for t in set(tuple(_) for _ in lexi_initial)]
lexi_unique.sort(key=lambda x: x[0])
for ele in lexi_unique:
        terme = "\t".join(ele)
        f_lexique.write(terme + "\n")