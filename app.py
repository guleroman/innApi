#!flask/bin/python
from flask import Flask, jsonify, request, json, send_file
from docxtpl import DocxTemplate
from num2words import num2words   
import innApi_v2, datetime, uuid
import pandas as pd
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/inn/', methods=['GET'])
def main():
    inn=request.args.get('inn')
    data,key = innApi_v2.mainn(inn)
    return jsonify(data)#{'Реквизиты': data})

@app.route('/api/doc/', methods=['GET'])
def main2():
    pid = []
    pr = []
    inn=request.args.get('inn')
    cid=request.args.get('cid')
    
    pid.append(request.args.get('pid1'))
    pid.append(request.args.get('pid2'))
    pid.append(request.args.get('pid3'))
    pid.append(request.args.get('pid4'))
    pid.append(request.args.get('pid5'))
    pr.append(request.args.get('pr1'))
    pr.append(request.args.get('pr2'))
    pr.append(request.args.get('pr3'))
    pr.append(request.args.get('pr4'))
    pr.append(request.args.get('pr5'))
    data,key = innApi_v2.mainn(inn)
    
    #загрузить из json
    with open('company.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
        company = json.load(fh)

    with open("iteration.json", "r") as read_file:
        num = json.load(read_file)
    nds = 20
    nds_2 = "20 %"
    nds_3 = "НДС " + nds_2
    var_23 = ''
    if company['cid'][cid]['nds'] == 1:
        nds = 0
        nds_2 = '-'
        nds_3 = ''
    #Заполняем таблицу DF    
    table = pd.DataFrame({'t_num':[],'t_products':[],'t_kol':[],'t_ed':[],'t_nds':[],'t_price':[],'t_sum':[]})
    table = table[['t_num','t_products','t_kol','t_ed','t_nds','t_price','t_sum']]
    print (table)
    for i in range(len(pid)):
        if pid[i] is not None:
            table.loc[len(table)] = [
                str(len(table)+1),
                str(company['cid'][cid]['pid'][pid[i]]['name']),
                str(pr[i]),
                str(company['cid'][cid]['pid'][pid[i]]['ed']),
                str(nds_2),
                company['cid'][cid]['pid'][pid[i]]['price'],
                int(pr[i])*int(company['cid'][cid]['pid'][pid[i]]['price'])]
    summa = table['t_sum'].sum()
    nds_4 = round(summa / 1.2 * 0.2,2)
    nds_5 = ', в том числе НДС:' + str(nds_4)
    for i in range(len(table),5):
        table.loc[len(table)] = [
            '',
            '',
            '',
            '',
            '',
            '',
            '']
            
    if company['cid'][cid]['nds'] == 1:
        nds_4 = ''
        nds_5 = ''
        var_23 = 'Стоимость услуг НДС не облагается в связи с применением Исполнителем упрощенной системы налогообложения.'
    doc = DocxTemplate("tpl_invoice.docx")
    context = { 
        'var0' : nds,
        'var1' : company['cid'][cid]['bank'],
        'var2' : company['cid'][cid]['inn'],
        'var3' : company['cid'][cid]['kpp'],
        'var4' : company['cid'][cid]['name'],
        'var5' : company['cid'][cid]['bik'],
        'var6' : company['cid'][cid]['account1'],
        'var7' : company['cid'][cid]['account2'],
        'var8' : num['number'],
        'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
        'var10' : company['cid'][cid]['address'],
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
        'var18' : str(summa),
        'var19' : num2words(int(summa), lang='ru')
        }
    doc.render(context)
    doc.save("doc_1_"+key+".docx")
    
#_____________________________________________________
    doc = DocxTemplate("tpl_invoice_2.docx")
    context = {
        'var2' : company['cid'][cid]['inn'],
        'var3' : company['cid'][cid]['kpp'],
        'var4' : company['cid'][cid]['name'],
        'var8' : num['number'],
        'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
        'var10' : company['cid'][cid]['address'],
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
        'var18' : str(summa),
        'var19' : num2words(int(summa), lang='ru')
        }
    doc.render(context)
    doc.save("doc_2_"+key+".docx")
#_____________________________________________________

#_____________________________________________________
    doc = DocxTemplate("tpl_invoice_3.docx")
    context = {
       'var1' : company['cid'][cid]['bank'],
        'var2' : company['cid'][cid]['inn'],
        'var3' : company['cid'][cid]['kpp'],
        'var4' : company['cid'][cid]['name'],
        'var5' : company['cid'][cid]['bik'],
        'var6' : company['cid'][cid]['account1'],
        'var7' : company['cid'][cid]['account2'],
        'var8' : num['number'],
        'var9' : datetime.datetime.today().strftime("%d.%m.%Y"),
        'var10' : company['cid'][cid]['address'],
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

        'var18' : str(summa),
        'var19' : num2words(int(summa), lang='ru'),
        
        'var20' : data['data']['ogrn'],
        'var21' : company['cid'][cid]['ogrn'],
        'var22' : nds_5,
        'var23' : var_23
        }
    doc.render(context)
    doc.save("doc_3_"+key+".docx")
#_____________________________________________________

    num['number'] = num['number'] + 1
    with open("iteration.json", "w") as write_file:
        json.dump(num, write_file)
    return "Hello ПримаДокументы! <br><br> <a href=/getfile/doc_1_"+key+".docx>Cчет на оплату</a><br><br><a href=/getfile/doc_2_"+key+".docx>Акт</a><br><br><a href=/getfile/doc_3_"+key+".docx>Договор о предоставлении услуг</a><br><br>"

@app.route('/getfile/<name>')
def get_output_file(name):
    return send_file(name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5000)

