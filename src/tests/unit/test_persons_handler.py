import asyncio

from unittest import mock
from uuid import UUID

import pytest

from fastapi.exceptions import HTTPException

from app.api import dal, persons_handler


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


class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@async_test
@mock.patch("app.api.dal.select_persons", new=async_mock())
async def test_read_persons_valid():
    records = [
        dict(
            record=1,
            person_id=UUID("5f2f95ab-8683-49ea-a755-50273c956e66"),
            first_name="a",
            last_name="b",
            version=2,
            is_latest=True,
        )
    ]
    dal.select_persons = async_mock()
    dal.database = async_mock()
    dal.database.fetch_all = async_mock(return_value=records)
    mock_loop = async_mock()
    mock_loop.is_running = mock.Mock()
    mock_loop.get_debug = mock.Mock()
    mock_loop.is_closed = mock.Mock()
    actual = await persons_handler.read_persons()
    expected = {
        "persons": [
            {
                "first_name": "a",
                "is_latest": True,
                "last_name": "b",
                "person_id": "5f2f95ab-8683-49ea-a755-50273c956e66",
                "record": 1,
                "version": 2,
            }
        ]
    }
    assert actual == expected


@async_test
@mock.patch("app.api.dal.select_persons", new=async_mock())
async def test_read_persons_no_records():
    dal.select_persons = async_mock()
    dal.database = async_mock()
    dal.database.fetch_all = async_mock(return_value=None)
    mock_loop = async_mock()
    mock_loop.is_running = mock.Mock()
    mock_loop.get_debug = mock.Mock()
    mock_loop.is_closed = mock.Mock()
    with pytest.raises(HTTPException):
        await persons_handler.read_persons()
