from flask import Flask, request, jsonify
from API import API
from addresses import BASE_ADDRESS, CONTRACT_ADDRESS
from datetime import datetime
import binascii
import hashlib

app = Flask(__name__)
api = API()


@app.route("/contract_info")
def info():
    return app.send_static_file("contract_info.html")


@app.route("/contract_get_sale/")
def get_sale():
    txid = request.args.get('id', "")
    if len(txid) != 64:
        return jsonify({"status": "OK",
                        "amount": "Error",
                        "date": "length of TxID should be equal to 64 symbols"})
    mhash = hashlib.md5(str.encode(txid)).hexdigest().upper()
    method = "0x" + api.getMethodId("getSaleDate(bytes16)") + mhash
    response = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, method)["data"]
    amount = int("0x" + response[2:66], 0)
    date = int("0x" + response[66:], 0)
    if date == 0:
        return jsonify({"status": "OK",
                        "amount": "None",
                        "date": "Hash not found"})
    return jsonify({"status": "OK",
                    "amount": amount / 10**8,
                    "date": datetime.fromtimestamp(date)})


def call_method(method, id):
    method = "0x" + api.getMethodId(method) + uint_to_bytes_string(id)
    return api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, method)["data"]


@app.route("/contract_get_info/")
def get_info():
    tokens = "0x" + api.getMethodId("totalTokens()")
    sales = "0x" + api.getMethodId("numberOfSales()")
    total_tokens, number_of_sales = -1, -1
    response_tokens = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, tokens)
    if response_tokens.status == 0:
        total_tokens = int(response_tokens["data"], 0) / 10 ** 8
    response_sales = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, sales)
    if response_sales.status == 0:
        number_of_sales = int(response_sales["data"], 0)
    if number_of_sales == -1 or total_tokens == -1:
        return jsonify({"status": "ERROR"})
    return jsonify({"status": "OK", "numberOfSales": number_of_sales,
                    "totalTokens": total_tokens})

def uint_to_bytes_string(number):
    number_bytes = number.to_bytes(32, byteorder='big')
    return str(binascii.b2a_hex(number_bytes), 'ascii')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
