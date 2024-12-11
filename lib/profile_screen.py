import os
import pygame
import sys
import time
from lib.betting_screen import betting_screen  # 베팅 화면 호출
from lib.profiles import load_profiles, save_profiles, create_profile, delete_profile
from lib.sound import noise_click  # noise_click 함수 가져오기

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블랙잭 게임")

# 색상 정의
BUTTON_BORDER_COLOR = (218, 177, 76)  # 노란색 테두리
BUTTON_BACKGROUND_COLOR = (0, 0, 0)  # 검정색 배경
BUTTON_TEXT_COLOR = (218, 177, 76)    # 노란색 글씨
POPUP_BACKGROUND_COLOR = (0, 0, 0)    # 팝업 배경색
POPUP_TEXT_COLOR = (218, 177, 76)     # 팝업 텍스트색

# 폰트 설정 (한글 폰트 파일 사용)
base_dir = os.path.dirname(__file__)
font_path = os.path.join(base_dir, "../assets/NanumGothic.ttf")

try:
    FONT_SMALL = pygame.font.Font(font_path, 30)
    FONT_LARGE = pygame.font.Font(font_path, 50)
except FileNotFoundError:
    print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
    sys.exit()

# 배경 이미지 로드
background_path = os.path.join(base_dir, "../assets/title_screen.png")
try:
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print(f"배경 이미지 파일을 찾을 수 없습니다: {background_path}")
    sys.exit()

# 연필 아이콘 로드
icon_path = os.path.join(base_dir, "../assets/edit_icon.png")
try:
    edit_icon = pygame.image.load(icon_path)
    edit_icon = pygame.transform.scale(edit_icon, (30, 30))
except FileNotFoundError:
    print(f"아이콘 파일을 찾을 수 없습니다: {icon_path}")
    sys.exit()

# 팝업 상태
popup_message = None
popup_time = 0
confirmation_popup = False
selected_profile = -1  # 현재 선택된 프로필


def draw_button(text, pos, width, height, hover):
    """버튼을 그리는 함수"""
    x, y = pos
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x - width // 2, y - height // 2, width, height), border_radius=10)
    pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x - width // 2 + 5, y - height // 2 + 5, width - 10, height - 10), border_radius=10)
    text_surface = FONT_LARGE.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x - width // 2, y - height // 2, width, height)


def draw_edit_button(pos, size):
    """연필 아이콘을 포함한 버튼을 그리는 함수"""
    x, y = pos
    width, height = size
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x - width // 2, y - height // 2, width, height), border_radius=10)
    pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x - width // 2 + 5, y - height // 2 + 5, width - 10, height - 10), border_radius=10)
    screen.blit(edit_icon, (x - 15, y - 15))
    return pygame.Rect(x - width // 2, y - height // 2, width, height)


def draw_popup(message, fade_out=False, confirmation=False):
    """팝업 창을 그리는 함수"""
    global popup_message, popup_time
    popup_width, popup_height = 700, 300
    x, y = (SCREEN_WIDTH - popup_width) // 2, (SCREEN_HEIGHT - popup_height) // 2 + 133

    # 팝업 테두리와 배경
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, popup_width, popup_height), border_radius=10)
    pygame.draw.rect(screen, POPUP_BACKGROUND_COLOR, (x + 5, y + 5, popup_width - 10, popup_height - 10), border_radius=10)

    # 메시지 텍스트
    lines = message.split("\n")
    for i, line in enumerate(lines):
        text_surface = FONT_LARGE.render(line, True, POPUP_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y + 70 + i * 60))
        screen.blit(text_surface, text_rect)

    # 네/아니오 버튼 추가 (확인 팝업인 경우)
    if confirmation:
        yes_button = draw_button("네", (x + 200, y + 200), 175, 75, False)
        no_button = draw_button("아니오", (x + 500, y + 200), 175, 75, False)
        return yes_button, no_button

    # 자동 닫기 처리
    if fade_out and time.time() - popup_time > 1:  # 1초 후 닫힘
        popup_message = None
    return None, None


def profile_screen():
    """프로필 선택 화면"""
    global popup_message, popup_time, confirmation_popup, selected_profile

    profiles = load_profiles()  # 딕셔너리 형태로 프로필 데이터 로드
    
        # 100점 미만의 프로필 자동 삭제
    for profile_key, score in profiles.items():
        if score is not None and score < 100:  # 점수가 100점 미만인 경우
            delete_profile(profile_key)  # 해당 프로필 삭제
    profiles = load_profiles()  # 업데이트된 프로필 다시 로드
    
    running = True

    while running:
        # 배경 이미지 그리기
        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from lib.main_menu import main_menu  # 메인 메뉴로 이동
                    main_menu()
                    return

        # 팝업이 활성화된 경우 처리
        if popup_message or confirmation_popup:
            if popup_message:
                draw_popup(popup_message, fade_out=True)

            if confirmation_popup:
                yes_button, no_button = draw_popup("프로필을 삭제하시겠습니까?", confirmation=True)
                if mouse_click:
                    if yes_button and yes_button.collidepoint(mouse_pos):
                        noise_click()  # 버튼 클릭 효과음
                        delete_profile(f"user{selected_profile + 1}")  # 프로필 삭제
                        profiles = load_profiles()  # 업데이트된 프로필 다시 로드
                        confirmation_popup = False
                    elif no_button and no_button.collidepoint(mouse_pos):
                        noise_click()  # 버튼 클릭 효과음
                        confirmation_popup = False

            pygame.display.flip()
            continue

        # 프로필 버튼 및 연필 아이콘 그리기
        for i in range(3):  # 인덱스를 통해 user1, user2, user3로 매핑
            if i == 2:  # 마지막 버튼은 "뒤로가기"로 변경
                back_button = draw_button("뒤로가기", (640, 400 + i * 100), 300, 70, False)
                if mouse_click and back_button.collidepoint(mouse_pos):
                    noise_click()  # 버튼 클릭 효과음
                    from lib.main_menu import main_menu
                    main_menu()  # 메인 메뉴로 이동
                    return
                continue
            
            profile_key = f"user{i + 1}"
            profile_text = f"프로필 {i + 1}" if profiles[profile_key] is not None else "빈 프로필"

            # 프로필 버튼
            profile_button = draw_button(profile_text, (640, 400 + i * 100), 300, 70, False)

            # 연필 아이콘 버튼
            edit_button = draw_edit_button((840, 415 + i * 100), (50, 50))

            if mouse_click:
                # 프로필 버튼 클릭 처리
                if profile_button.collidepoint(mouse_pos):
                    noise_click()  # 버튼 클릭 효과음
                    if profiles[profile_key] is not None:  # 프로필이 존재하는 경우
                        betting_screen(profile_key)  # user1, user2로 전달
                    else:
                        popup_message = "프로필이 없습니다.\n오른쪽 아이콘을 눌러서\n프로필을 생성하십시오."
                        popup_time = time.time()

                # 연필 아이콘 클릭 처리
                if edit_button.collidepoint(mouse_pos):
                    noise_click()  # 버튼 클릭 효과음
                    if profiles[profile_key] is not None:  # 프로필이 이미 존재
                        confirmation_popup = True
                        selected_profile = i  # 선택된 프로필 인덱스 저장
                    else:  # 새 프로필 생성
                        create_profile(profile_key)
                        profiles = load_profiles()  # 업데이트된 프로필 다시 로드
                        popup_message = "프로필이 생성되었습니다."
                        popup_time = time.time()

        pygame.display.flip()

if __name__ == "__main__":
    profile_screen()
