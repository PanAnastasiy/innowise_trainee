from unittest.mock import MagicMock

import pytest

from TASKS.task_4.data_manager import Executer


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.execute = MagicMock()
    return db


@pytest.fixture
def executer(mock_db):
    return Executer(mock_db)


def test_list_rooms_count_students(executer, mock_db):
    mock_db.execute.return_value = [
        {"Room's number": "101", "Count of students in room": 3},
        {"Room's number": "102", "Count of students in room": 2},
    ]

    result = executer.list_rooms_count_students()
    assert isinstance(result, list)
    assert all(isinstance(r, dict) for r in result)
    assert result[0]["Room's number"] == "101"
    mock_db.execute.assert_called_once()


def test_rooms_smallest_avg_age(executer, mock_db):
    mock_db.execute.return_value = [
        {"Room's number": "101", "Average age of students": 18.5},
    ]

    result = executer.rooms_smallest_avg_age(limit=1)
    assert len(result) == 1
    assert "Average age of students" in result[0]
    mock_db.execute.assert_called_once()
    sql = mock_db.execute.call_args[0][0]
    assert "LIMIT 1" in sql


def test_rooms_largest_age_diff(executer, mock_db):
    mock_db.execute.return_value = [
        {"Room's number": "102", "Difference in the age of students": 4},
    ]

    result = executer.rooms_largest_age_diff(limit=1)
    assert result[0]["Difference in the age of students"] == 4
    sql = mock_db.execute.call_args[0][0]
    assert "LIMIT 1" in sql


def test_rooms_different_sex(executer, mock_db):
    mock_db.execute.return_value = [
        {"List of rooms where different-sex students live": "101"},
    ]

    result = executer.rooms_different_sex()
    assert isinstance(result, list)
    assert "List of rooms where different-sex students live" in result[0]


def test_rooms_same_sex(executer, mock_db):
    mock_db.execute.return_value = [
        {"List of rooms where same-sex students live": "102"},
    ]

    result = executer.rooms_same_sex()
    assert isinstance(result, list)
    assert "List of rooms where same-sex students live" in result[0]
