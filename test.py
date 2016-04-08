from API import API

api = API()
base_address = "0x551da69d04f10de86f3c12f24bd92abb1ece4503"
contract_address = "0xA0929Cca97a25bdb2f74a6FcAf78006Cd9F4AD68"

# gas_price = hex(api.getGasPrice()["result"])
# response = api.getStorageAt(contract_address, "0x0", "0x1")
# print(response)

method = "0x" + api.getMethodId("numberOfSales()")
response = api.getInfo(base_address, contract_address, method)
print(response["data"])

