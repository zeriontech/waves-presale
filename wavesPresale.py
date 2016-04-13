#!/usr/bin/env python3.4
from API import API
from addresses import BASE_ADDRESS, CONTRACT_ADDRESS
import binascii
import hashlib
import sys

api = API()


def logSale(bitcoin_tx_id, amount, timestamp):
    if len(bitcoin_tx_id) != 64:
        print('TX Id must contain 64 symbols')
        return
    with open("sales.log", "a") as logfile:
        logfile.write(str(bitcoin_tx_id) + "\n")
    definition = "newSale(bytes16,uint256,uint256)"
    method_id = api.getMethodId(definition)
    amount = abs(int(amount * (10 ** 8)))
    mhash = hashlib.md5(str.encode(bitcoin_tx_id)).hexdigest().upper() + "0" * 32
    data = "0x" + method_id + mhash + uint_to_bytes_string(amount)\
           + uint_to_bytes_string(timestamp)
    gas_price = hex(api.getGasPrice()["result"])
    response = api.send_transaction(BASE_ADDRESS, CONTRACT_ADDRESS,
                                    gas=hex(200000), gasPrice=gas_price,
                                    value=hex(0), data=data)
    print(str(response))
    return data


def uint_to_bytes_string(number):
    number_bytes = number.to_bytes(32, byteorder='big')
    return str(binascii.b2a_hex(number_bytes), 'ascii')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Must contain following arguments:\n\tbitcoin_tx_id\n\tamount\n\ttimestamp")
    else:
        bitcoin_tx_id = sys.argv[1]
        amount = float(sys.argv[2])
        timestamp = int(sys.argv[3])
        logSale(bitcoin_tx_id, amount, timestamp)
