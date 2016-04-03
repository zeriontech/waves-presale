from API import API

base_address = "0x82e1c8c4c38f5c0767f7c426e235f194010b71e9"
contract_address = "0xac64a5168144734f0d688D689c730A519844D0c5"
api = API()

def logSale(bitcoin_tx_id, amount):
    definition = "newSale(bytes32,uint256)"
    method_id = api.getMethodId(definition)
    amount = abs(int(amount * (10 ** 8)))
    amount_bytes = amount.to_bytes(32, byteorder='big').hex()
    data = "0x" + method_id + bitcoin_tx_id + amount_bytes

    gas_price = hex(api.getGasPrice()["result"])
    response = api.send_transaction(base_address, contract_address,
                         gas=hex(200000), gasPrice=gas_price,
                         value=hex(0), data=data)
    print(str(response))
    return data