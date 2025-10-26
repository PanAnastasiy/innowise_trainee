import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any
from xml.dom import minidom
from xml.sax.saxutils import escape


class OutputReporter(ABC):
    """
    Абстрактный базовый класс для создания отчётов в различных форматах (JSON, XML и др.).
    """

    @abstractmethod
    def format(self, data: dict[str, list[dict[str, Any]]]) -> str:
        """
        Форматирует входные данные в строку требуемого формата.

        :param data: Словарь, где ключ — название запроса, значение — список результатов (список словарей).
        :return: Отформатированная строка.
        """
        pass

    def save(self, data: dict[str, list[dict[str, Any]]], filename: str) -> None:
        """
        Сохраняет отформатированные данные в файл.

        :param data: Результаты запросов к бд в виде словаря.
        :param filename: Путь к файлу, куда будет сохранён отчёт.
        """
        output = self.format(data)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)


class JSONReporter(OutputReporter):
    """
    Класс, сохраняющий данные в формате JSON.
    """

    def format(self, data: dict[str, list[dict[str, Any]]]) -> str:
        """
        Преобразует данные в отформатированную JSON-строку.

        :param data: Словарь с результатами анализа.
        :return: Строка JSON с отступами.
        """
        return json.dumps(data, ensure_ascii=False, indent=4, default=str)


class XMLReporter(OutputReporter):
    """
    Класс, сохраняющий данные в формате XML.
    """

    @staticmethod
    def sanitize_tag(tag: str) -> str:
        """
        Преобразует строку в корректное имя XML-тега, ругалось на пробелы и на апосторофы:
        - заменяет пробелы и апострофы на подчёркивания,
        - удаляет недопустимые символы,

        :param tag: Исходный ключ.
        :return: Корректное имя XML-тега.
        """
        import re

        tag = tag.replace(' ', '_').replace("'", "_")
        tag = re.sub(r'[^a-zA-Z0-9_-]', '', tag)
        if tag and tag[0].isdigit():
            tag = '_' + tag
        return tag

    @staticmethod
    def format_value(value: Any) -> str:
        """
        Преобразует значение в строку для XML:
        - конвертирует Decimal в float,
        - экранирует спецсимволы (&, <, > и т.д.).

        :param value: Значение из базы данных.
        :return: Безопасная строка.
        """
        if isinstance(value, Decimal):
            value = float(value)
        return escape(str(value))

    def format(self, data: dict[str, list[dict[str, Any]]]) -> str:
        """
        Формирует XML-документ из словаря данных.

        :param data: Словарь с результатами анализа.
        :return: Строка XML в читаемом виде.
        """
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
