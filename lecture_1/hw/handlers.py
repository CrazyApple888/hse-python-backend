import math
from abc import abstractmethod

from lecture_1.hw.exceptions import HttpException
from lecture_1.hw.response import HttpResponse


class BaseHandler:

    @abstractmethod
    def is_suitable(self, route: bytes) -> bool:
        pass

    @abstractmethod
    async def handle(self, route: bytes, query: bytes, body: bytes) -> HttpResponse:
        pass


class FibonacciHandler(BaseHandler):

    def is_suitable(self, route: bytes) -> bool:
        return route.find("/fibonacci/") != -1

    async def handle(self, route: bytes, query: bytes, body: bytes) -> HttpResponse:
        n = int(route.split('/')[-1])
        if n < 0:
            raise HttpException(400, "N should be more than 0")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b

        return HttpResponse(
            code=200,
            body=f"{{ \"result\": {b} }}".encode('utf-8')
        )


class FactorialHandler(BaseHandler):

    def is_suitable(self, route: bytes) -> bool:
        return route.endswith("/factorial")

    async def handle(self, route: bytes, query: bytes, body: bytes) -> HttpResponse:
        n = int(query.split(b'n=')[-1])

        if n < 0:
            raise HttpException(400, "N should be more than 0")

        return HttpResponse(
            code=200,
            body=f"{{ \"result\": {math.factorial(n)} }}".encode('utf-8'),
        )


class MeanHandler(BaseHandler):

    def is_suitable(self, route: bytes) -> bool:
        return route.endswith("/mean")

    async def handle(self, route: bytes, query: bytes, body: bytes) -> HttpResponse:
        if len(body) == 0:
            raise HttpException(422, "Unprocessable entity")
        string_numbers = (body.decode('utf-8')
                          .replace(" ", "")
                          .replace("[", "")
                          .replace("]", "")
                          )

        if len(string_numbers) == 0:
            raise HttpException(400, "Invalid value for body, must be non-empty array of floats")

        numbers = list(map(float, string_numbers.split(",")))

        return HttpResponse(
            code=200,
            body=f"{{ \"result\": {sum(numbers) / len(numbers)} }}".encode('utf-8')
        )
