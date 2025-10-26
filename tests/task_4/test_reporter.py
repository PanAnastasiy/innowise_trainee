import json
from decimal import Decimal

import pytest

from TASKS.task_4.data_manager import JSONReporter, XMLReporter


@pytest.fixture
def sample_data():
    return {
        "rooms_count_students": [
            {"Room's number": "101", "Count of students in room": 3},
            {"Room's number": "102", "Count of students in room": 2},
        ],
        "rooms_smallest_avg_age": [
            {"Room's number": "101", "Average age of students": Decimal('18.5')}
        ],
    }


def test_json_reporter_format(sample_data):
    reporter = JSONReporter()
    output = reporter.format(sample_data)
    parsed = json.loads(output)  # проверяем, что можно распарсить обратно
    assert parsed["rooms_count_students"][0]["Room's number"] == "101"
    assert (
        parsed["rooms_smallest_avg_age"][0]["Average age of students"] == "18.5"
    )  # Decimal -> str


def test_json_reporter_save(tmp_path, sample_data):
    reporter = JSONReporter()
    file_path = tmp_path / "report.json"
    reporter.save(sample_data, str(file_path))
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "rooms_count_students" in data


def test_xml_reporter_format(sample_data):
    reporter = XMLReporter()
    output = reporter.format(sample_data)
    assert "<analysis_results>" in output
    assert "Room_s_number" in output or "Room_s_number" in output.replace(
        "'", "_"
    )  # проверка sanitize_tag
    assert "18.5" in output


def test_xml_reporter_save(tmp_path, sample_data):
    reporter = XMLReporter()
    file_path = tmp_path / "report.xml"
    reporter.save(sample_data, str(file_path))
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<analysis_results>" in content
