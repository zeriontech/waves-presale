class BadResponseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Bad response status code: {0}".format(repr(self.value))