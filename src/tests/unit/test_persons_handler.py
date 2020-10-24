from unittest import mock

import pytest

from fastapi.exceptions import HTTPException

from app.api import dal, persons_handler
from tests.unit import sample_data
from tests.unit.async_test_helpers import async_mock, async_test


@async_test
@mock.patch("app.api.dal.select_persons", new=async_mock())
async def test_read_persons_valid():
    dal.select_persons = async_mock()
    dal.database = async_mock()
    dal.database.fetch_all = async_mock(return_value=sample_data.persons_record)
    mock_loop = async_mock()
    mock_loop.is_running = mock.Mock()
    mock_loop.get_debug = mock.Mock()
    mock_loop.is_closed = mock.Mock()
    actual = await persons_handler.read_persons()
    assert actual == sample_data.valid_persons_response


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
