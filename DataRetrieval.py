# -*- coding: utf-8 -*-
import mechanize
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
import numpy as np

StateIdARR = []
BJSPopulationGroupIdARR = []

CrimeCrossIdARR = []
DataTypeARR = []
YearStartARR = []
YearEndARR = []

BJSPGI_arr = ['12','13','18','19']

"""*** IMPORTANT : Items that can be changed are marked with comments like this #~~~~~~ on the lines above and below """


def first_page(br,state_num):

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
	    	#print(" name=%s values=%s" % (item.name, str([label.text  for label in item.get_labels()])))

	#print(StateId.value)
	#print(StateId)  # selected value is starred
	#StateId.value = ["2"]
	#print(StateId)
	br[StateId.name] = [str(state_num)]  
	br[BJSPopulationGroupId.name] = ['12','13','18','19']
	return br

def fill_crime_cross_ids(br):
	second = br.submit()
	#print(second)
	response = second
	CCI_arr = []
	br.form = list(br.forms())[0]
	#print(br.form)
	CrimeCrossId = br.form.find_control("CrimeCrossId")
	if CrimeCrossId.type == "select":  # means it's class ClientForm.SelectControl
	    for item in CrimeCrossId.items:
	    	CCI_arr.append(item.name)
	return CCI_arr

def second_page(br,police_id):
	#sprint(br)
	second = br.submit()
	#print('reached after submit')
	response = second

	br.form = list(br.forms())[0]  
	CrimeCrossId = br.form.find_control("CrimeCrossId")
	if CrimeCrossId.type == "select":  # means it's class ClientForm.SelectControl
	    for item in CrimeCrossId.items:
	    	for label in item.get_labels():
	    		CrimeCrossIdARR.append(label.text)
	CrimeCrossIdARR.append(None) 
	 		
	DataType = br.form.find_control("DataType")
	if DataType.type == "select": 
	    for item in DataType.items:
	    	for label in item.get_labels():
	    		DataTypeARR.append(label.text)
	#DataTypeARR.append(None)

	YearStart = br.form.find_control("YearStart")
	if YearStart.type == "select": 
	    for item in YearStart.items:
	    	for label in item.get_labels():
	    		YearStartARR.append(label.text)
	YearStartARR.append(None)

	YearEnd = br.form.find_control("YearEnd")
	if DataType.type == "select": 
	    for item in YearEnd.items:
	    	for label in item.get_labels():
	    		YearEndARR.append(label.text)
	YearEndARR.append(None)
	#print(DataTypeARR)
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	br[DataType.name] = ['1','2']	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	if police_id != None:
		br[CrimeCrossId.name] = [str(police_id)] 
	
	table = br.submit()
	html = str(table.read())
	return html

def alter_html(html):
	html_one_split = html.split('<DIV CLASS="indent">')[2]
	caption = html_one_split.split("Crime reported by ")[1].split("</CAPTION>")[0]
	#print(caption)
	html_two_split = html_one_split.split('<hr NOSHADE>')[1]
	df = pd.read_html("<TABLE>" + html_two_split, header = 0)
	df = df[0]

	df.columns = ['year','months-reporting','population-coverage','VC_violent-crime-total',
				  'VC_murder-and-nonnegligent-manslaughter','VC_forcible-rape','VC_robbery',
				  'VC_aggravated-assault','PC_property-crime-total','PC_burglary','PC_larceny-theft',
				  'PC_motor-vehicle-theft']
	#,'PCR_property-crime-total','PCR_burglary','PCR_larceny-theft','PCR_motor-vehicle-theft'
	both = caption.replace('\r\n','').replace('        ','').replace('Sheriff Department','').replace('Sheriff Deptartment','')
	df['county-name'] = both.split(', ')[0]
	df['state'] = both.split(', ')[1]
	#print(df)
	return df

def main():
	#create dataframe with appropriate columns by running 
	#functions for the first police id/state, and deleting all row values
	columns = ['year','months-reporting','population-coverage','VC_violent-crime-total',
			  'VC_murder-and-nonnegligent-manslaughter','VC_forcible-rape','VC_robbery',
			  'VC_aggravated-assault','PC_property-crime-total','PC_burglary','PC_larceny-theft',
			  'PC_motor-vehicle-theft']
	index = np.arange(1) # array of numbers for the number of samples
	large_df = pd.DataFrame(columns=columns, index = index)
	#df is now an empty dataframe with [0 rows x 22 columns]
	#~~~~~~~~~~~~~~~~~~
	SI_arr = [1,3,4,5,6,8,10,11,12,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,32,33,34,36,37,38,41,42,43,44,45,47,48,49,50,51] #set to [range(1,52)] when we want all data
	print(len(SI_arr))
	#Manually edited SI_arr with StateId's that aren't messed up. 
	#~~~~~~~~~~~~~~~~~~
	df_list = []
	for num in SI_arr:
		print('STARTING NEW STATE : ', num)
		br = mechanize.Browser()
		br.set_handle_robots(False)  
		br.set_handle_refresh(False) 
		response = br.open('https://www.ucrdatatool.gov/Search/Crime/Local/JurisbyJuris.cfm')
		altered_br = first_page(br, str(num))
		#print(altered_br)
		CCI_arr = fill_crime_cross_ids(first_page(br, str(num)))
		#print('FILLED CCI_arr : ', num)
		#print(CCI_arr)
		counter = 1
		for police_id in CCI_arr:

			br = mechanize.Browser()
			br.set_handle_robots(False)  
			br.set_handle_refresh(False) 
			response = br.open('https://www.ucrdatatool.gov/Search/Crime/Local/JurisbyJuris.cfm')
			#print('moving on after new BR element')
			html = second_page(first_page(br, str(num)),police_id)
			df = alter_html(html)
			#print(df)
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			#df.to_csv('data.csv', encoding='utf-8')
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			#large_df.append(df)
			df_list.append(df)
			print('DONE WITH POLICE ID NUMBER : ', counter)
			counter += 1
		#print('reset CCI_arr')
		CCI_arr = []
	result = pd.concat(df_list)
	print(result)
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	result.to_csv('final.csv', encoding='utf-8')
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

main()
