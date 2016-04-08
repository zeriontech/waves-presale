from API import API

api = API()
base_address = "0x551da69d04f10de86f3c12f24bd92abb1ece4503"
contract_address = "0x64fddDcbD0ddB00aeA47eC63Ce6376300e76B11E"

# gas_price = hex(api.getGasPrice()["result"])
# response = api.getStorageAt(contract_address, "0x0", "0x1")
# print(response)

# sales = "0x" + api.getMethodId("totalTokens()")
# responseSales = api.getInfo(base_address, contract_address, sales)
# if responseSales.status == 0:
#     numberOfSales = responseSales.response_dict["data"]
# print(numberOfSales)

# 0 - owner
# 1 - number of sales ?
# 2 - number of sales ?
# 3 - total tokens
print(api.getStorageAt(contract_address, "0x011"))
