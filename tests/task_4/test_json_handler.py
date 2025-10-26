from unittest.mock import MagicMock, patch

import pytest

from TASKS.task_4.handlers import DBConnection, JSONHandler
from TASKS.utils.design import Message

patcher = patch.object(Message, "print_message", lambda *a, **k: None)
patcher.start()


@patch("builtins.open")
@patch("json.load")
def test_init_loads_json(mock_json_load, mock_open):
    mock_json_load.return_value = [{"id": 1, "name": "Alice"}]

    db_mock = MagicMock(spec=DBConnection)
    handler = JSONHandler(db_mock, "students.json")

    assert "students.json" in handler.data
    assert handler.data["students.json"] == [{"id": 1, "name": "Alice"}]


def test_load_data_to_db_file_missing():
    db_mock = MagicMock(spec=DBConnection)
    handler = JSONHandler(db_mock)
    handler.data = {}  # пустой словарь данных

    mapping = {"nonexistent.json": "students"}
    handler.load_data_to_db(mapping)


def test_load_data_to_db_empty_file():
    db_mock = MagicMock(spec=DBConnection)
    handler = JSONHandler(db_mock)
    handler.data = {"empty.json": []}

    mapping = {"empty.json": "students"}
    handler.load_data_to_db(mapping)


def test_load_data_to_db_raises_on_execute_error():
    db_mock = MagicMock(spec=DBConnection)
    db_mock.execute.side_effect = Exception("DB error")

    handler = JSONHandler(db_mock)
    handler.data = {"students.json": [{"id": 1, "name": "Alice"}]}

    mapping = {"students.json": "students"}
    with pytest.raises(Exception) as excinfo:
        handler.load_data_to_db(mapping)

    assert "DB error" in str(excinfo.value)
