from TASKS.utils.design import Color, Message


class MainHandler:

    @staticmethod
    def menu():
        Message.print_message(
            "          Список функций, реализуемых с помощью PySpark:          ",
            Color.LIGHT_WHITE,
            Color.BLUE,
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 1. Количество фильмов каждой категории.                            |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 2. Самые популярные актёры.                                        |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 3. Самые прибыльные категории.                                     |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 4. Фильмы, которые пока что не в прокате.                          |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 5. Топ 3 актёров в категории фильмов <Дети>.                       |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 6. Активность гостей по городам.                                   |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| 7. Лучшие категории по просмотрам, включающие заданные символы.    |"
            + Color.RESET
        )
        print(
            Color.LIGHT_WHITE
            + Color.BOLD
            + "| ?. Информация о разработчике.                                      |"
            + Color.RESET,
            end='',
        )
        Message.print_message(
            "0. Выход из программы.                                            ",
            Color.LIGHT_WHITE,
            Color.RED,
        )

    @staticmethod
    def getChoice() -> str:
        Message.print_message("Что желаете реализовать ?", Color.LIGHT_WHITE, Color.CYAN)
        return input()
