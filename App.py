from flask import Flask, request, jsonify
from API import API
from configs import BASE_ADDRESS, CONTRACT_ADDRESS
from datetime import datetime
import binascii

app = Flask(__name__)
api = API()


@app.route("/")
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
    tx_id_method = "0x" + api.getMethodId("getSaleTxId(uint32)") + uint_to_bytes_string(id)
    tx_id = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, tx_id_method)["data"]
    amount_method = "0x" + api.getMethodId("getSaleAmount(uint32)") + uint_to_bytes_string(id)
    amount = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, amount_method)["data"]
    date_method = "0x" + api.getMethodId("getSaleDate(uint32)") + uint_to_bytes_string(id)
    date = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, date_method)["data"]
    print(tx_id, amount, date)
    return jsonify({"status": "OK", "tx_id": tx_id, "amount": int(amount, 0) / 10**8, "date": datetime.fromtimestamp(int(date, 0))})


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
    app.run(host="0.0.0.0", port=5000)
