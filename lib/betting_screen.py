import pygame
import sys
import os
from lib.profiles import load_profiles, save_profiles  # 프로필 로드 및 저장 함수
from lib.sound import noise_click  # noise_click 함수 가져오기
from random import choice

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블랙잭 게임")

# 배경 이미지 로드
base_dir = os.path.dirname(__file__)
background_path = os.path.join(base_dir, "../assets/title_screen.png")
try:
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print(f"배경 이미지 파일을 찾을 수 없습니다: {background_path}")
    sys.exit()

# 색상 정의
BUTTON_BORDER_COLOR = (218, 177, 76)  # 노란색 테두리
BUTTON_BACKGROUND_COLOR = (0, 0, 0)  # 검정색 배경
BUTTON_TEXT_COLOR = (218, 177, 76)    # 노란색 글씨
BACKGROUND_COLOR = (2, 51, 0)        # 녹색 배경

# 폰트 설정
base_dir = os.path.dirname(__file__)
font_path = os.path.join(base_dir, "../assets/NanumGothic.ttf")
try:
    FONT_LARGE = pygame.font.Font(font_path, 50)
except FileNotFoundError:
    print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
    sys.exit()

def draw_button(text, pos, width, height):
    """버튼을 그리는 함수"""
    x, y = pos
    # 테두리 및 배경
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x - width // 2, y - height // 2, width, height), border_radius=10)
    pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x - width // 2 + 5, y - height // 2 + 5, width - 10, height - 10), border_radius=10)
    # 텍스트
    text_surface = FONT_LARGE.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x - width // 2, y - height // 2, width, height)

def betting_screen(profile_id):
    """베팅 설정 화면"""
    profiles = load_profiles()  # 프로필 데이터 로드
    player_money = profiles[profile_id]  # 선택된 프로필의 잔액
    if player_money is None or player_money < 100:
        print("게임 오버 되었습니다")
        from lib.main_menu import main_menu
        main_menu()
        return
    betting_amount = 100  # 초기 베팅 금액

    running = True
    while running:
        # 배경 색상
        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        # 현재 잔액 및 베팅금 표시
        balance_text = FONT_LARGE.render(f"잔액: {player_money}원", True, BUTTON_TEXT_COLOR)
        bet_text = FONT_LARGE.render(f"베팅금: {betting_amount}원", True, BUTTON_TEXT_COLOR)
        screen.blit(balance_text, balance_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 66)))
        screen.blit(bet_text, bet_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # 버튼 배치
        minus_button = draw_button("-", (SCREEN_WIDTH // 2 - 200, 550), 100, 70)
        all_in_button = draw_button("올인", (SCREEN_WIDTH // 2, 550), 150, 70)
        plus_button = draw_button("+", (SCREEN_WIDTH // 2 + 200, 550), 100, 70)

        play_button = draw_button("플레이", (SCREEN_WIDTH // 2 - 150, 650), 200, 70)
        quit_button = draw_button("그만두기", (SCREEN_WIDTH // 2 + 150, 650), 200, 70)

        # 버튼 클릭 처리
        if mouse_click:
            if minus_button.collidepoint(mouse_pos) and betting_amount > 100:
                noise_click()  # 버튼 클릭 효과음
                betting_amount -= 100
            if plus_button.collidepoint(mouse_pos) and betting_amount + 100 <= player_money:
                noise_click()  # 버튼 클릭 효과음
                betting_amount += 100
            if all_in_button.collidepoint(mouse_pos):
                noise_click()  # 버튼 클릭 효과음
                betting_amount = player_money

            if play_button.collidepoint(mouse_pos):
                noise_click()  # 버튼 클릭 효과음
                print(f"게임 시작! 베팅금: {betting_amount}원")
                profiles[profile_id] -= betting_amount  # 베팅금 차감
                save_profiles(profiles)  # 프로필 데이터 저장

                from lib.game_screen import game_screen
                game_screen(profile_id, betting_amount)  # 프로필 ID와 베팅금만 전달
                return
            if quit_button.collidepoint(mouse_pos):
                noise_click()  # 버튼 클릭 효과음
                print("프로필 화면으로 돌아가기")
                from lib.profile_screen import profile_screen
                profile_screen()
                return None

        pygame.display.flip()

