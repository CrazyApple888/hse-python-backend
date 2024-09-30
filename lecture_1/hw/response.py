class HttpResponse:

    def __init__(self, code: int, body: bytes):
        self.code = code
        self.body = body
