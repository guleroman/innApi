import requests, bs4, sys, json

def mainn(inn):
	print (inn)
	def start(link2):
		all_info = []
		site = requests.get(link2)
		bb = bs4.BeautifulSoup(site.text, "html.parser")
		name_1 = bb.select('div.page-header h1') # Название организации/ИП
		name_2 = bb.select('.table.table-striped.table-hover td') # Значения из таблицы	
		return (name_1,name_2,all_info)


	def company(inn):
		link = 'https://огрн.онлайн/компании/?поиск='
		link2 = link + inn
		name_1, name_2,all_info = start(link2)
		name = name_1[0].getText().replace('\"','')
		
		for i in range(3,18,2):
			all_info = all_info + [name_2[i].getText().replace('\n','').replace('\r','').replace('  ','')]
		data = {
		"Название": name,
		"ОГРН": all_info[0],
		"Дата регистрации": all_info[1],
		"ИНН": all_info[2],
		"КПП": all_info[3],
		"ОКОПФ": all_info[4],
		"Юридический адрес": all_info[5],   
		"Регистрирующий орган": all_info[6]   
		}
		return (data)
		

	#inn = '7813054277'
	data = company(inn)
	#print (data)
	return (data)
		#return (a)
		#def personal():
		#	link = 'https://огрн.онлайн/люди/?инн='
		#	link2 = link + inn
		#	name_1, name_2 = start(link2)
		#	name = name_1[0].getText()
			
		#	for i in range(3,18,2):
		#		all_info = all_info + [name_2[i].getText().replace('\n','').replace('\r','').replace('  ','')]
		#	data = {
		#	"Название": name,
		#	"ОГРНИП:": all_info[0],
		#	"Дата регистрации": all_info[1],
		#	"ИНН": all_info[2],
		#	"КПП": all_info[3],
		#	"Регистрирующий орган:": all_info[4],
		#	"Гражданство": all_info[5],     
		#	}
		#	return (data)


		# Формируем словарь

		#print (data)

		# Производим запись в JSON файл
	#def writeJSON():
		#with open("data_file.json", "w") as write_file:
			#json.dump(data, write_file,ensure_ascii=False)
		#return (type(write_file))
	#writeJSON()
	#print(cc)			
			
if __name__ == "__main__":
	print (sys.argv[1])
	mainn(sys.argv[1])
