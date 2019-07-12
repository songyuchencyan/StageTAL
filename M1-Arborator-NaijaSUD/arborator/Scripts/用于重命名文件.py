#coding:utf-8
import os
file_folder = os.listdir(r'C:/Users/CYAN/CONLL')
for filename in file_folder:
    new_name = filename.replace(".","-")
    new_name = new_name.replace("-eaf-csv",".eaf.csv")
    new_name = new_name.replace("-most-recent-trees-conll10",".conll")
    os.rename(r'C:/Users/CYAN/CONLL/'+filename,r'C:/Users/CYAN/CONLL/'+new_name)

# (unicode error) ‘unicodeescape’ codec can’t decode bytes in position 2-3: truncated \UXXXXXXXX escape
# 原因：在Python中\是转义符，\u表示其后是UNICODE编码，因此\User在这里会报错，在字符串前面加个r表示就可以了。