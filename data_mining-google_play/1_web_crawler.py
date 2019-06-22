# -*- coding: utf-8 -*-
"""
Created on Sun May 26 13:24:41 2019

@author: Xuan Yeh
"""

import time
from bs4 import BeautifulSoup
import sys, io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import *


f = open("store評論new.txt", 'w',encoding = 'utf8')
no_of_reviews = 1000

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
driver = webdriver.Chrome(r'C:\Users\samue\Anaconda3\Scripts\chromedriver.exe')

wait = WebDriverWait( driver, 10 )


# Append your app store urls here

urls = ["https://play.google.com/store/apps/details?id=com.garena.game.fctw"
#"https://play.google.com/store/apps/details?id=com.gamania.lineagem",
#"https://play.google.com/store/apps/details?id=com.lilithgame.roc.gp.tw",
#"https://play.google.com/store/apps/details?id=tw.txwy.and.wll"#,
#"https://play.google.com/store/apps/details?id=com.madhead.tos.zh",
#"https://play.google.com/store/apps/details?id=com.szckhd.jwgly.azfanti",
#"https://play.google.com/store/apps/details?id=com.more.laozi",
#"https://play.google.com/store/apps/details?id=com.garena.game.kgtw"
#"https://play.google.com/store/apps/details?id=com.bbgame.sgzapk.tw",
#"https://play.google.com/store/apps/details?id=com.nintendo.zaga"
#"https://play.google.com/store/apps/details?id=jp.naver.line.android",
#"https://play.google.com/store/apps/details?id=com.facebook.katana"
]

for url in urls:
    counter = 1
    driver.get(url)
    page = driver.page_source
    soup_expatistan = BeautifulSoup(page, "lxml")
    expatistan_table = soup_expatistan.find("h1", class_="AHFaub")
    f.write(expatistan_table.string+'$')
    print("App name: ", expatistan_table.string)
    expatistan_table = soup_expatistan.find("meta", itemprop="ratingValue")
    f.write(expatistan_table['content']+'$')
    print("Rating Value: ", expatistan_table['content'])
    f.write(('\n'))
    # open all reviews
    url = url+'&showAllReviews=true'
    driver.get(url)
    time.sleep(5) # wait dom ready
    for t in range(1,60):
        for i in range(1,6):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')#scroll to load other reviews
            time.sleep(1)
            
        page = driver.page_source
        soup_expatistan = BeautifulSoup(page, "lxml")
        driver.find_element_by_class_name("CwaK9").click()
        
    page = driver.page_source
    soup_expatistan = BeautifulSoup(page, "lxml")
    expand_pages = soup_expatistan.findAll("div", class_="d15Mdf")
                
    for expand_page in expand_pages:
        try:
            f.write(str(counter)+'$')
            #print("review："+str(counter))
            f.write(str(expand_page.find("span", class_="X43Kjb").text)+'$')
            #print("Author Name: ", str(expand_page.find("span", class_="X43Kjb").text))
            f.write(expand_page.find("span", class_="p2TkOb").text+'$')
            #print("Review Date: ", expand_page.find("span", class_="p2TkOb").text)
            reviewer_ratings = expand_page.find("div", class_="pf5lIe").find_next()['aria-label'];
            reviewer_ratings = reviewer_ratings.split('(')[0]
            reviewer_ratings = ''.join(x for x in reviewer_ratings if x.isdigit())
            f.write(reviewer_ratings+'$')
            #print("Reviewer Ratings: ", reviewer_ratings)
            f.write(str(expand_page.find("div", class_="UD7Dzf").text)+'$')
            #print("Review Body: ", str(expand_page.find("div", class_="UD7Dzf").text))
            f.write(('\n'))
            counter+=1
        except:
            pass
driver.close()
f.close()