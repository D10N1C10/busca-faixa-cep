# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 01:53:35 2020

@author: Dionicio
"""
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import json

url = "http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm"
UF_records = {} # [Localidade FaixaCEP Id]
visualize=False
printData=False

response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
option_elements=soup.findAll('option')
option_elements=option_elements[1:]
UFs=[]

for opt in option_elements:
    UFs.append(opt.get_text())

def getDataUF(driver,uf):
    select = Select(driver.find_element_by_name('UF'))
    select.select_by_visible_text(uf)
    driver.find_element_by_xpath("//input[@type='Submit' and @value='Buscar']").click()
    if visualize:
        driver.implicitly_wait(5) 
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    table = soup.findAll('table', attrs={"class":"tmptabela"})[1] 
    df= pd.read_html(str(table))[0]
    df=df.iloc[:,0:2]
    if printData:
        print(df) 
    df['Id']=0
    total_index=0
    for index,row in df.iterrows():
        total_index=total_index+1  
        df.loc[index,'Id'] =  uf + "-" + str(total_index)              
        
    while True:
        try:            
            driver.find_element_by_partial_link_text("Próxima").click()
            if visualize:
                driver.implicitly_wait(5) 
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            table = soup.findAll('table', attrs={"class":"tmptabela"})
            df2= pd.read_html(str(table))[0]
            df2=df2.iloc[:,0:2]
            if printData:
                print(df2) 
            df2['Id']=0
            for index,row in df2.iterrows():
                total_index=total_index+1  
                df2.loc[index,'Id'] =  uf + "-" + str(total_index)  
            df=pd.concat([df,df2])
        except Exception:
            break
    if printData:
        print(df)    
    driver.find_element_by_partial_link_text("Nova Consulta").click()    
    return df.to_dict('records')    

option = Options()
option.headless = True
if visualize:
    driver = webdriver.Firefox()
else:
    driver = webdriver.Firefox(options=option)
    
driver.get(url)

if visualize:
    driver.implicitly_wait(5) 
    
for uf in UFs:    
        UF_records[uf] = getDataUF(driver,uf)

driver.quit()
    
with open('records.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(UF_records, indent=4)
    jp.write(js)
