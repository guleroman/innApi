#!flask/bin/python
from flask import Flask, jsonify, request
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/inn/', methods=['GET'])
def main():
    inn=request.args.get('inn')
    return "Hello ПримаДокументы! <br><br> <a href=/getfile/doc_1_.docx>Cчет на оплату</a><br><br><a href=/getfile/doc_2_.docx>Акт</a><br><br><a href=/getfile/doc_3_.docx>Договор о предоставлении услуг</a><br><br>"#{'Реквизиты': data})
	
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)

