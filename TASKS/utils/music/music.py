import time

import pygame


def play_background_music(file_path: str, loop: bool = True):
    try:

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1 if loop else 0)
    except pygame.error as e:
        print(f"Ошибка воспроизведения: {e}")


def stop_background_music():
    pygame.mixer.music.stop()


def main():

    music_file = consts.background_music
    play_background_music(music_file)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_background_music()
