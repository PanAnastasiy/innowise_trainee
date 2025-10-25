from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.sax.saxutils import escape


class OutputReporter(ABC):

    @abstractmethod
    def format(self, data: dict[str, list[dict[str, Any]]]) -> str:
        """Возвращает строку в нужном формате."""
        pass

    def save(self, data: dict[str, list[dict[str, Any]]], filename: str) -> None:
        """Сохраняет отформатированные данные в файл."""
        output = self.format(data)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)


class JSONReporter(OutputReporter):

    def format(self, data: dict[str, list[dict[str, Any]]]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4, default=str)


class XMLReporter(OutputReporter):

    def sanitize_tag(self, tag: str) -> str:
        """Превращает ключ словаря в корректное имя XML-тега"""
        import re
        tag = tag.replace(' ', '_').replace("'", "_")
        tag = re.sub(r'[^a-zA-Z0-9_-]', '', tag)
        if tag and tag[0].isdigit():
            tag = '_' + tag
        return tag

    def format_value(self, value: Any) -> str:
        """Конвертирует Decimal и экранирует спецсимволы"""
        if isinstance(value, Decimal):
            value = float(value)
        return escape(str(value))

    def format(self, data: dict[str, list[dict[str, Any]]]) -> str:
        root = ET.Element("analysis_results")

        for query_name, items in data.items():
            query_element = ET.SubElement(root, "query", name=self.sanitize_tag(str(query_name)))
            for item in items:
                item_element = ET.SubElement(query_element, "item")
                for key, value in item.items():
                    field = ET.SubElement(item_element, self.sanitize_tag(str(key)))
                    field.text = self.format_value(value)

        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")