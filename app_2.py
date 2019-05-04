#!flask/bin/python
from flask import Flask, jsonify, request, json, make_response, send_file
import uuid, time,os
import innApi_v2
#from afterResponse import AfterResponse,AfterResponseMiddleware
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#AfterResponse(app)



@app.route('/api/companies/<inn>',methods=['GET'])
def get_data_about_company(inn):
    data = innApi_v2.mainn(inn)
    if data == None:
        return make_response(jsonify({"_status_code":404,"error":{"client_inn":"invalid value"}}),404)
    return jsonify(data)

#@app.after_response
def say_hi():
    link = 'http://176.99.11.61:6060/api/companies/'+provider_inn+'/documents'
    header = {'key':key}
    try:
        requests.post(link, data = json.dumps(existing_fields,ensure_ascii=True), headers = header, timeout=0.00001)
    except:
        print ("Выполнил - "+key)

@app.route('/api/companies/<int:prov_inn>/documents', methods=['POST'])
def response(prov_inn):
    start_time = time.time()
    global provider_inn, key, existing_fields
    
    provider_inn = str(prov_inn)
    key = str(uuid.uuid4())
    data_post = json.loads(request.data)
    message = {"_status_code":200,"error":{}}
    existing_fields = {
        "client_inn":"",
        "client_kpp":"",
        "template_code":"",
        "product_name":"",
        "tariff_name":"",
        "tariff_users_count":0,
        "tariff_notincluded_users_count":0,
        "tariff_included_minuts_count":0,
        "tariff_abonent_number_abc":"",
        "tariff_abonent_number_8800":"",
        "tariff_abonent_number_category_abc":"",
        "tariff_user_hardware_type":"",
        "tariff_payment_access":"",
        "tariff_payment_on_number_category_access":"",
        "tariff_period_of_access":"",
        "tariff_users_count_for_record":"",
        "tariff_virtual_center_count":"",
        "tariff_operator_count":"",
        
        "tariff_organization_call_forwarding_in_8800":False,
        "tariff_hardware_transfer":"",
        "tariff_abonent_hardware_interface":"",
        "invoice_address_delivery":"",
        "information_about_caller_using":"",
        "contract_period":"",
        "advert_getting":True,
        "payment_frequency":"",
        "invoice": [

        ]
    }

    def key_area():
        try:
            existing_fields.update({"client_inn":data_post['client_inn']})
            if type(existing_fields['client_inn']) is not str:
                message['error'].update({"client_inn":"string is expected"})
                message.update({"_status_code":422})
        except:
            message['error'].update({"client_inn":"required field"})
            message.update({"_status_code":422})
            del existing_fields['client_inn']

        try:
           existing_fields.update({"client_kpp":data_post['client_kpp']})
           if type(existing_fields['client_kpp']) is not str:
                message['error'].update({"client_kpp":"string is expected"})
                message.update({"_status_code":422})
        except:
            #message['error'].update({"client_kpp":"required field"})
            pass

        try:
            existing_fields.update({"template_code":data_post['template_code']})
            if type(existing_fields['template_code']) is not str:
                message['error'].update({"template_code":"string is expected"})
                message.update({"_status_code":422})
        except:           
            message['error'].update({"template_code":"required field"})
            message.update({"_status_code":422})

        try:        
            existing_fields.update({"product_name":data_post['payload']['product_name']})
            if type(existing_fields['product_name']) is not str:
                message['error'].update({"product_name":"string is expected"})
                message.update({"_status_code":422})
        except:            
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_name":data_post['payload']['tariff_name']})
            if type(existing_fields['tariff_name']) is not str:
                message['error'].update({"tariff_name":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_users_count":data_post['payload']['tariff_users_count']})
            if type(existing_fields['tariff_users_count']) is not int:
                message['error'].update({"tariff_users_count":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"payment_frequency":data_post['payload']['payment_frequency']})
            if type(existing_fields['payment_frequency']) is not str:
                message['error'].update({"payment_frequency":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_notincluded_users_count":data_post['payload']['tariff_notincluded_users_count']})
            if type(existing_fields['tariff_notincluded_users_count']) is not int:
                message['error'].update({"tariff_notincluded_users_count":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_included_minuts_count":data_post['payload']['tariff_included_minuts_count']})
            if type(existing_fields['tariff_included_minuts_count']) is not int:
                message['error'].update({"tariff_included_minuts_count":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_abonent_number_abc":data_post['payload']['tariff_abonent_number_abc']})
            if type(existing_fields['tariff_abonent_number_abc']) is not str:
                message['error'].update({"tariff_abonent_number_abc":"string is expected"})
                message.update({"_status_code":422})
        except:          
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_abonent_number_8800":data_post['payload']['tariff_abonent_number_8800']})
            if type(existing_fields['tariff_abonent_number_8800']) is not str:
                message['error'].update({"tariff_abonent_number_8800":"string is expected"})
                message.update({"_status_code":422})
        except:            
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_abonent_number_category_abc":data_post['payload']['tariff_abonent_number_category_abc']})
            if type(existing_fields['tariff_abonent_number_category_abc']) is not str:
                message['error'].update({"tariff_abonent_number_category_abc":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass 

        try:
            existing_fields.update({"tariff_user_hardware_type":data_post['payload']['tariff_user_hardware_type']})
            if type(existing_fields['tariff_user_hardware_type']) is not str:
                message['error'].update({"tariff_user_hardware_type":"string is expected"})
                message.update({"_status_code":422})
        except:            
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_payment_access":data_post['payload']['tariff_payment_access']})
            if type(existing_fields['tariff_payment_access']) is not str:
                message['error'].update({"tariff_payment_access":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_payment_on_number_category_access":data_post['payload']['tariff_payment_on_number_category_access']})
            if type(existing_fields['tariff_payment_on_number_category_access']) is not str:
                message['error'].update({"tariff_payment_on_number_category_access":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_period_of_access":data_post['payload']['tariff_period_of_access']})
            if type(existing_fields['tariff_period_of_access']) is not str:
                message['error'].update({"tariff_period_of_access":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_users_count_for_record":data_post['payload']['tariff_users_count_for_record']})
            if type(existing_fields['tariff_users_count_for_record']) is not str:
                message['error'].update({"tariff_users_count_for_record":"string is expected"})
                message.update({"_status_code":422})
        except:            
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_virtual_center_count":data_post['payload']['tariff_virtual_center_count']})
            if type(existing_fields['tariff_virtual_center_count']) is not str:
                message['error'].update({"tariff_virtual_center_count":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:
            existing_fields.update({"tariff_operator_count":data_post['payload']['tariff_operator_count']})
            if type(existing_fields['tariff_operator_count']) is not str:
                message['error'].update({"tariff_operator_count":"string is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        #чекбоксы
        try:
            existing_fields.update({"tariff_organization_call_forwarding_in_8800":data_post['payload']['tariff_organization_call_forwarding_in_8800']})
            if type(existing_fields['tariff_organization_call_forwarding_in_8800']) is not bool:
                message['error'].update({"tariff_organization_call_forwarding_in_8800":"boolean is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass 

        try:    
            existing_fields.update({"tariff_hardware_transfer":data_post['payload']['tariff_hardware_transfer']})
            if type(existing_fields['tariff_hardware_transfer']) is not int:
                message['error'].update({"tariff_hardware_transfer":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:    
            existing_fields.update({"tariff_abonent_hardware_interface":data_post['payload']['tariff_abonent_hardware_interface']})
            if type(existing_fields['tariff_abonent_hardware_interface']) is not int:
                message['error'].update({"tariff_abonent_hardware_interface":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:    
            existing_fields.update({"invoice_address_delivery":data_post['payload']['invoice_address_delivery']})
            if type(existing_fields['invoice_address_delivery']) is not int:
                message['error'].update({"invoice_address_delivery":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:    
            existing_fields.update({"information_about_caller_using":data_post['payload']['information_about_caller_using']})
            if type(existing_fields['information_about_caller_using']) is not bool:
                message['error'].update({"information_about_caller_using":"boolean is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:    
            existing_fields.update({"contract_period":data_post['payload']['contract_period']})
            if type(existing_fields['contract_period']) is not int:
                message['error'].update({"contract_period":"integer is expected"})
                message.update({"_status_code":422})
        except:           
            #message['error'].update({"client_inn":"required field"})
            pass

        try:    
            existing_fields.update({"advert_getting":data_post['payload']['advert_getting']})
            if type(existing_fields['advert_getting']) is not bool:
                message['error'].update({"advert_getting":"boolean is expected"})
                message.update({"_status_code":422})
        except:
            #message['error'].update({"advert_getting":"required field"})
            pass

        try:
            if len(data_post['payload']['invoice']) <= 5:
                for i in range(len(data_post['payload']['invoice'])):
                    try:
                        existing_fields['invoice'].append({})
                        existing_fields['invoice'][i].update({"service_name":data_post['payload']['invoice'][i]['service_name']})
                        if  type(existing_fields['invoice'][i]['service_name']) is not str:
                            message['error'].update({"service_name":"string is expected"})
                            message.update({"_status_code":422})
                    except:
                        pass

                    try:
                        existing_fields['invoice'][i].update({"unit":data_post['payload']['invoice'][i]['unit']})
                        if  type(existing_fields['invoice'][i]['unit']) is not str:
                            message['error'].update({"unit":"string is expected"})
                            message.update({"_status_code":422})
                    except:
                        pass

                    try:
                        existing_fields['invoice'][i].update({"quantity":data_post['payload']['invoice'][i]['quantity']})
                        if  type(existing_fields['invoice'][i]['quantity']) is not int:
                            message['error'].update({"quantity":"integer is expected"})
                            message.update({"_status_code":422})
                    except:
                        pass

                    try:
                        existing_fields['invoice'][i].update({"cost":data_post['payload']['invoice'][i]['cost']})
                        if  type(existing_fields['invoice'][i]['cost']) is not int:
                            message['error'].update({"cost":"integer is expected"})
                            message.update({"_status_code":422})
                    except:
                        pass
            else:
                message.update({"_status_code":422})
                message['error'].update({"invoice":"[] must be <= 5"})
        except:
            pass

        return message
    
    key_area = key_area()
    #if innApi_v2.mainn(existing_fields['client_inn']) == None:
        #return make_response(jsonify({"_status_code":404,"error":{"client_inn":"invalid value"}}),404)
    
    if key_area['_status_code'] != 200:
        return make_response(jsonify(key_area),key_area['_status_code'])
    
    print("Принял - "+key)
    if existing_fields['template_code'] == 'vpbx':
        responseJson = {"contractRT_url": "http://176.99.11.61:6060/getfile/doc_4_"+key+".docx"}
    else:
        responseJson = {"contract_url": "http://176.99.11.61:6060/getfile/doc_3_"+key+".docx","act_url": "http://176.99.11.61:6060/getfile/doc_2_"+key+".docx","invoice_url": "http://176.99.11.61:6060/getfile/doc_1_"+key+".docx"}
    
    say_hi()
    print("--- %s seconds ---" % (time.time() - start_time))
    return jsonify(responseJson)
 

if __name__ == '__main__':

    app.run(debug=False,threaded = True, host='0.0.0.0', port=5000)