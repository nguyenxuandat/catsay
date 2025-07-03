async def app(scope, receive, send):
    body = "Hello, world! I'm here again!"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "header": [
                [b"content-type", b"text/plain"],
                [b"content-length", len(body)],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": body.encode("utf-8"),
        }
    )
