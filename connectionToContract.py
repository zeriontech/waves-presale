from API import API

contract_address = "0xB19BA96Bc945712ef731b836db50332ADfA885b8".lower()
api = API()

def logSale(bitcoin_tx_id, amount):
    definition = "newSale(bytes32,uint128)"
    method_id = api.getMethodId(definition)
    amount = abs(int(amount * (10 ** 8)))
    amount_bytes = amount.to_bytes(16, byteorder='big').hex()
    data = "0x" + method_id + bitcoin_tx_id + amount_bytes
    return data