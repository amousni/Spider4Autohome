# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:14:36 2020

@author: al
"""

import re
import os

#大量特殊字符问题
cmp1 = re.compile("\.hs_bg_myAppend.*?.\);}")
cmp2 = re.compile("\(function\(.*?.;}\)\(document\);")
cmp3 = re.compile("0%buffered.*?.chrome80.0.3987.\d\d\d")

EV_file_list = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\data processing\EV")
PHEV_file_list = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\data processing\PHEV")
EXEV_file_list = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\data processing\EXEV")

for file in EV_file_list:
    if file.endswith('.txt'):
        file_path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//EV//" + file
        path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//EV//" + file
        print(file, ' is processing')
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                data = f.read()
        except:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
        rst1 = re.sub(cmp1, '', data)
        rst2 = re.sub(cmp2, '', rst1)
        rst3 = re.sub(cmp3, '', rst2)
        data = rst3.split('\n')
        data_ = list(set(data))
        rst3 = '\n'.join(data_)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(rst3)
        all_path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//EV//allEV.txt"
        for i in data_:
            s = i + '\n'
            with open(all_path, 'a', encoding='utf-8') as f:
                f.write(s)
        
for file in PHEV_file_list:
    if file.endswith('.txt'):
        file_path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//PHEV//" + file
        path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//PHEV//" + file
        print(file, ' is processing')
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                data = f.read()
        except:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
        rst1 = re.sub(cmp1, '', data)
        rst2 = re.sub(cmp2, '', rst1)
        rst3 = re.sub(cmp3, '', rst2)
        data = rst3.split('\n')
        data_ = list(set(data))
        rst3 = '\n'.join(data_)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(rst3)
        all_path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//PHEV//allPHEV.txt"
        for i in data_:
            s = i + '\n'
            with open(all_path, 'a', encoding='utf-8') as f:
                f.write(s)
            
for file in EXEV_file_list:
    if file.endswith('.txt'):
        file_path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//EXEV//" + file
        path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//EXEV//" + file
        print(file, ' is processing')
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                data = f.read()
        except:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
        rst1 = re.sub(cmp1, '', data)
        rst2 = re.sub(cmp2, '', rst1)
        rst3 = re.sub(cmp3, '', rst2)
        data = rst3.split('\n')
        data_ = list(set(data))
        rst3 = '\n'.join(data_)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(rst3)
        all_path = "C://Users//al//Desktop//Deep Learning//NLP//data processing//EXEV//allEXEV.txt"
        for i in data_:
            s = i + '\n'
            with open(all_path, 'a', encoding='utf-8') as f:
                f.write(s)          
            
            
            
            