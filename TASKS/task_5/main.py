from TASKS.consts import BACKGROUND_MUSIC_PATH
from TASKS.task_5.handlers.main_handler import MainHandler
from TASKS.task_5.handlers.solution_handler import Solution
from TASKS.utils.design import Color, Console, Developer, Message
from TASKS.utils.music import BackgroundMusic


class Main:

    @staticmethod
    def main():
        music = BackgroundMusic(BACKGROUND_MUSIC_PATH, loop=True, volume=0.3)
        music.play()
        sol = Solution()
        while True:
            Console.clear()
            MainHandler.menu()
            your_choice = MainHandler.getChoice()
            Console.clear()
            match your_choice:
                case '1':
                    sol.task_1()
                case '2':
                    sol.task_2()
                case '3':
                    sol.task_3()
                case '4':
                    sol.task_4()
                case '5':
                    sol.task_5()
                case '6':
                    sol.task_6()
                case '7':
                    sol.task_7()
                case '0':
                    Message.print_message(
                        'Осуществляем выход из программы...', Color.PURPLE, Color.LIGHT_WHITE
                    )
                    music.stop()
                    exit(0)
                case '?':
                    Developer.print_info_of_developer()
                    Message.wait_for_enter()
            if your_choice not in '12345670?':
                Message.print_message(
                    'Введен некорректный номер подзадачи.', Color.RED, Color.LIGHT_WHITE
                )
                Message.wait_for_enter()


if __name__ == "__main__":
    Main.main()
