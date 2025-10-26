from unittest.mock import MagicMock, patch

import pytest

from TASKS.task_4.handlers import DBConnection
from TASKS.utils.design import Message

patcher = patch.object(Message, "print_message", lambda *a, **k: None)
patcher.start()


@patch("psycopg2.connect")
def test_context_manager_connect_close(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    with DBConnection(
        host="localhost", port=5432, database="testdb", user="user", password="pass"
    ) as db:
        assert db.conn is not None
        assert db.cursor is not None
        mock_connect.assert_called_once_with(
            host="localhost",
            port=5432,
            database="testdb",
            user="user",
            password="pass",
        )

    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("psycopg2.connect")
def test_execute_select(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "Room #1"}]
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    with DBConnection() as db:
        result = db.execute("SELECT * FROM room")
        assert result == [{"id": 1, "name": "Room #1"}]  # исправлено
        mock_cursor.execute.assert_called_once_with("SELECT * FROM room", None)


@patch("psycopg2.connect", side_effect=Exception("Connection failed"))
def test_connection_failure(mock_connect):
    with pytest.raises(Exception) as excinfo:
        with DBConnection():
            pass
    assert "Connection failed" in str(excinfo.value)


@patch("psycopg2.connect")
def test_execute_non_select(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    with DBConnection() as db:
        result = db.execute("UPDATE room SET name='Room #1-01' WHERE id=1")
        assert result is None
        mock_conn.commit.assert_called_once()


@patch("psycopg2.connect")
def test_execute_rollback_on_error(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Query failed")
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    with DBConnection() as db:
        with pytest.raises(Exception) as excinfo:
            db.execute("SELECT * FROM room")
        mock_conn.rollback.assert_called_once()
        assert "Query failed" in str(excinfo.value)
