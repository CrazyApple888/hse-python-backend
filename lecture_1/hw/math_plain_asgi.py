import uvicorn

from lecture_1.hw.exceptions import HttpException
from lecture_1.hw.routes import routes


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def send_response(send, code: int, body: bytes):
    await send({
        'type': 'http.response.start',
        'status': code,
        'headers': [
            [b'content-type', b'application/json'],
        ],
    })

    if body is not None:
        await send({
            'type': 'http.response.body',
            'body': body,
        })


async def handle_request(scope, receive, send):
    route = scope['path']
    for handler in routes:
        if handler.is_suitable(route):
            response = await handler.handle(
                route,
                scope['query_string'],
                await read_body(receive),
            )
            await send_response(send, response.code, response.body)
            return

    raise HttpException(404, "Not found")


async def app(scope, receive, send):
    try:
        await handle_request(scope, receive, send)
    except HttpException as exception:
        await send_response(send, exception.code, exception.message.encode("utf-8"))
    except ValueError:
        await send_response(send, 422, "Unprocessable entity".encode("utf-8"))


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
