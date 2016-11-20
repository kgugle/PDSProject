# -*- coding: utf-8 -*-
import mechanize
from bs4 import BeautifulSoup
import pandas as pd
import html5lib

br = mechanize.Browser()
#br.set_all_readonly(False)    # don't need to write to anything
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this

response = br.open('https://www.ucrdatatool.gov/Search/Crime/Local/JurisbyJurisStepTwo.cfm')
#print(response.read())
response1 = br.response()  
#print(response1.read())
#for form in br.forms():
#    print("Form name:", form.name)
#    print(form)

StateIdARR = []
BJSPopulationGroupIdARR = []
br.form = list(br.forms())[0]  # use when form is unnamed
StateId = br.form.find_control("StateId")
if StateId.type == "select":  # means it's class ClientForm.SelectControl
    for item in StateId.items:
    	for label in item.get_labels():
    		StateIdARR.append(label.text)
    	#print(" name=%s values=%s" % (item.name, str([label.text  for label in item.get_labels()])))

BJSPopulationGroupId = br.form.find_control("BJSPopulationGroupId")
if BJSPopulationGroupId.type == "select": 
    for item in BJSPopulationGroupId.items:
    	for label in item.get_labels():
    		BJSPopulationGroupIdARR.append(label.text)

#print(StateId.value)
#print(StateId)  # selected value is starred
#StateId.value = ["2"]
#print(StateId)
#br[StateId.name] = ["4"]  

second = br.submit()
response = second
#print(response.read())
'''for form in br.forms():
    print("Form name:", form.name)
    print(form)
'''
CrimeCrossIdARR = []
DataTypeARR = []
YearStartARR = []
YearEndARR = []

br.form = list(br.forms())[0]  
CrimeCrossId = br.form.find_control("CrimeCrossId")
if CrimeCrossId.type == "select":  # means it's class ClientForm.SelectControl
    for item in CrimeCrossId.items:
    	for label in item.get_labels():
    		CrimeCrossIdARR.append(label.text)

DataType = br.form.find_control("DataType")
if DataType.type == "select": 
    for item in DataType.items:
    	for label in item.get_labels():
    		DataTypeARR.append(label.text)

YearStart = br.form.find_control("YearStart")
if YearStart.type == "select": 
    for item in YearStart.items:
    	for label in item.get_labels():
    		YearStartARR.append(label.text)

YearEnd = br.form.find_control("YearEnd")
if DataType.type == "select": 
    for item in YearEnd.items:
    	for label in item.get_labels():
    		YearEndARR.append(label.text)

br[DataType.name] = ["1"]
table = br.submit()
html = str(table.read())

html_one_split = html.split('<DIV CLASS="indent">')[2]
caption = html_one_split.split("Crime reported by ")[1].split("</CAPTION>")[0]
print(caption)
html_two_split = html_one_split.split('<hr NOSHADE>')[1]
df = pd.read_html("<TABLE>" + html_two_split, header = 0)
df = df[0]
df.columns = ['year','mo-reporting','pop-cov','v-cr-total','mur-nonneg-man','for-rape','robbery','agg-assault']
df['county'] = caption.replace('\r\n','').replace('        ','')

print(df)
