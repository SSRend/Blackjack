import os
import pygame
from lib.main_menu import main_menu
from lib.sound import play_music

if __name__ == "__main__":
    play_music()  # 프로그램 실행 시 음악 재생
    main_menu()   # 메인 메뉴 시작
