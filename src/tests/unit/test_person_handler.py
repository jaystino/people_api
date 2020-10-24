from unittest import mock

import pytest

from fastapi.exceptions import HTTPException

from app.api import dal, person_handler
from tests.unit import sample_data
from tests.unit.async_test_helpers import async_mock, async_test


@async_test
@mock.patch("app.api.dal.select_persons", new=async_mock())
async def test_read_person_valid():
    dal.select_person = async_mock()
    dal.database = async_mock()
    dal.database.fetch_one = async_mock(return_value=sample_data.person_record)
    mock_loop = async_mock()
    mock_loop.is_running = mock.Mock()
    mock_loop.get_debug = mock.Mock()
    mock_loop.is_closed = mock.Mock()
    actual = await person_handler.read_person(
        "5f2f95ab-8683-49ea-a755-50273c956e66", None
    )
    assert actual == sample_data.valid_person_response


@async_test
@mock.patch("app.api.dal.select_persons", new=async_mock())
async def test_read_person_version_valid():
    dal.select_person = async_mock()
    dal.database = async_mock()
    dal.database.fetch_one = async_mock(return_value=sample_data.person_record)
    mock_loop = async_mock()
    mock_loop.is_running = mock.Mock()
    mock_loop.get_debug = mock.Mock()
    mock_loop.is_closed = mock.Mock()
    actual = await person_handler.read_person("5f2f95ab-8683-49ea-a755-50273c956e66", 2)
    assert actual == sample_data.valid_person_response


@async_test
@mock.patch("app.api.dal.select_persons", new=async_mock())
async def test_read_person_version_invalid():
    dal.select_person = async_mock()
    dal.database = async_mock()
    dal.database.fetch_one = async_mock(return_value=None)
    mock_loop = async_mock()
    mock_loop.is_running = mock.Mock()
    mock_loop.get_debug = mock.Mock()
    mock_loop.is_closed = mock.Mock()
    with pytest.raises(HTTPException):
        await person_handler.read_person("5f2f95ab-8683-49ea-a755-50273c956e66", 25)
