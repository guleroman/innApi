#!flask/bin/python
from flask import Flask, jsonify, request, json, make_response, send_file
from docxtpl import DocxTemplate,InlineImage
from docx.shared import Mm
from num2words import num2words   
import innApi_v2, datetime
import pandas as pd
import time
import qrcode
import requests


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#ip = 'http://176.99.11.61:6060'
ip = 'http://localhost:5555'

def say_hii(input_file):#176.99.11.61
    link = ip + '/converter/'+input_file
    #try:
    requests.post(link, timeout=0.0001)
    #except:
    print ("Выполнил - ")

@app.route('/getfile/<name>')
def get_output_file(name):
    try:
        return send_file(name, as_attachment=True)
    except:
        return make_response(jsonify({"_status_code":404,"error":{"document":"file is not ready yet"}}),404)

@app.route('/api/companies/<int:provider_inn>/documents', methods=['POST'])
def main3(provider_inn):
    start_time = time.time()
    provider_inn = str(provider_inn)
    key = request.headers.get('key')
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
        #data_provider = data_provider[0]
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
       #nds_6 = ''
    else:
        nds = 0
        nds_2 = '-'
        nds_3 = ''
        nds_4 = ''
        #nds_5 = ''
        #nds_6 = 'Стоимость услуг НДС не облагается в связи с применением Исполнителем упрощенной системы налогообложения.'
    
    # Поступающие данные в POST запросе
    #Данные о заказчике и перечне услуг,стоимости и тд.
    data_post = json.loads(request.data) 
    client_inn = data_post['client_inn'] # инн - заказчика
    client_kpp = data_post['client_kpp']
    template_code = data_post['template_code']
    product_name = data_post['product_name']
    tariff_name = data_post['tariff_name']
    tariff_users_count = str(data_post['tariff_users_count'])
    payment_frequency = data_post['payment_frequency']
    tariff_notincluded_users_count = str(data_post['tariff_notincluded_users_count'])
    tariff_included_minuts_count = str(data_post['tariff_included_minuts_count'])
    tariff_abonent_number_abc = data_post['tariff_abonent_number_abc']
    tariff_abonent_number_8800 = data_post['tariff_abonent_number_8800']
    tariff_abonent_number_category_abc = data_post['tariff_abonent_number_category_abc']
    tariff_user_hardware_type = data_post['tariff_user_hardware_type']
    tariff_payment_access = data_post['tariff_payment_access']
    tariff_payment_on_number_category_access = data_post['tariff_payment_on_number_category_access']
    tariff_period_of_access = data_post['tariff_period_of_access']
    tariff_users_count_for_record = data_post['tariff_users_count_for_record']
    tariff_virtual_center_count = data_post['tariff_virtual_center_count']
    tariff_operator_count = data_post['tariff_operator_count']
    #чекбоксы
    tariff_organization_call_forwarding_in_8800 = data_post['tariff_organization_call_forwarding_in_8800']
    tariff_hardware_transfer = data_post['tariff_hardware_transfer']
    tariff_abonent_hardware_interface = data_post['tariff_abonent_hardware_interface']
    invoice_address_delivery = data_post['invoice_address_delivery']
    information_about_caller_using = data_post['information_about_caller_using']
    contract_period = data_post['contract_period']
    advert_getting = data_post['advert_getting']

    

    tariff_organization_call_forwarding_in_8800_1 = ''
    tariff_hardware_transfer_1 = ''
    tariff_hardware_transfer_2 = ''
    tariff_hardware_transfer_3 = ''
    tariff_hardware_transfer_4 = ''
    tariff_hardware_transfer_5 = ''
    tariff_abonent_hardware_interface_1 = ''
    tariff_abonent_hardware_interface_2 = ''
    invoice_address_delivery_1 = ''
    invoice_address_delivery_2 = ''
    invoice_address_delivery_3 = ''
    invoice_address_delivery_4 = ''
    information_about_caller_using_1 = ''
    information_about_caller_using_2 = ''
    contract_period_1 = ''
    contract_period_2 = ''
    advert_getting_1 = ''
    if tariff_organization_call_forwarding_in_8800 is True:
        tariff_organization_call_forwarding_in_8800_1 = 'Х'

    if tariff_hardware_transfer == 1:
        tariff_hardware_transfer_1 = 'Х'
    elif tariff_hardware_transfer == 2:
        tariff_hardware_transfer_2 = 'Х'
    elif tariff_hardware_transfer == 3:
        tariff_hardware_transfer_3 = 'Х'
    elif tariff_hardware_transfer == 4:
        tariff_hardware_transfer_4 = 'Х'
    elif tariff_hardware_transfer == 5:
        tariff_hardware_transfer_5 = 'Х'

    if tariff_abonent_hardware_interface == 1:
        tariff_abonent_hardware_interface_1 = 'Х'
    elif tariff_abonent_hardware_interface == 2:
        tariff_abonent_hardware_interface_2 = 'X'

    if invoice_address_delivery == 1:
        invoice_address_delivery_1 = 'Х'
    elif invoice_address_delivery == 2:
        invoice_address_delivery_2 = 'Х'
    elif invoice_address_delivery == 3:
        invoice_address_delivery_3 = 'Х'
    elif invoice_address_delivery == 4:
        invoice_address_delivery_4 = 'Х'

    if information_about_caller_using is True:
        information_about_caller_using_1 = 'Х'
    elif information_about_caller_using is False:
        information_about_caller_using_2 = 'Х'

    if contract_period == 1:
        contract_period_1 = 'Х'
    elif contract_period == 2:
        contract_period_2 = 'Х'

    if advert_getting is False:
        advert_getting_1 = 'Х'


    #Получаем данные от DaData
    data = innApi_v2.mainn(client_inn)

    #Заполняемм таблицу - товар/цена/стоимость и тд.
    summa = 0
    count = 0
    bag = []
    table = pd.DataFrame({'t_num':[],'t_products':[],'t_kol':[],'t_ed':[],'t_nds':[],'t_price':[],'t_sum':[],'t_payment_frequency':[]})
    table = table[['t_num','t_products','t_kol','t_ed','t_nds','t_price','t_sum','t_payment_frequency']] 
    try:
        for i in range(len(data_post['invoice'])):
            table.loc[len(table)] = [
                str(len(table)+1),
                data_post['invoice'][i]['service_name'],
                str(data_post['invoice'][i]['quantity']),
                data_post['invoice'][i]['unit'],
                nds_2,
                '{0:.2f}'.format(data_post['invoice'][i]['cost']),
                '{0:.2f}'.format(data_post['invoice'][i]['quantity'] * data_post['invoice'][i]['cost']),
                payment_frequency]
            count = count + data_post['invoice'][i]['quantity']
            summa = summa + (data_post['invoice'][i]['quantity'] * data_post['invoice'][i]['cost'])
            bag.append({'n': table['t_num'][i], 'product': table['t_products'][i],'kol': table['t_kol'][i],'ed': table['t_ed'][i],'nds': table['t_nds'][i],'price': table['t_price'][i],'summ': table['t_sum'][i], 'param':str(table['t_kol'][i]+table['t_ed'][i]), 'period':payment_frequency})
    except:
        pass
    #Общая стоимость заказа
    if provider_nds == 1:
        nds_4 = round(summa / 1.2 * 0.2,2)
        #nds_5 = ', в том числе НДС:' + str(nds_4)
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
        ##Узнать текущий месяц для оплаты периода
        #_____________________________________________________        
        m = int(datetime.date.today().strftime('%m'))
        a = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        year = datetime.date.today().strftime('%Y')
        data_invoice = (a[m-1]+' '+year)

        ##QRCODE_GENERATION
        #_____________________________________________________
        img = qrcode.make(f'''ST00012|Name={provider_name}|
                            PersonalAcc={provider_account1}|
                            BankName={provider_bank}|
                            BIC={provider_bik}|
                            CorrespAcc={provider_account2}|
                            LastName={data['data']['management']['name'].split()[0]}|
                            FirstName={data['data']['management']['name'].split()[1]}|
                            MiddleName={data['data']['management']['name'].split()[2]}|
                            Purpose=Оплата услуги Виртуальная АТС за {data_invoice} года|
                            Sum={'{0:.0f}'.format(float(summa_str)*100)}''')
        img.save('qr_'+key+'.png')

        doc = DocxTemplate("tpl_invoice.docx")
        myimage = InlineImage(doc,'qr_'+key+'.png',width=Mm(30))
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
            'var17' : nds_4,
            'var18' : summa_str,
            'var19' : num2words(int(summa), lang='ru').capitalize(),
            'var20' : data_invoice,
            'var21' : count,
            'var22' : product_name,
            'qrcode': myimage,
            'tbl_contents': bag,

            }
        doc.render(context)
        #myimage = InlineImage(doc,'test_files/python_logo.png',width=Mm(20))
        
        #print (namme,"\n",pwd)
        doc.save("doc_1_"+key+".docx")
        say_hii("doc_1_"+key+".docx")
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

            'var17' : nds_4,
            'var18' : summa_str,
            'var19' : num2words(int(summa), lang='ru').capitalize(),
            'var20' : count,#len(data_post['invoice']),
            'tbl_contents': bag,

            }
        #print (len(data_post['invoice']))
        doc.render(context)
        doc.save("doc_2_"+key+".docx")

    ##Договор о предоставлении услуг
    #_____________________________________________________
    #def write_contract():
        #doc = DocxTemplate("tpl_invoice_3.docx")
        #context = {
        #    #'var1' : provider_bank,
        #    #'var2' : provider_inn,
        #    #'var3' : provider_kpp,
        #    #'var4' : provider_name,
        #    #'var5' : provider_bik,
        #    #'var6' : provider_account1,
        #    #'var7' : provider_account2,
        #    #'var8' : num['number'],
        #    #'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
        #    #'var10' : provider_address,
        #    #'var11' : data['value'],
        #    #'var12' : data['data']['inn'],
        #    #'var13' : data['data']['kpp'],
        #    #'var14' : data['data']['address']['value'],
        #    #
        #    #'n1' : table.iloc[0]['t_num'],
        #    #'n2' : table.iloc[1]['t_num'],
        #    #'n3' : table.iloc[2]['t_num'],
        #    #'n4' : table.iloc[3]['t_num'],
        #    #'n5' : table.iloc[4]['t_num'],
        #    #
        #    #'product1' : table.iloc[0]['t_products'],
        #    #'product2' : table.iloc[1]['t_products'],
        #    #'product3' : table.iloc[2]['t_products'],
        #    #'product4' : table.iloc[3]['t_products'],
        #    #'product5' : table.iloc[4]['t_products'],
        #    #
        #    #'kol1' : table.iloc[0]['t_kol'],
        #    #'kol2' : table.iloc[1]['t_kol'],
        #    #'kol3' : table.iloc[2]['t_kol'],
        #    #'kol4' : table.iloc[3]['t_kol'],
        #    #'kol5' : table.iloc[4]['t_kol'],
        #    #
        #    #'ed1' : table.iloc[0]['t_ed'],
        #    #'ed2' : table.iloc[1]['t_ed'],
        #    #'ed3' : table.iloc[2]['t_ed'],
        #    #'ed4' : table.iloc[3]['t_ed'],
        #    #'ed5' : table.iloc[4]['t_ed'],
        #    #
        #    #'nds1' : table.iloc[0]['t_nds'],
        #    #'nds2' : table.iloc[1]['t_nds'],
        #    #'nds3' : table.iloc[2]['t_nds'],
        #    #'nds4' : table.iloc[3]['t_nds'],
        #    #'nds5' : table.iloc[4]['t_nds'],
        #    #
        #    #'price1' : table.iloc[0]['t_price'],
        #    #'price2' : table.iloc[1]['t_price'],
        #    #'price3' : table.iloc[2]['t_price'],
        #    #'price4' : table.iloc[3]['t_price'],
        #    #'price5' : table.iloc[4]['t_price'],
        #    #
        #    #'summ1' : table.iloc[0]['t_sum'],
        #    #'summ2' : table.iloc[1]['t_sum'],
        #    #'summ3' : table.iloc[2]['t_sum'],
        #    #'summ4' : table.iloc[3]['t_sum'],
        #    #'summ5' : table.iloc[4]['t_sum'],
        #    #
        #    #'var18' : summa_str,
        #    #'var19' : num2words(int(summa), lang='ru'),
        #    #
        #    #'var20' : data['data']['ogrn'],
        #    #'var21' : provider_ogrn,
        #    #'var22' : nds_5,
        #    #'var23' : nds_6
        #    #}
        #doc.render(context)
        #doc.save("doc_3_"+key+".docx")
    
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
            'var23' : tariff_notincluded_users_count,
            'var24' : tariff_included_minuts_count,
            'var25' : tariff_abonent_number_abc,
            'var26' : tariff_abonent_number_8800,
            'var27' : tariff_abonent_number_category_abc,
            'var28' : tariff_user_hardware_type,
            'var29' : tariff_payment_access,
            'var30' : tariff_payment_on_number_category_access,
            'var31' : tariff_period_of_access,
            'var32' : tariff_users_count_for_record,
            'var33' : tariff_virtual_center_count,
            'var34' : tariff_operator_count,
            #заполняем чекбоксы
            'var35_1' : tariff_organization_call_forwarding_in_8800_1,
            'var36_1' : tariff_hardware_transfer_1,
            'var36_2' : tariff_hardware_transfer_2,
            'var36_3' : tariff_hardware_transfer_3,
            'var36_4' : tariff_hardware_transfer_4,
            'var36_5' : tariff_hardware_transfer_5,
            'var37_1' : tariff_abonent_hardware_interface_1,
            'var37_2' : tariff_abonent_hardware_interface_2,
            'var38_1' : invoice_address_delivery_1,
            'var38_2' : invoice_address_delivery_2,
            'var38_3' : invoice_address_delivery_3,
            'var38_4' : invoice_address_delivery_4,
            'var39_1' : information_about_caller_using_1,
            'var39_2' : information_about_caller_using_2,
            'var40_1' : contract_period_1,
            'var40_2' : contract_period_2,
            'var41_1' : advert_getting_1,
            'tbl_contents': bag,

            }
        doc.render(context)
        doc.save("doc_4_"+key+".docx")


    ##Условия для создания шаблонов
    #_____________________________________________________
    if template_code == 'vpbx':
        write_contract_RT()
        write_invoice()
        write_act()
        #responseJson = {"contractRT_url": "/getfile/doc_4_"+key+".docx"}
    else:
        pass
        #responseJson = {"contract_url": "/getfile/doc_3_"+key+".docx","act_url": "/getfile/doc_2_"+key+".docx","invoice_url": "/getfile/doc_1_"+key+".docx"}
        #write_invoice()
        #write_act()
        #write_contract()
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
    print("--- %s seconds ---" % (time.time() - start_time))
    #Формируем ответ    
    #responseJson = {"contractRT_url": "/getfile/doc_4_"+key+".docx","contract_url": "/getfile/doc_3_"+key+".docx","act_url": "/getfile/doc_2_"+key+".docx","invoice_url": "/getfile/doc_1_"+key+".docx"}
    return ('ok')

#@app.route('/api/companies/<int:provider_inn>/documents', methods=['GET'])
#def get_documents(provider_inn):
#    provider_inn = str(provider_inn)
#    table = pd.DataFrame({'Акт':[],'Договор':[],'Счет на оплату':[],'Дата создания':[],'Заказчик':[]})
#    table = table[['Заказчик','Акт','Договор','Счет на оплату','Дата создания']] 
#    for i in range(3):
#        table.loc[len(table)] = [float('{0:.2f}'.format(1000)),'12',11223344]    

if __name__ == '__main__':

    app.run(debug=False,threaded = True, host='0.0.0.0', port=6060)