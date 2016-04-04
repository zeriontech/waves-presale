import requests
from APIResponse import APIResponse
from Errors import *
import json
import binascii


class API:
    def __init__(self):
        self.api_endpoint = "http://localhost:8545/"

    def http_request(self, method, params):
        data = {"jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1543}  # TODO make nonce

        r = requests.post(self.api_endpoint, json=data)
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            raise BadResponseError(r.status_code)

    def api_request(self, method, params):
        try:
            response = self.http_request(method, params)
            json_response = json.loads(response)
            if json_response.get('error', False):
                return APIResponse({}, json_response['error'].get('code', '-1'),
                                   json_response['error'].get('message', 'Internal error'))
            return APIResponse(json_response, 0)
        except BadResponseError:
            return APIResponse({}, 3, "Internal error")

    def getGasPrice(self):
        response = self.api_request("eth_gasPrice", [])
        response.response_dict["result"] = int(response.response_dict["result"], 16)
        return response

    def getAccountByAddress(self, address):
        response = self.api_request("eth_getBalance", [address, "latest"])
        ans = APIResponse({"address": address,
                           "balance": int(response.response_dict["result"], 16)})
        return ans

    def getLatestBlock(self):
        response = self.api_request("eth_getBlockByNumber", ["latest", False])
        ans = APIResponse({"number": int(response.response_dict["result"]["number"], 16),
                           "hash": response.response_dict["result"]["hash"]})
        return ans

    def getSHA256(self, string):
        b = bytearray()
        b.extend(map(ord, string))
        bytes_string = str(binascii.b2a_hex(b), 'ascii')
        byte_string = "0x" + bytes_string
        response = self.api_request("web3_sha3", [byte_string])
        return response.response_dict["result"]

    #tested on samples
    def getMethodId(self, definition):
        hash = self.getSHA256(definition)
        return hash[2:10]

    def send_transaction(self, from_address, to_address, gas, gasPrice, value, data):
        response = self.api_request("eth_sendTransaction", [{"from": from_address,
                                                            "to": to_address,
                                                            "gas": gas,
                                                            "gasPrice": gasPrice,
                                                            "value": value,
                                                            "data": data}])
        print(response)
        ans = APIResponse({"hash": response.response_dict["result"]})
        return ans

