import os
import pygame
import sys
from lib.profile_screen import profile_screen  # 프로필 화면 호출
from lib.sound import load_audio_config, set_volume, noise_click  # 오디오 설정 함수 가져오기

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블랙잭 게임")

# 색상 및 폰트 설정
BUTTON_BORDER_COLOR = (218, 177, 76)  # 노란색 테두리
BUTTON_BACKGROUND_COLOR = (0, 0, 0)  # 검정색 배경
BUTTON_TEXT_COLOR = (218, 177, 76)    # 노란색 글씨
BACKGROUND_COLOR = (2, 51, 0)       # 녹색 배경
SLIDER_COLOR = (218, 177, 76)        # 슬라이더 색상
TEXT_COLOR = (255, 255, 255)         # 흰색
font_path = os.path.join(os.path.dirname(__file__), "../assets/NanumGothic.ttf") # 한글 폰트

try:
    FONT_SMALL = pygame.font.Font(font_path, 30)  # 작은 크기의 한글 폰트
    FONT_LARGE = pygame.font.Font(font_path, 50)  # 큰 크기의 한글 폰트
except FileNotFoundError:
    print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
    sys.exit()

# 볼륨 값 (전역 상태로 유지)
current_volume = 0.5  # 초기 볼륨 값
show_settings = False  # 설정 UI 표시 여부

# 배경 이미지 로드
base_dir = os.path.dirname(__file__)
background_path = os.path.join(base_dir, "../assets/title_screen.png")
try:
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print(f"배경 이미지 파일을 찾을 수 없습니다: {background_path}")
    sys.exit()

# 버튼 정보
buttons = [
    {"text": "시작", "pos": (640, 400), "action": "start"},
    {"text": "설정", "pos": (640, 500), "action": "settings"},
    {"text": "종료", "pos": (640, 600), "action": "quit"},
]

def draw_button(text, pos, surface, hover):
    """버튼을 그리는 함수"""
    x, y = pos
    width, height = 300, 70

    # 버튼 테두리
    pygame.draw.rect(surface, BUTTON_BORDER_COLOR, (x - width // 2, y - height // 2, width, height), border_radius=10)

    # 버튼 배경
    pygame.draw.rect(surface, BUTTON_BACKGROUND_COLOR, (x - width // 2 + 5, y - height // 2 + 5, width - 10, height - 10), border_radius=10)

    # 버튼 텍스트
    text_surface = FONT_LARGE.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

    return pygame.Rect(x - width // 2, y - height // 2, width, height)

def draw_settings_ui():
    """설정 UI를 오른쪽 아래에 표시"""
    # 현재 볼륨 읽기
    music_volume, sound_effect_volume = load_audio_config()
    x, y = 960, 500
    width, height = 300, 200

    # 설정 UI 테두리
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), border_radius=0)

    # 설정 UI 배경
    pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x + 5, y + 5, width - 10, height - 10), border_radius=0)

    # 볼륨 슬라이더
    slider_x, slider_y = x + 20, y + 90
    slider_width, slider_height = 260, 10
    knob_x = slider_x + int(music_volume * slider_width / 100)  # 음악 볼륨 슬라이더 위치

    # 슬라이더 바
    pygame.draw.rect(screen, SLIDER_COLOR, (slider_x, slider_y, slider_width, slider_height))

    # 슬라이더 노브
    pygame.draw.circle(screen, SLIDER_COLOR, (knob_x, slider_y + slider_height // 2), 10)

    # 볼륨 값 텍스트
    volume_text = f"음악 볼륨: {music_volume}%"
    text_surface = FONT_SMALL.render(volume_text, True, BUTTON_TEXT_COLOR)
    screen.blit(text_surface, (x + 20, y + 50))

    # 효과음 슬라이더
    slider_effect_y = slider_y + 70  # 효과음 슬라이더 위치
    knob_effect_x = slider_x + int(sound_effect_volume * slider_width / 100)  # 효과음 볼륨 슬라이더 위치

    pygame.draw.rect(screen, SLIDER_COLOR, (slider_x, slider_effect_y, slider_width, slider_height))
    pygame.draw.circle(screen, SLIDER_COLOR, (knob_effect_x, slider_effect_y + slider_height // 2), 10)

    effect_text = f"효과음 볼륨: {sound_effect_volume}%"
    effect_text_surface = FONT_SMALL.render(effect_text, True, BUTTON_TEXT_COLOR)
    screen.blit(effect_text_surface, (x + 20, slider_effect_y - 40))

    # 이벤트 처리
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    # 음악 볼륨 슬라이더 조정
    if mouse_click and slider_x <= mouse_pos[0] <= slider_x + slider_width and slider_y - 10 <= mouse_pos[1] <= slider_y + slider_height + 10:
        music_volume = int((mouse_pos[0] - slider_x) / slider_width * 100)
        set_volume(music_volume=music_volume)

    # 효과음 볼륨 슬라이더 조정
    if mouse_click and slider_x <= mouse_pos[0] <= slider_x + slider_width and slider_effect_y - 10 <= mouse_pos[1] <= slider_effect_y + slider_height + 10:
        sound_effect_volume = int((mouse_pos[0] - slider_x) / slider_width * 100)
        set_volume(sound_effect_volume=sound_effect_volume)

    # 닫기 버튼 (정사각형)
    close_button_size = 30
    close_button_rect = pygame.Rect(x + width - close_button_size - 10, y + 10, close_button_size, close_button_size)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, close_button_rect)  # 테두리
    pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, close_button_rect.inflate(-5, -5))  # 내부 배경

    # 닫기 버튼 텍스트 (X)
    close_text = FONT_SMALL.render("X", True, BUTTON_TEXT_COLOR)
    text_rect = close_text.get_rect(center=close_button_rect.center)
    screen.blit(close_text, text_rect)

    return close_button_rect

def main_menu():
    """메인 메뉴 화면"""
    global show_settings
    while True:
        # 배경 이미지 그리기
        screen.blit(background_image, (0, 0))

        # 화면 그리기 및 버튼 처리
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
            if event.type == pygame.KEYDOWN:  # 키보드 이벤트 처리
                if event.key == pygame.K_ESCAPE and show_settings:  # ESC 키 처리
                    show_settings = False
                    
        # 버튼 그리기
        for button in buttons:
            button_rect = draw_button(
                button["text"],
                button["pos"],
                screen,
                hover=button["pos"][0] - 150 < mouse_pos[0] < button["pos"][0] + 150 and
                      button["pos"][1] - 35 < mouse_pos[1] < button["pos"][1] + 35
            )

            # 버튼 클릭 처리
            if mouse_click and button_rect.collidepoint(mouse_pos):
                noise_click()  # 버튼 클릭 효과음 추가
                if button["action"] == "start":
                    profile_screen()
                elif button["action"] == "settings":
                    show_settings = not show_settings
                elif button["action"] == "quit":
                    pygame.quit()
                    sys.exit()

        # 설정 UI 표시
        if show_settings:
            close_button_rect = draw_settings_ui()
            if mouse_click and close_button_rect.collidepoint(mouse_pos):
                noise_click()  # 닫기 버튼 클릭 효과음 추가
                show_settings = False

        pygame.display.flip()
        
if __name__ == "__main__":
    main_menu()
