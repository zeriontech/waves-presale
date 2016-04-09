from flask import Flask, request, jsonify
from API import API
from addresses import BASE_ADDRESS, CONTRACT_ADDRESS
from datetime import datetime
import binascii

app = Flask(__name__)
api = API()


@app.route("/contract_info")
def info():
    return app.send_static_file("checker.html")


@app.route("/get_sale/")
def get_sale():
    try:
        id = int(request.args.get('id', -1))
    except ValueError:
        return jsonify({"status": "OK", "tx_id": "None", "amount": "None", "date": "None"})
    if id < 0:
        return jsonify({"status": "OK", "tx_id": "None", "amount": "None", "date": "None"})
    num_of_sales_method = "0x" + api.getMethodId("numberOfSales()")
    num_of_sales = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, num_of_sales_method)["data"]
    num_of_sales = int(num_of_sales, 0)
    print(id, num_of_sales)
    if id >= num_of_sales:
        return jsonify({"status": "OK", "tx_id": "None", "amount": "None", "date": "None"})
    tx_id = call_method("getSaleTxId(uint32)", id)
    amount = call_method("getSaleAmount(uint32)", id)
    date = call_method("getSaleDate(uint32)", id)
    print(tx_id, amount, date)
    return jsonify({"status": "OK",
                    "tx_id": tx_id,
                    "amount": int(amount, 0) / 10**8,
                    "date": datetime.fromtimestamp(int(date, 0))})


def call_method(method, id):
    method = "0x" + api.getMethodId(method) + uint_to_bytes_string(id)
    return api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, method)["data"]


@app.route("/get_info/")
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


@app.route("/styles.css")
def styles():
    return app.send_static_file("styles.css")


def uint_to_bytes_string(number):
    number_bytes = number.to_bytes(32, byteorder='big')
    return str(binascii.b2a_hex(number_bytes), 'ascii')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)