import requests, bs4, sys, json
import time
def mainn(inn):
    start_time = time.time()
    def start(link2):
        all_info = []
        site = requests.get(link2)
        bb = bs4.BeautifulSoup(site.text, "html.parser")
        name_1 = bb.select('div.page-header h1') # Название организации/ИП
        name_2 = bb.select('.table.table-striped.table-hover td') # Неструктурированная инфа из таблицы на сайте    
        return (name_1,name_2,all_info)

    #____________________________________________________<для выгрузки инфы по организации>
    
    def company(inn):
        link = 'https://огрн.онлайн/компании/?поиск='
        link2 = link + inn
        name_1, name_2,all_info = start(link2)
        
        if len(name_2) != 0:
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
        else:
            return (0)
    #____________________________________________________</для выгрузки инфы по организации>
    
    
    #____________________________________________________<для выгрузки инфы по ИП>

    def personel(inn):
        link = 'https://огрн.онлайн/люди/?инн='
        link2 = link + inn
        name_1, name_2,all_info = start(link2)
        
        if len(name_2) != 0:
            name = name_1[0].getText().rpartition(' ИНН')[0]
            for i in range(4,13,2):
                all_info = all_info + [name_2[i].getText().replace('\n','').replace('\r','').replace('  ','')]
            data = {
            "Название": name,
            "ОГРНИП": all_info[0],
            "Дата регистрации": all_info[1],
            "ИНН": all_info[2],
            "Регистрирующий орган": all_info[3],
            "Гражданство": all_info[4]  
            }
            return (data)
        else:
            return (0)
    #____________________________________________________</для выгрузки инфы по ИП>
    
    data = company(inn)
    if data == 0:
        data = personel(inn)
        if data == 0:
            print('Введен некорректный ИНН')
    
    print("--- %s seconds ---" % (time.time() - start_time))
    return (data)
            
if __name__ == "__main__":
    print (sys.argv[1])
    mainn(sys.argv[1])