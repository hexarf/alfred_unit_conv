#!/usr/bin/python
# -*- coding: utf-8 -*-

#====================================================================================================
#	Date : 2013.7.02
#	Unit Converter
#	Version : 0.1
#	hexarf@gmail.com
#	http://twitter.com/hexarf
#====================================================================================================

#import sys
import re
import json
import sys
import alfred
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

##string divide func
def string_div(target_str):
#	target_str = "-33320202.23inch"
	number_partten = r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
	number_list = re.findall(number_partten, target_str)
#	param = re.sub(number_partten, '', target_str)
#	unit = param.strip(' \t\n\r')

	if (len(number_list)<1):
		return False
	else:
		number = number_list[0];
		unit = re.sub(number_list[0], '', target_str)
		return {'number':number, 'unit':unit.strip(' \t\n\r')}



def convert(query):
	#Input data
	query2 = unicodedata.normalize('NFC', query)

	parsed_data = string_div(query2)
#	print(parsed_data)
	unit = parsed_data['unit']
	number = parsed_data['number']

	#Load convert data file
	try:
		f = open("unit.json",'r')
	except:
		print("ERROR:can't create file")

	unit_data = json.load(f, encoding='utf-8')

	#print(unit_data['inch'])

	#Data check & convert
	output_list = []
#	item = alfred.Item({'uid': alfred.uid(1), 'arg': 'some arg', 'valid': 'no'}, unit, number, ('someicon.png', {'type': 'filetype'}))
#	output_list.append(item)

	for unit_group in unit_data:
		inputs = unit_data[unit_group]['input']
		outputs = unit_data[unit_group]['output']

		for input_keyword in inputs:
			if input_keyword==unit:
				for output_unit in outputs:

					#convert calc type check
					find_index = outputs[output_unit].find("?")
					if find_index>=0:
						#special pattern
						float_str = eval(outputs[output_unit].replace('?',number));
						float_data = float(float_str)
					else:
						#normal pattern
						float_data = float(outputs[output_unit]) * float(number)

					#output_data = {'number':str(float_data),'unit':output_unit}
					output_str = str(float_data)+output_unit
					item = alfred.Item({'uid':alfred.uid(len(output_list)+1),'arg':output_str,'valid':'yes'},output_str,query,('icon.png',{'type':'png'}))
					output_list.append(item)
#	print(output_list)

	xml = alfred.xml(output_list)
	alfred.write(xml)



#Test code
#convert(u"293kg")

