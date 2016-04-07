from API import API

api = API()
base_address = "0x551da69d04f10de86f3c12f24bd92abb1ece4503"
contract_address = "0x64fddDcbD0ddB00aeA47eC63Ce6376300e76B11E"

# gas_price = hex(api.getGasPrice()["result"])
# response = api.getStorageAt(contract_address, "0x0", "0x1")
# print(response)

tokens = "0x" + api.getMethodId("totalTokens()")
sales = "0x" + api.getMethodId("numberOfSales()")
totalTokens, numberOfSales = -1, -1
responseTokens = api.getInfo(base_address, contract_address, tokens)
if responseTokens.status == 0:
    totalTokens = int(responseTokens.response_dict["data"], 0) / 10**8
responseSales = api.getInfo(base_address, contract_address, sales)
if responseSales.status == 0:
    numberOfSales = int(responseSales.response_dict["data"], 0)
print(totalTokens, numberOfSales)
