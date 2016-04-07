from flask import Flask, request, jsonify
from API import API
from configs import BASE_ADDRESS, CONTRACT_ADDRESS

app = Flask(__name__)
api = API()


@app.route("/")
def info():
    return app.send_static_file("checker.html")


@app.route("/get_sale/")
def get_sale():
    # TODO: here
    method = "0x" + api.getMethodId("getSale(uint32)")
    response = api.getInfo(BASE_ADDRESS, CONTRACT_ADDRESS, method)
    print(response)
    return jsonify({"status": "OK", "data": response["data"]})


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
