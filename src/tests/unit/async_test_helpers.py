import asyncio

from unittest import mock


def async_mock(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))

    return wrapper


# class MockResponse:
#     def __init__(self, text, status):
#         self._text = text
#         self.status = status
#
#     async def text(self):
#         return self._text
#
#     async def __aexit__(self, exc_type, exc, tb):
#         pass
#
#     async def __aenter__(self):
#         return self
