# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:31:41 2020

@author: al
"""

import re
from collections import defaultdict
import pandas as pd

phev_df = pd.read_excel('./ALL/EXEV.xlsx')
data_list = list(phev_df['comment'])
ccmp = re.compile("【最满意】|【最不满意】|【空间】|【动力】|【操控】|【能耗】|【舒适性】|【外观】|【内饰】|【性价比】|【为什么选择这款车】|【电耗】|【保养】|【故障】|【吐槽】|【运动】|【经济】|【为什么最终选择这款车】|【最满意的一点】|【最不满意的一点】|【为什么最终选择这款车？】|【其它描述】|【其他描述】|【耗电量】")
all_labels = ['最满意', '最不满意', '空间', '动力', '操控', '能耗', '舒适性', '外观', '内饰', '性价比', '为什么选择这款车', '电耗', '保养', '故障', '吐槽', '运动', '经济', '为什么最终选择这款车', '最满意的一点', '最不满意的一点', '为什么最终选择这款车？', '其他描述', '其它描述', '耗电量']
all_labels_ = ['最满意_', '最不满意_', '空间_', '动力_', '操控_', '能耗_', '舒适性_', '外观_', '内饰_', '性价比_', '为什么选择这款车_', '电耗_', '保养_', '故障_', '吐槽_', '运动_', '经济_', '为什么最终选择这款车_', '最满意的一点_', '最不满意的一点_', '为什么最终选择这款车？_', '其他描述_', '其它描述_', '耗电量_']

'''
data = list(set(data_list))
data_str = '\n'.join(data)
with open('all_.txt', 'w', encoding='utf-8') as f:
    f.write(data_str)

'''

c = defaultdict(list)

for i in range(len(data_list)):
    tc = defaultdict(list)
    label = ccmp.findall(str(data_list[i]))
    rst = re.sub(ccmp, '\n', str(data_list[i]))
    data_txt = rst.split('\n')
    # print('----------')
    # print(data_list[i])
    # print(label[:])
    #print(data_txt[1:])
    for idx in range(len(label)):
        tc[label[idx][1:-1]].append(data_txt[idx+1])
    for i in list(set(label)):
        tc[i[1:-1]] = '，'.join(list(set(tc[i[1:-1]])))
    # print(tc)
    for i in all_labels:
        if len(tc[i]) == 0:
            tc[i] = -1
    for i in all_labels:
        c[i].append(tc[i])

c = dict(c)
# print(c)
for i in range(len(all_labels)):
    phev_df[all_labels_[i]] = c[all_labels[i]]

phev_df.to_excel('EXEV_p2.xlsx', encoding='utf_8_sig')

'''

df = pd.DataFrame.from_dict(c, orient='index')
if not df.empty:
    file_name = 'all_.xlsx'
    df_ = pd.DataFrame(df.values.T, columns=df.index, index=df.columns)
    columns_list = list(df.index)
    df = df_.drop_duplicates(subset=columns_list)
    df.to_excel(file_name, encoding='utf_8_sig')
'''
    
    
    
    
    