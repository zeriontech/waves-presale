import requests
from APIResponse import APIResponse
from Errors import *
import json


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
        return str(response)

    def getAccountByAddress(self, address):
        response = self.api_request("eth_getBalance", [address, "latest"])
        ans = APIResponse({"address": address,
                           "balance": int(response.response_dict["result"], 16)})
        return str(ans)

    def getLatestBlock(self):
        response = self.api_request("eth_getBlockByNumber", ["latest", False])
        ans = APIResponse({"number": int(response.response_dict["result"]["number"], 16),
                           "hash": response.response_dict["result"]["hash"]})
        return str(ans)
