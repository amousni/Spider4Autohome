# -*- coding:utf-8 -*-
from __future__ import print_function, division, absolute_import
import requests
from lxml import etree, html
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

import ssl
from urllib import request
from scrapy.selector import Selector

import time
import datetime

from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from reportlab.graphics.shapes import Path
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing, scale
from PIL import Image

from collections import defaultdict

from image2word_baidu import get_words

bd_OCR_URL_general = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
bd_OCR_URL_accurate = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

from xf_ocr import xf_get_word

import os

chrome_driver = 'C://Users//al//Desktop//Deep Learning//NLP//chromedriver'

ssl._create_default_https_context = ssl._create_unverified_context

class ReportLabPen(BasePen):
    """A pen for drawing onto a reportlab.graphics.shapes.Path object."""
    
    def __init__(self, glyphSet, path=None):
        BasePen.__init__(self, glyphSet)
        if path is None:
            path = Path()
        self.path = path
 
    def _moveTo(self, p):
        (x,y) = p
        self.path.moveTo(x,y)
 
    def _lineTo(self, p):
        (x,y) = p
        self.path.lineTo(x,y)
 
    def _curveToOne(self, p1, p2, p3):
        (x1,y1) = p1
        (x2,y2) = p2
        (x3,y3) = p3
        self.path.curveTo(x1, y1, x2, y2, x3, y3)
 
    def _closePath(self):
        self.path.closePath()
 
def ttfToImage(fontName,imagePath,fmt="png"):
    image_names = []
    font = TTFont(fontName)
    gs = font.getGlyphSet()
    glyphNames = font.getGlyphNames()
    for i in glyphNames:
        if i[0] == '.':#跳过'.notdef', '.null'
            continue
        
        g = gs[i]
        pen = ReportLabPen(gs, Path(fillColor=colors.black, strokeWidth=2))
        g.draw(pen)
        w, h = g.width, g.width
        g = Group(pen.path)
        g.translate(200, 400)
        
        d = Drawing(w*1.2, h*1.2)
        d.add(g)
        imageFile = imagePath+"/"+i+".png"
        renderPM.drawToFile(d, imageFile, fmt)
        
        image_names.append(i)
        #print(i)
    return image_names

def produceImage(file_in, file_out, width=300, height=300):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)
 
