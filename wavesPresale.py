from API import API
import binascii

base_address = "0x82e1c8c4c38f5c0767f7c426e235f194010b71e9"
contract_address = "0xac64a5168144734f0d688D689c730A519844D0c5"
api = API()

def logSale(bitcoin_tx_id, amount, timestamp):
    if len(bitcoin_tx_id) != 64:
        print('TX Id must contain 64 symbols')
        return
    timestamp = int(timestamp)
    definition = "newSale(bytes32,uint256)"
    method_id = api.getMethodId(definition)
    amount = abs(int(amount * (10 ** 8)))
    data = "0x" + method_id + bitcoin_tx_id + uint_to_bytes_string(amount) + uint_to_bytes_string(timestamp)

    gas_price = hex(api.getGasPrice()["result"])
    response = api.send_transaction(base_address, contract_address,
                         gas=hex(200000), gasPrice=gas_price,
                         value=hex(0), data=data)
    print(str(response))
    return data


def uint_to_bytes_string(number):
    number_bytes = number.to_bytes(32, byteorder='big')
    return str(binascii.b2a_hex(number_bytes), 'ascii')

