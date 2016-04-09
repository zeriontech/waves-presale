import json


class APIResponse:
    def __init__(self, response_dict={}, status=0, error=""):
        self.response_dict = response_dict
        if self.response_dict.get("jsonrpc"):
            del self.response_dict["jsonrpc"]
        if self.response_dict.get("id"):
            del self.response_dict["id"]
        self.status = status
        self.error = error

    def __str__(self):
        self.response_dict["status"] = self.status
        if self.status != 0:
            self.response_dict["error"] = self.error
        return json.dumps(self.response_dict, sort_keys=True)

    def __getitem__(self, item):
        return self.response_dict[item]