#抓取autohome评论
class AutoSpider:
    #页面初始化
    def __init__(self):
        self.headers = {
            #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            #"Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }
        
    # 获取评论
    def getNote(self, car_name, url = "https://k.autohome.com.cn/detail/view_01e3xetbx268wkgd1s74v00000.html?st=1&piap=0|5346|0|0|1|0|0|0|0|0|1"):
        #host = {'host':'club.autohome.com.cn',
                #'cookie':'your cookie'}
        #headers = dict(self.headers.items() + host.items())
        # 获取页面内容

        self.url = url
        self.car_name = car_name
        print(self.url)

        browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
        browser.set_page_load_timeout(30)
        browser.set_script_timeout(30)
        try:
            browser.get(self.url)
        except:
            print('selenium browser broke!')
            print('可能原因是网络速度较慢')
            print('切换网络')
            while os.system('netsh wlan connect name=E329_5G'):
                time.sleep(1)
                continue
            
            print('当前网络: E329_5G')
            time.sleep(5)
            browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
            browser.set_page_load_timeout(30)
            browser.set_script_timeout(30)
            try:
                browser.get(self.url)
            except:
                while os.system('netsh wlan connect name=E329_2.4G'):
                    time.sleep(1)
                    continue
                print('当前网络: E329_2.4G')
                time.sleep(5)
                browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
                browser.set_page_load_timeout(30)
                browser.set_script_timeout(30)
                try:
                    browser.get(self.url)
                except:
                    while os.system('netsh wlan connect name=eduroam'):
                        time.sleep(1)
                        continue
                    print('当前网络: eduroam')
                    time.sleep(5)
                    browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
                    browser.set_page_load_timeout(30)
                    browser.set_script_timeout(30)
                    try:
                        browser.get(self.url)
                    except:
                        print('*****重启selenium失败，记录故障url，睡眠300s*****')
                        with open('error_url.txt', 'a') as f:
                            s = self.car_name + '_NETError' + '\t' + self.url + '\n'
                            f.write(s)
                        return 0, 0
                    
        r = browser.page_source
        selector = Selector(text = r)
        h = etree.HTML(r)
        response = html.fromstring(r)
        browser.close()
        '''
        req = request.Request(self.url, headers=self.headers)
        r = request.urlopen(req).read().decode('gbk')
        selector = Selector(text=r)
        h = etree.HTML(r)
        response = html.fromstring(r)
        '''
        
        # 匹配ttf font
        print('Find and save ttf')
        cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
        rst = cmp.findall(r)
        try:
            ttf = requests.get("http:" + rst[0], stream=True)
        except:
            print('*****Cannot find ttf url!*****')

            error_xpath_r = h.xpath("/html/body/div[@class='wrap']/div[@class='info2']")
            if len(error_xpath_r) != 0:
                print('*****当前口碑已被屏蔽*****')
                with open('error_url.txt', 'a') as f:
                    s = self.car_name + '_COMMENTError' + '\t' + self.url + '\n'
                    f.write(s)
                return 0, 0
            else:
                while os.system('netsh wlan connect name=E329_5G'):
                    time.sleep(1)
                    continue
                
                print('当前网络: E329_5G')
                time.sleep(5)
                browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
                browser.set_page_load_timeout(30)
                browser.set_script_timeout(30)
                try:
                    browser.get(self.url)
                    r = browser.page_source
                    browser.close()
                    print('Find and save ttf')
                    cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
                    rst = cmp.findall(r)
                    ttf = requests.get("http:" + rst[0], stream=True)
                except:
                    while os.system('netsh wlan connect name=E329_2.4G'):
                        time.sleep(1)
                        continue
                    print('当前网络: E329_2.4G')
                    time.sleep(5)
                    browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
                    browser.set_page_load_timeout(30)
                    browser.set_script_timeout(30)
                    try:
                        browser.get(self.url)
                        r = browser.page_source
                        browser.close()
                        print('Find and save ttf')
                        cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
                        rst = cmp.findall(r)
                        ttf = requests.get("http:" + rst[0], stream=True)
                    except:
                        while os.system('netsh wlan connect name=eduroam'):
                            time.sleep(1)
                            continue
                        print('当前网络: eduroam')
                        time.sleep(5)
                        browser = webdriver.Chrome(executable_path = chrome_driver, options=chrome_options)
                        browser.set_page_load_timeout(30)
                        browser.set_script_timeout(30)
                        try:
                            browser.get(self.url)
                            r = browser.page_source
                            browser.close()
                            print('Find and save ttf')
                            cmp = re.compile("url\('(//.*.ttf)'\) format\('woff'\)")
                            rst = cmp.findall(r)
                            ttf = requests.get("http:" + rst[0], stream=True)

                        except:
                            print('*****全部网络连接失败，睡眠300s*****')
                            with open('error_url.txt', 'a') as f:
                                s = self.car_name + '_NETError' + '\t' + self.url + '\n'
                                f.write(s)
                            time.sleep(300)
                            return 0, 0
            
        with open("autohome.ttf", "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        
        #字体库文件转图片
        print('Convert ttf to pngs', end='\t')
        try:
            image_names = ttfToImage(fontName="autohome.ttf",imagePath="images")
        except:
            print('字体库文件保存错误，重新下载字体库')
            ttf = requests.get("http:" + rst[0], stream=True)
            with open("autohome.ttf", "wb") as pdf:
                for chunk in ttf.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            try:
                print('重新转换ttf')
                image_names = ttfToImage(fontName="autohome.ttf",imagePath="images")
            except:
                print('*****字体库文件二次保存错误！*****')
                with open('error_url.txt', 'a') as f:
                    s = self.car_name + '_TTFError' + '\t' + self.url + '\n'
                    f.write(s)
                time.sleep(100)
                return 0, 0
        
        #字体图片压缩
        root = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//images//"
        for image_name in image_names:
            path = root + image_name + '.png'
            produceImage(path, path, 300, 300)
        
        #图片整合
        print('Concat ttf pngs', end='\t')
        num_images = len(image_names)
        row = 10
        col = int(num_images/row) + 1
        toImage = Image.new('RGB', (300*row, col*300))
        flag = 0
        toImage_path = root + 'all.png'
        
        for y in range(col):
            for x in range(row):
                if flag < num_images:
                    path = root + image_names[flag] + '.png'
                    fromImage = Image.open(path)
                    toImage.paste(fromImage, (x*300, y*300))
                    flag += 1
        toImage.save(toImage_path)
        
        print('OCR')
        #整合图片文字识别
        try:
            print('当前OCR方法：百度普通模式')
            text_list = get_words(toImage_path, bd_OCR_URL_general)
            #print('length of text list: %d'%(len(text_list)))
            #print('num of ttf img: %d'%(num_images))
        except:
            print('百度OCR普通模式调用失败，调用精度模式')
            try:
                text_list = get_words(toImage_path, bd_OCR_URL_accurate)
                #print('length of text list: %d'%(len(text_list)))
                #print('num of ttf img: %d'%(num_images)) 
            except:
                print('百度OCR精度模式调用失败，调用讯飞OCR')
                try:
                    text_list = xf_get_word(toImage_path)
                    #print('length of text list: %d'%(len(text_list)))
                    #print('num of ttf img: %d'%(num_images)) 
                except:
                    print('讯飞OCR调用失败，10秒后重新调用')
                    time.sleep(10)
                    try:
                        text_list = xf_get_word(toImage_path)
                        #print('length of text list: %d'%(len(text_list)))
                        #print('num of ttf img: %d'%(num_images)) 
                    except:
                        print('二次调用失败，记录故障url')
                        with open('error_url.txt', 'a') as f:
                            s = self.car_name + '_NETError' + '\t' + self.url + '\n'
                            f.write(s)
                        return 0, 0
        
        #判断当前百度OCR识别字体个数是否与真实字体图片个数匹配
        #如果不匹配则调用讯飞OCR
        if len(text_list) != num_images:
            print('OCR字体识别个数问题，调用百度精度OCR')
            try:
                text_list = get_words(toImage_path, bd_OCR_URL_accurate)
                #print('length of text list: %d'%(len(text_list)))
                #print('num of ttf img: %d'%(num_images))
                if len(text_list) != num_images:
                    print('百度精度OCR字符不匹配，调用讯飞OCR')
                    try:
                        text_list = xf_get_word(toImage_path)
                        #print('length of text list: %d'%(len(text_list)))
                        #print('num of ttf img: %d'%(num_images)) 
                    except:
                        print('讯飞OCR调用失败，10秒后重新调用')
                        time.sleep(10)
                        try:
                            text_list = xf_get_word(toImage_path)
                            #print('length of text list: %d'%(len(text_list)))
                            #print('num of ttf img: %d'%(num_images)) 
                        except:
                            print('二次调用失败，记录故障url')
                            with open('error_url.txt', 'a') as f:
                                s = self.car_name + '_NETError' + '\t' + self.url + '\n'
                                f.write(s)
                            return 0, 0
            except:
                print('百度精度OCR调用失败，可能使用量到达今日上限，调用讯飞OCR')
                try:
                    text_list = xf_get_word(toImage_path)
                    #print('length of text list: %d'%(len(text_list)))
                    #print('num of ttf img: %d'%(num_images)) 
                except:
                    print('讯飞OCR调用失败，10秒后重新调用')
                    time.sleep(10)
                    try:
                        text_list = xf_get_word(toImage_path)
                        #print('length of text list: %d'%(len(text_list)))
                        #print('num of ttf img: %d'%(num_images)) 
                    except:
                        print('二次调用失败，记录故障url')
                        with open('error_url.txt', 'a') as f:
                            s = self.car_name + '_NETError' + '\t' + self.url + '\n'
                            f.write(s)
                        return 0, 0
            
        # 解析字体库font文件
        font = TTFont('autohome.ttf')
        uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        
        if len(image_names) != len(text_list):
            print('OCR故障，保存故障url')
            with open('error_url.txt', 'a') as f:
                s = self.car_name + '_OCRError' + '\t' + self.url + '\n'
                f.write(s)
            return 0, 0
        
        #按照uniList给text_list排序
        uni2text = dict(zip(image_names, text_list))
        #print('uni2text:', uni2text)
        wordList = []
        for uni in uniList:
            if uni.startswith('uni'):
                wordList.append(uni2text[uni])
        
        utf8List = [eval(r"u'\u" + uni[3:] + "'") for uni in uniList[1:]]        
        
        # 获取发帖内容
        junk_note1 = h.xpath("//div[@class='mouth-main']/div[@class='mouth-item koubei-final']/div[@class='text-con']/style/text()")
        junk_note2 = h.xpath("//div[@class='mouth-main']/div[@class='mouth-item koubei-final']/div[@class='text-con']/script/text()")
        junk = junk_note1 + junk_note2
        data = selector.xpath("//div[@class='text-con']")
        note = ''
        for i in range(len(data)):
            note = note + data[i].xpath('string(.)').extract()[0]
        for j in junk:
            note = note.replace(j, '')
        for i in range(len(utf8List)):
            note = note.replace(utf8List[i], wordList[i])
        note = note.replace(' ', '')
        note = note.replace('\n', '')
        note = note.replace('\t', '')
        #print(note)
        
        #删除images目录下保存的字体图片
        #print("清理字体图片")
        #img_names = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\images")
        #for img in img_names:
        #    os.remove("C://Users//al//Desktop//Deep Learning//NLP//images//" + img)
        
        return note, r
    
    def getBasic(self, r, c, actual_labels):
        selector = Selector(text=r)
        labels = selector.xpath("//div[@class='choose-con']//dt")
        comments = selector.xpath("//div[@class='choose-con']//dd")
        h = etree.HTML(r)
        otime = h.xpath("//div[@class='title-name name-width-01']/b/text()")
        platform = h.xpath("//div[@class='title-name name-width-01']/text()")
        views = h.xpath("//span[@class='fn-left font-arial mr-20']/span[@id='koubeipv']/text()")
        support = h.xpath("//div[@class='help']/span[@class='fn-left font-arial']/label/text()")
        typeofcar = h.xpath("//div[@class='subnav-title-name']/a/text()")
        c['发表时间'].append(selective(otime))
        if len(platform) != 0:
            c['发表平台'].append(platform[-1].split('：')[-1])
        else:
            c['发表平台'].append(-1)
        c['浏览量'].append(selective(views))
        c['支持数'].append(selective(support))
        c['车型'].append(selective(typeofcar))
        
        labels_list = []
        comments_list = []
        for i in range(len(labels)):
            note = labels[i].xpath('string(.)').extract()[0]
            note = note.replace('\xa0', '')
            note = note.replace(' ', '')
            note = note.replace('\n', '')
            note = note.replace('\t', '')
            labels_list.append(note)
        for i in range(len(comments)):
            note = comments[i].xpath('string(.)').extract()[0]
            note = note.replace('\xa0', '')
            note = note.replace('   ', '')
            note = note.replace('\n', '')
            note = note.replace('\t', '')
            comments_list.append(note)
        #print(labels_list, comments_list)
        if len(labels) == len(comments):
            t = dict(zip(labels_list, comments_list))
            for label in actual_labels:
                if label in labels_list:
                    c[label].append(t[label])
                else:
                    c[label].append('-1')
        else:
            for label in actual_labels:
                c[label].append('-1')
        return c 

def selective(xpath_list):
    if len(xpath_list) == 0:
        return -1
    else:
        return xpath_list[0]

EV_comment_urls = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\url_data\koubei_urls\EV_urls_")
PHEV_comment_urls = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\url_data\koubei_urls\PHEV_urls_")
EXEV_comment_urls = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\url_data\koubei_urls\EXEV_urls_")

existed_ev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\comment_data\EV")
existed_phev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\comment_data\PHEV")
existed_exev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\comment_data\EXEV")

t_ev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\t_data\EV")
t_phev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\t_data\PHEV")
t_exev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\t_data\EXEV")

error_ev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\t_data\EV\error")
error_phev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\t_data\PHEV\error")
error_exev_files = os.listdir(r"C:\Users\al\Desktop\Deep Learning\NLP\Ahome_\t_data\EXEV\error")

auto = AutoSpider()

LABELS = ['动力', '购买时间', '裸车购买价', '常规续航里程冬季续航里程', '购买车型', '耗电量', '购买地点', '油耗目前行驶', '目前行驶', '操控', '冬季续航里程', '能耗', '舒适性', '油耗', '内饰', '常规续航里程', '油耗耗电量', '性价比', '油耗耗电量目前行驶', '空间', '购车经销商', '购车目的', '外观', '耗电量目前行驶']

for filename in EV_comment_urls:
    if filename.endswith('txt') and filename not in existed_ev_files:
        
        path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//url_data//koubei_urls//EV_urls_//" + filename
        save_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//comment_data//EV//" + filename
        t_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//t_data//EV//" + filename
        error_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//t_data//EV//error//" + filename
        
        print('=====================')
        print(filename)
        print('---------------------')
        
        if filename in t_ev_files:
            print('read t_data')
            with open(t_path, encoding='utf-8') as f:
                t_data = eval(f.read())
            index = len(t_data['comment'])
        else:
            index = 0      
        print('length of t_data:{}'.format(index))
        flag = index + 1
        
        if flag == 1:
            c = defaultdict(list)
            error_num = 0
        else:
            c = t_data
            
            print('read error url num')
            if filename in error_ev_files:
                with open(error_path, encoding='utf-8') as f:
                    error_num = int(f.read())
                index += error_num
                flag += error_num
            else:
                error_num = 0
            print('error url num:{}'.format(error_num))

        with open(path) as f:
            comment_urls = f.read().split('\n')
         
        url_num = len(comment_urls)
        for comment_url in comment_urls[index:]:
            
            print('---------%d / %d----------'%(flag, url_num))
            stime = datetime.datetime.now()
            print(datetime.datetime.now())
            comment_url = 'https:' + comment_url
            note, r = auto.getNote(filename.split('.')[0], comment_url)
            if note != 0:
                c['comment'].append(note)
                c = auto.getBasic(r, c, LABELS)
                #print(str(dict(c)))
                if flag % 20 == 0:
                    with open(t_path, 'w', encoding='utf-8') as ft:
                        s = str(dict(c))
                        ft.write(s)
                    with open(error_path, 'w', encoding='utf-8') as f:
                        f.write(str(error_num))
            else:
                error_num += 1
                    
            flag += 1
            print(str(datetime.datetime.now() - stime))
        with open(save_path, 'w', encoding='utf-8') as f:
            s = str(dict(c))
            f.write(s)
        with open(error_path, 'w', encoding='utf-8') as f:
            f.write(str(error_num))    

for filename in PHEV_comment_urls:
    if filename.endswith('txt') and filename not in existed_phev_files:
        
        path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//url_data//koubei_urls//PHEV_urls_//" + filename
        save_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//comment_data//PHEV//" + filename
        t_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//t_data//PHEV//" + filename
        error_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//t_data//PHEV//error//" + filename
        print('=====================')
        
        print(filename)
        print('---------------------')
        
        if filename in t_phev_files:
            print('read t_data')
            with open(t_path, encoding='utf-8') as f:
                t_data = eval(f.read())
            index = len(t_data['comment'])
        else:
            index = 0      
        print('length of t_data:{}'.format(index))
        flag = index + 1
        
        if flag == 1:
            c = defaultdict(list)
            error_num = 0
        else:
            c = t_data
        
            print('read error url num')
            if filename in error_phev_files:       
                with open(error_path, encoding='utf-8') as f:
                    error_num = int(f.read())
                index += error_num
                flag += error_num
            else:
                error_num = 0    
            print('error url num:{}'.format(error_num))

        with open(path) as f:
            comment_urls = f.read().split('\n')
         
        url_num = len(comment_urls)
        for comment_url in comment_urls[index:]:
            print('---------%d / %d----------'%(flag, url_num))
            stime = datetime.datetime.now()
            print(stime)
            comment_url = 'https:' + comment_url
            note, r = auto.getNote(filename.split('.')[0], comment_url)
            if note != 0:
                c['comment'].append(note)
                c = auto.getBasic(r, c, LABELS)
                if flag % 20 == 0:
                    with open(t_path, 'w', encoding='utf-8') as ft:
                        s = str(dict(c))
                        ft.write(s)
                    with open(error_path, 'w', encoding='utf-8') as f:
                        f.write(str(error_num))
            else:
                error_num += 1          
                    
            flag += 1
            print(str(datetime.datetime.now() - stime))
        with open(save_path, 'w', encoding='utf-8') as f:
            s = str(dict(c))
            f.write(s)
        with open(error_path, 'w', encoding='utf-8') as f:
            f.write(str(error_num))   
            
            
for filename in EXEV_comment_urls:
    if filename.endswith('txt') and filename not in existed_exev_files:
        
        path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//url_data//koubei_urls//EXEV_urls_//" + filename
        save_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//comment_data//EXEV//" + filename
        t_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//t_data//EXEV//" + filename
        error_path = "C://Users//al//Desktop//Deep Learning//NLP//Ahome_//t_data//EXEV//error//" + filename
        print('=====================')
        
        print(filename)
        print('---------------------')
        
        if filename in t_exev_files:
            print('read t_data')
            with open(t_path, encoding='utf-8') as f:
                t_data = eval(f.read())
            index = len(t_data['comment'])
        else:
            index = 0      
        print('length of t_data:{}'.format(index))
        flag = index + 1
        
        if flag == 1:
            c = defaultdict(list)
            error_num = 0
        else:
            c = t_data
            
            print('read error url num')
            if filename in error_exev_files:                
                with open(error_path, encoding='utf-8') as f:
                    error_num = int(f.read())                
                index += error_num
                flag += error_num
            else:
                error_num = 0    
            print('error url num:{}'.format(error_num))

        with open(path) as f:
            comment_urls = f.read().split('\n')
         
        url_num = len(comment_urls)
        for comment_url in comment_urls[index:]:
            print('---------%d / %d----------'%(flag, url_num))
            stime = datetime.datetime.now()
            print(stime)
            comment_url = 'https:' + comment_url
            note, r = auto.getNote(filename.split('.')[0], comment_url)
            if note != 0:
                c['comment'].append(note)
                c = auto.getBasic(r, c, LABELS)
                if flag % 20 == 0:
                    with open(t_path, 'w', encoding='utf-8') as ft:
                        s = str(dict(c))
                        ft.write(s)
                    with open(error_path, 'w', encoding='utf-8') as f:
                        f.write(str(error_num))
            else:
                error_num += 1       
                    
            flag += 1
            print(str(datetime.datetime.now() - stime))
        with open(save_path, 'w', encoding='utf-8') as f:
            s = str(dict(c))
            f.write(s)
        with open(error_path, 'w', encoding='utf-8') as f:
            f.write(str(error_num))   
        
        
        