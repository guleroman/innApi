#!flask/bin/python
from flask import Flask, jsonify, request
import innApi_v2
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/', methods=['GET'])
def main():
	inn=request.args.get('inn')
	data = innApi_v2.mainn(inn)
	return jsonify({'Реквизиты': data})
	
if __name__ == '__main__':
	app.run(debug=True ,host='0.0.0.0', port=5000)