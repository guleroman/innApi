#!flask/bin/python
from flask import Flask, jsonify, request, json, send_file
from docxtpl import DocxTemplate
from num2words import num2words   
import innApi_v2, datetime, uuid
import pandas as pd
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/companies/<int:provider_inn>/documents', methods=['POST'])
def main3(provider_inn):
    provider_inn = str(provider_inn)

    with open('company.json', 'r', encoding='utf-8') as fh: #открываем файл с данными о исполнителях на чтение
        company = json.load(fh)

    with open("iteration.json", "r") as read_file: #открываем файл с количеством оформленных документов (итератор)
        num = json.load(read_file)


    #Данные о исполнителе
    try:
        provider_bank = company[provider_inn]['bank']
        provider_kpp = company[provider_inn]['kpp']
        provider_ogrn = company[provider_inn]['ogrn']
        provider_name = company[provider_inn]['name']
        provider_bik = company[provider_inn]['bik']
        provider_account1 = company[provider_inn]['account1']
        provider_account2 = company[provider_inn]['account2']
        provider_address = company[provider_inn]['address']
        provider_nds = company[provider_inn]['nds']
        print('________Cache!________')
    except KeyError:
        data_provider = innApi_v2.mainn(provider_inn)
        data_provider = data_provider[0]
        provider_bank = ''
        provider_kpp = data_provider['data']['kpp']
        provider_ogrn = data_provider['data']['ogrn']
        provider_name = data_provider['value']
        provider_bik = ''
        provider_account1 = ''
        provider_account2 = ''
        provider_address = data_provider['data']['address']['value']
        provider_nds = 1
        print('________DADATA_provider!________')

        #Кешируем данные о Исполнителе
        cacheProviderData = {str(provider_inn): 
            {
            "bank":"",
            "inn":provider_inn,
            "kpp":provider_kpp,
            "ogrn":provider_ogrn,
            "name":provider_name,
            "bik":"",
            "account1":"",
            "account2":"",
            "address":provider_address,
            "nds":1
            }}
        company.update(cacheProviderData)
        with open("company.json", "w", encoding='utf-8') as write_file:
            json.dump(company, write_file)

    #Создаем переменные по налогам, исходя из данных Исполнителя
    if provider_nds == 1:
        nds = 20
        nds_2 = "20 %"
        nds_3 = "НДС " + nds_2
        nds_6 = ''
    else:
        nds = 0
        nds_2 = '-'
        nds_3 = ''
        nds_4 = ''
        nds_5 = ''
        nds_6 = 'Стоимость услуг НДС не облагается в связи с применением Исполнителем упрощенной системы налогообложения.'
    
    # Поступающие данные в POST запросе
    #Данные о заказчике и перечне услуг,стоимости и тд.
    data_post = json.loads(request.data) 
    client_inn = data_post['client_inn'] # инн - заказчика
    client_kpp = data_post['client_kpp']
    template_code = data_post['template_code']
    product_name = data_post['payload']['product_name']
    tariff_name = data_post['payload']['tariff_name']
    tariff_users_count = data_post['payload']['tariff_users_count']
    tariff_phone_numbers_count = data_post['payload']['tariff_phone_numbers_count']
    payment_frequency = data_post['payload']['payment_frequency']

    #Получаем данные от DaData
    data,key = innApi_v2.mainn(client_inn)

    #Заполняемм таблицу - товар/цена/стоимость и тд.
    summa = 0
    table = pd.DataFrame({'t_num':[],'t_products':[],'t_kol':[],'t_ed':[],'t_nds':[],'t_price':[],'t_sum':[],'t_payment_frequency':[]})
    table = table[['t_num','t_products','t_kol','t_ed','t_nds','t_price','t_sum','t_payment_frequency']] 
    for i in range(len(data_post['payload']['invoice'])):
        table.loc[len(table)] = [
            str(len(table)+1),
            data_post['payload']['invoice'][i]['service_name'],
            str(data_post['payload']['invoice'][i]['quantity']),
            data_post['payload']['invoice'][i]['unit'],
            nds_2,
            '{0:.2f}'.format(data_post['payload']['invoice'][i]['cost']),
            '{0:.2f}'.format((data_post['payload']['invoice'][i]['quantity'] * data_post['payload']['invoice'][i]['cost'])),
            payment_frequency]
        summa = summa + (data_post['payload']['invoice'][i]['quantity'] * data_post['payload']['invoice'][i]['cost'])
    
    #Общая стоимость заказа
    if provider_nds == 1:
        nds_4 = round(summa / 1.2 * 0.2,2)
        nds_5 = ', в том числе НДС:' + str(nds_4)
    summa_str = '{0:.2f}'.format(summa)

    #Дозапоняем пустыми значениями
    for i in range(len(table),5):
        table.loc[len(table)] = [
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '']

    #Дополнительное КПП клиента
    if client_kpp == '':
        client_kpp = data['data']['kpp']


    #Генерация документов
    ##Счет на оплату
    #_____________________________________________________ 
    def write_invoice():
        doc = DocxTemplate("tpl_invoice.docx")
        context = { 
            'var0' : nds,
            'var1' : provider_bank,
            'var2' : provider_inn,
            'var3' : provider_kpp,
            'var4' : provider_name,
            'var5' : provider_bik,
            'var6' : provider_account1,
            'var7' : provider_account2,
            'var8' : num['number'],
            'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
            'var10' : provider_address,
            'var11' : data['value'],
            'var12' : data['data']['inn'],
            'var13' : data['data']['kpp'],
            'var14' : data['data']['address']['value'],
            'var15' : nds_3,
            'var16' : (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%d.%m.%Y'),
            
            'n1' : table.iloc[0]['t_num'],
            'n2' : table.iloc[1]['t_num'],
            'n3' : table.iloc[2]['t_num'],
            'n4' : table.iloc[3]['t_num'],
            'n5' : table.iloc[4]['t_num'],
            
            'product1' : table.iloc[0]['t_products'],
            'product2' : table.iloc[1]['t_products'],
            'product3' : table.iloc[2]['t_products'],
            'product4' : table.iloc[3]['t_products'],
            'product5' : table.iloc[4]['t_products'],
            
            'kol1' : table.iloc[0]['t_kol'],
            'kol2' : table.iloc[1]['t_kol'],
            'kol3' : table.iloc[2]['t_kol'],
            'kol4' : table.iloc[3]['t_kol'],
            'kol5' : table.iloc[4]['t_kol'],
            
            'ed1' : table.iloc[0]['t_ed'],
            'ed2' : table.iloc[1]['t_ed'],
            'ed3' : table.iloc[2]['t_ed'],
            'ed4' : table.iloc[3]['t_ed'],
            'ed5' : table.iloc[4]['t_ed'],

            'nds1' : table.iloc[0]['t_nds'],
            'nds2' : table.iloc[1]['t_nds'],
            'nds3' : table.iloc[2]['t_nds'],
            'nds4' : table.iloc[3]['t_nds'],
            'nds5' : table.iloc[4]['t_nds'],
            
            'price1' : table.iloc[0]['t_price'],
            'price2' : table.iloc[1]['t_price'],
            'price3' : table.iloc[2]['t_price'],
            'price4' : table.iloc[3]['t_price'],
            'price5' : table.iloc[4]['t_price'],
            
            'summ1' : table.iloc[0]['t_sum'],
            'summ2' : table.iloc[1]['t_sum'],
            'summ3' : table.iloc[2]['t_sum'],
            'summ4' : table.iloc[3]['t_sum'],
            'summ5' : table.iloc[4]['t_sum'],

            'var17' : nds_4,
            'var18' : summa_str,
            'var19' : num2words(int(summa), lang='ru')
            }
        doc.render(context)
        doc.save("doc_1_"+key+".docx")

    ##Акт о проделанных работах
    #_____________________________________________________
    def write_act():
        doc = DocxTemplate("tpl_invoice_2.docx")
        context = {
            'var2' : provider_inn,
            'var3' : provider_kpp,
            'var4' : provider_name,
            'var8' : num['number'],
            'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
            'var10' : provider_address,
            'var11' : data['value'],
            'var12' : data['data']['inn'],
            'var13' : data['data']['kpp'],
            'var14' : data['data']['address']['value'],
            'var15' : nds_3,
            
            'n1' : table.iloc[0]['t_num'],
            'n2' : table.iloc[1]['t_num'],
            'n3' : table.iloc[2]['t_num'],
            'n4' : table.iloc[3]['t_num'],
            'n5' : table.iloc[4]['t_num'],
            
            'product1' : table.iloc[0]['t_products'],
            'product2' : table.iloc[1]['t_products'],
            'product3' : table.iloc[2]['t_products'],
            'product4' : table.iloc[3]['t_products'],
            'product5' : table.iloc[4]['t_products'],
            
            'kol1' : table.iloc[0]['t_kol'],
            'kol2' : table.iloc[1]['t_kol'],
            'kol3' : table.iloc[2]['t_kol'],
            'kol4' : table.iloc[3]['t_kol'],
            'kol5' : table.iloc[4]['t_kol'],
            
            'ed1' : table.iloc[0]['t_ed'],
            'ed2' : table.iloc[1]['t_ed'],
            'ed3' : table.iloc[2]['t_ed'],
            'ed4' : table.iloc[3]['t_ed'],
            'ed5' : table.iloc[4]['t_ed'],

            'nds1' : table.iloc[0]['t_nds'],
            'nds2' : table.iloc[1]['t_nds'],
            'nds3' : table.iloc[2]['t_nds'],
            'nds4' : table.iloc[3]['t_nds'],
            'nds5' : table.iloc[4]['t_nds'],
            
            'price1' : table.iloc[0]['t_price'],
            'price2' : table.iloc[1]['t_price'],
            'price3' : table.iloc[2]['t_price'],
            'price4' : table.iloc[3]['t_price'],
            'price5' : table.iloc[4]['t_price'],
            
            'summ1' : table.iloc[0]['t_sum'],
            'summ2' : table.iloc[1]['t_sum'],
            'summ3' : table.iloc[2]['t_sum'],
            'summ4' : table.iloc[3]['t_sum'],
            'summ5' : table.iloc[4]['t_sum'],

            'var17' : nds_4,
            'var18' : summa_str,
            'var19' : num2words(int(summa), lang='ru')
            }
        doc.render(context)
        doc.save("doc_2_"+key+".docx")

    ##Договор о предоставлении услуг
    #_____________________________________________________
    def write_contract():
        doc = DocxTemplate("tpl_invoice_3.docx")
        context = {
            'var1' : provider_bank,
            'var2' : provider_inn,
            'var3' : provider_kpp,
            'var4' : provider_name,
            'var5' : provider_bik,
            'var6' : provider_account1,
            'var7' : provider_account2,
            'var8' : num['number'],
            'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
            'var10' : provider_address,
            'var11' : data['value'],
            'var12' : data['data']['inn'],
            'var13' : data['data']['kpp'],
            'var14' : data['data']['address']['value'],
            
            'n1' : table.iloc[0]['t_num'],
            'n2' : table.iloc[1]['t_num'],
            'n3' : table.iloc[2]['t_num'],
            'n4' : table.iloc[3]['t_num'],
            'n5' : table.iloc[4]['t_num'],
            
            'product1' : table.iloc[0]['t_products'],
            'product2' : table.iloc[1]['t_products'],
            'product3' : table.iloc[2]['t_products'],
            'product4' : table.iloc[3]['t_products'],
            'product5' : table.iloc[4]['t_products'],
            
            'kol1' : table.iloc[0]['t_kol'],
            'kol2' : table.iloc[1]['t_kol'],
            'kol3' : table.iloc[2]['t_kol'],
            'kol4' : table.iloc[3]['t_kol'],
            'kol5' : table.iloc[4]['t_kol'],
            
            'ed1' : table.iloc[0]['t_ed'],
            'ed2' : table.iloc[1]['t_ed'],
            'ed3' : table.iloc[2]['t_ed'],
            'ed4' : table.iloc[3]['t_ed'],
            'ed5' : table.iloc[4]['t_ed'],

            'nds1' : table.iloc[0]['t_nds'],
            'nds2' : table.iloc[1]['t_nds'],
            'nds3' : table.iloc[2]['t_nds'],
            'nds4' : table.iloc[3]['t_nds'],
            'nds5' : table.iloc[4]['t_nds'],
            
            'price1' : table.iloc[0]['t_price'],
            'price2' : table.iloc[1]['t_price'],
            'price3' : table.iloc[2]['t_price'],
            'price4' : table.iloc[3]['t_price'],
            'price5' : table.iloc[4]['t_price'],
            
            'summ1' : table.iloc[0]['t_sum'],
            'summ2' : table.iloc[1]['t_sum'],
            'summ3' : table.iloc[2]['t_sum'],
            'summ4' : table.iloc[3]['t_sum'],
            'summ5' : table.iloc[4]['t_sum'],

            'var18' : summa_str,
            'var19' : num2words(int(summa), lang='ru'),
            
            'var20' : data['data']['ogrn'],
            'var21' : provider_ogrn,
            'var22' : nds_5,
            'var23' : nds_6
            }
        doc.render(context)
        doc.save("doc_3_"+key+".docx")
    
    ##Договор о предоставлении услуг(Ростелеком)
    #_____________________________________________________
    def write_contract_RT():
        doc = DocxTemplate("tpl_invoice_4.docx")
        context = {
            'var0' : datetime.datetime.today().strftime("%d.%m.%Y"),
            'var1' : data['data']['name']['full_with_opf'],
            'var2' : data['data']['address']['data']["city_with_type"],
            'var3' : data['data']['management']['name'].split()[0],
            'var4' : data['data']['management']['name'].split()[1],
            'var5' : data['data']['management']['name'].split()[2],
            'var6' : data['data']['address']['data']['postal_code'],
            'var7' : data['data']['address']['data']['region'],
            'var8' : data['data']['address']['data']['city_district'],
            'var9' : data['data']['address']['data']['city'],
            'var10' : data['data']['address']['data']['street_with_type'],
            'var11' : data['data']['address']['data']['house'],
            'var12' : data['data']['address']['value'],
            'var13' : data['data']['ogrn'],
            'var14' : data['data']['inn'],
            'var15' : client_kpp,
            'var16' : data['data']['okpo'],
            'var17' : data['data']['management']['name'],
            'var18' : product_name,
            'var19' : num['number'],
            'var20' : tariff_name,
            'var21' : tariff_users_count,
            'var22' : tariff_phone_numbers_count,

            'product1' : table.iloc[0]['t_products'],
            'product2' : table.iloc[1]['t_products'],
            'product3' : table.iloc[2]['t_products'],
            'product4' : table.iloc[3]['t_products'],
            'product5' : table.iloc[4]['t_products'],
            
            'kol1' : table.iloc[0]['t_kol'],
            'kol2' : table.iloc[1]['t_kol'],
            'kol3' : table.iloc[2]['t_kol'],
            'kol4' : table.iloc[3]['t_kol'],
            'kol5' : table.iloc[4]['t_kol'],
            
            'ed1' : table.iloc[0]['t_ed'],
            'ed2' : table.iloc[1]['t_ed'],
            'ed3' : table.iloc[2]['t_ed'],
            'ed4' : table.iloc[3]['t_ed'],
            'ed5' : table.iloc[4]['t_ed'],

            'summ1' : table.iloc[0]['t_sum'],
            'summ2' : table.iloc[1]['t_sum'],
            'summ3' : table.iloc[2]['t_sum'],
            'summ4' : table.iloc[3]['t_sum'],
            'summ5' : table.iloc[4]['t_sum'],

            'payment1' : table.iloc[0]['t_payment_frequency'],
            'payment2' : table.iloc[1]['t_payment_frequency'],
            'payment3' : table.iloc[2]['t_payment_frequency'],
            'payment4' : table.iloc[3]['t_payment_frequency'],
            'payment5' : table.iloc[4]['t_payment_frequency'],

            }
        doc.render(context)
        doc.save("doc_4_"+key+".docx")


    ##Условия для создания шаблонов
    #_____________________________________________________
    if template_code == 'vpbx':
        write_contract_RT()
        responseJson = {"contractRT_url": "/getfile/doc_4_"+key+".docx"}
    else:
        responseJson = {"contract_url": "/getfile/doc_3_"+key+".docx","act_url": "/getfile/doc_2_"+key+".docx","invoice_url": "/getfile/doc_1_"+key+".docx"}
        write_invoice()
        write_act()
        write_contract()
    #Запись в историю
    #with open('history.json', 'r',encoding='utf-8') as fh: #открываем файл с данными о исполнителях на чтение
    #    history = json.load(fh)
    #cacheHistory = {str(provider_inn): 
    #    {
    #    "number": num['number'],
    #    "provider":provider_name,
    #    "client": data['value'],
    #    "act_url":"/getfile/doc_2_"+key+".docx",
    #    "contract_url":"/getfile/doc_3_"+key+".docx",
    #    "invoice_url":"/getfile/doc_1_"+key+".docx",
    #    "date_creation":datetime.datetime.today().strftime("%H:%M-%d.%m.%Y")
    #    }}
    #history.update(cacheHistory)    
    #with open("history.json", "w", encoding='utf-8') as write_file:
    #    json.dump(history, write_file)    

    #Плюсуем итератор количества оформленых документов
    num['number'] = num['number'] + 1
    with open("iteration.json", "w") as write_file:
        json.dump(num, write_file)

    #Формируем ответ    
    #responseJson = {"contractRT_url": "/getfile/doc_4_"+key+".docx","contract_url": "/getfile/doc_3_"+key+".docx","act_url": "/getfile/doc_2_"+key+".docx","invoice_url": "/getfile/doc_1_"+key+".docx"}
    return jsonify(responseJson)

#Точка входа для скачивания файлов
@app.route('/getfile/<name>')
def get_output_file(name):
    return send_file(name, as_attachment=True)

#@app.route('/api/companies/<int:provider_inn>/documents', methods=['GET'])
#def get_documents(provider_inn):
#    provider_inn = str(provider_inn)
#    table = pd.DataFrame({'Акт':[],'Договор':[],'Счет на оплату':[],'Дата создания':[],'Заказчик':[]})
#    table = table[['Заказчик','Акт','Договор','Счет на оплату','Дата создания']] 
#    for i in range(3):
#        table.loc[len(table)] = [float('{0:.2f}'.format(1000)),'12',11223344]    

if __name__ == '__main__':

    app.run(debug=False,host='0.0.0.0', port=5000)