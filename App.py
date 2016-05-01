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


@app.route("/contract_stat")
def stat():
    return app.send_static_file("contract_statistics.html")


@app.route("/Chart.js")
def chart():
    return app.send_static_file("Chart.js")


@app.route("/contract_get_sale/")
def get_sale():
    txid = request.args.get('id', "")
    if len(txid) != 64:
        return jsonify({"status": "OK",
                        "amount": "Error",
                        "date": "length of TxID should be equal to 64 symbols"})
    mhash = hashlib.md5(str.encode(txid)).hexdigest().upper()
    method = "0x" + api.getMethodId("getNumOfSalesWithSameId(bytes16)") + mhash
    number_of_txs = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, method)["data"]
    number_of_txs = int(number_of_txs, 0)
    amounts = []
    dates = []
    for i in range(number_of_txs):
        method = "0x" + api.getMethodId("getSaleDate(bytes16,uint256)") + mhash + "0" * 32 + uint_to_bytes_string(i)
        tx = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, method)["data"]
        amounts.append(int("0x" + tx[2:66], 0))
        dates.append(int("0x" + tx[66:], 0))
    if len(dates) == 0:
        return jsonify({"status": "OK",
                        "amount": "None",
                        "date": "Hash not found"})
    amounts = list(map(lambda amount: amount / 10**8, amounts))
    dates = list(map(lambda date: datetime.fromtimestamp(date), dates))
    return jsonify({"status": "OK",
                    "amount": amounts,
                    "date": dates})


@app.route("/stat_by_day")
def stat_by_day():
    with open("Statistics/info_by_day.txt") as f:
        info = list(map(lambda x: x.split(), f.readlines()))

    return jsonify(info[1:])


@app.route("/top_10")
def stat_top_ten():
    with open("Statistics/top.txt") as f:
        info = list(map(lambda x: x.split(), f.readlines()))
    data = {}
    for i, x in enumerate(info):
        if i == 10:
            data["Others"] = {"amount": x[0]}
        else:
            data["Top {}".format(i+1)] = {"amount": x[1], "date": x[2], "time": x[3]}
    return jsonify(data)

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
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
