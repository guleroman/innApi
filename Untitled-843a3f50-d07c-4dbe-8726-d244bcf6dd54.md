# Автоматизированное формирование учетных документов

---

---

### Генерируемые документы

[Счет на оплату](./Untitled-1746d1b3-bff8-442e-b8fb-58cffa5fbae0.md)

[Акт](./Untitled-ff69d6fb-2d41-4640-9fef-429849e4742b.md)

[Договор](./Untitled-6ee86605-b5bb-41ee-ace7-998a3a8fed35.md)

### API

    http://176.99.11.61:8888
    
    POST /api/companies/{inn}/documents //генерация документов
    
    GET /api/companies/{inn} //Получение информации о компании

### Замысел

Обращение к Dadata.
Получение информации о компании.
Генерация документов.
Кэширование информации.
Статистика.

---

## Создание документов

[Описание POST /api/companies/{inn}/documents](./POST-api-companies-inn-documents-b574523e-8de0-423b-8c8d-7f45f55dd3e5.csv)

    POST /api/companies/{inn}/documents
    
    {
      "client_inn": "5504036333",
      "client_kpp": "8866111123",
      "template_code": "vpbx",
      "payload": {
    		  "product_name": "Виртуальная АТС", 
    		  "tariff_name": "План 100", 
    		  "tariff_users_count": 1,
    			"tariff_notincluded_users_count": 4, 
    	    "tariff_included_minuts_count": 100, 
    			"tariff_abonent_number_abc": "1",
    			"tariff_abonent_number_8800": "1", 
    			"tariff_abonent_number_category_abc": "1",
    			"tariff_user_hardware_type": "1", 
    			"tariff_payment_access": "1",
    			"tariff_payment_on_number_category_access": "1",
    			"tariff_period_of_access": "1",
    			"tariff_users_count_for_record": "1", 
    			"tariff_virtual_center_count": "1", 
    			"tariff_operator_count": "1", 
    			"tariff_organization_call_forwarding_in_8800": true, 
    			"tariff_hardware_transfer": 1,
    			"tariff_abonent_hardware_interface": 1,
    			"invoice_address_delivery": 1, 
    			"information_about_caller_using": true, 
    			"contract_period": 1, 
    			"advert_getting": true,
    		
    			"invoice": [
    		    {
    				 "service_name": "Абонентская плата",
    				 "unit": "шт.",            
    		     "quantity": 1,
    	       "cost": 100
    		    },
    		    {
    	       "service_name": "Пакет 100 (100 исходящих минут, 1 рабочее место, 1 номер)",
    				 "unit": "шт.",            
    	       "quantity": 1,
             "cost": 300
    		    },
    		    {
    	       "service_name": "Дополнительное рабочее место Виртуальной АТС",
    				 "unit": "шт.",            
             "quantity": 10,
             "cost": 60
    		    }
    		   ],
    		   "payment_frequency": "Ежегодный"
    	  }
    }
    
    // Ответ
    {
    	"contractRT_url": "",         
      "act_url": "",
      "invoice_url": ""
    }
    

### Хранимые данные о исполнителе

*company.json*

    {
      "7707049388": {
            "account1": "40702810038180132605",
            "account2": "30101810400000000225",
            "address": "Российская Федерация, 191002, г. Санкт-Петербург, ул. Достоевского, д. 15",
            "bank": "ПАО Сбербанк",
            "bik": "044525225",
            "inn": "7707049388",
            "kpp": "784001001",
            "name": "ПАО «Ростелеком»",
            "nds": 1,
            "ogrn": "1027700198767"
        },  
    	"231231231": {
            "account1": "1111111111111111111",
            "account2": "2222222222222222222",
            "address": "г Санкт-Петербург, ул.Попова, д.22",
            "bank": "Газпромбанк",
            "bik": "292909090929",
            "inn": "231231231",
            "kpp": "444444444",
            "name": "Ленэнерго",
            "nds": 0,
            "ogrn": "000000020000000"
        },
        "321321321": {
            "account1": "8888888888888888888",
            "account2": "9999999999999999999",
            "address": "г Москва, ул.Десантников, д.1",
            "bank": "Альфа-банк",
            "bik": "4444444444",
            "inn": "321321321",
            "kpp": "090900099",
            "name": "Ростелеком",
            "nds": 1,
            "ogrn": "000000010000000"
        },
        "3528000597": {
            "account1": "",
            "account2": "",
            "address": "Вологодская обл, г Череповец, ул Мира, д 30",
            "bank": "",
            "bik": "",
            "inn": "3528000597",
            "kpp": "352801001",
            "name": "ПАО \"СЕВЕРСТАЛЬ\"",
            "nds": 1,
            "ogrn": "1023501236901"
        },
        "7453240780": {
            "account1": "",
            "account2": "",
            "address": "454048, ОБЛАСТЬ ЧЕЛЯБИНСКАЯ, ГОРОД ЧЕЛЯБИНСК, УЛИЦА ВОРОВСКОГО, 60, НЕЖИЛОЕ ПОМЕЩЕНИЕ 5",
            "bank": "",
            "bik": "",
            "inn": "7453240780",
            "kpp": "745301001",
            "name": "ООО \"ДОДО ПИЦЦА ЧЕЛЯБИНСК\"",
            "nds": 1,
            "ogrn": "1127453003149"
        }
    }

### Статистика

    GET /api/companies/{inn}/documents
    GET /api/companies/{inn}/clients
    
    //Ответ
    {
    ...
    }