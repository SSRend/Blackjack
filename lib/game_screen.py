import pygame
import sys
import os
from random import choice  # 추가: random 모듈에서 choice 함수 임포트
from lib.profiles import load_profiles, save_profiles, delete_profile
from lib.sound import noise_card, noise_click  # 소리 함수 가져오기

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블랙잭 게임")

# 색상 정의
BACKGROUND_COLOR = (2, 51, 0)        # 녹색 배경
BUTTON_BORDER_COLOR = (218, 177, 76)  # 노란색 테두리
BUTTON_BACKGROUND_COLOR = (0, 0, 0)  # 검정색 배경
BUTTON_TEXT_COLOR = (218, 177, 76)    # 노란색 글씨

# 폰트 설정
base_dir = os.path.dirname(__file__)
font_path = os.path.join(base_dir, "../assets/NanumGothic.ttf")
try:
    FONT_LARGE = pygame.font.Font(font_path, 50)
except FileNotFoundError:
    print(f"폰트 파일을 찾을 수 없습니다: {font_path}")
    sys.exit()

# 카드 이미지 경로
cards_folder = os.path.join(base_dir, "../assets/cards")
back_card_path = os.path.join(cards_folder, "back.png")

# 카드 크기
CARD_WIDTH, CARD_HEIGHT = 125, 180

# 카드 이미지 로드
def load_card_image(card_name):
    """카드 이미지 파일을 로드"""
    card_path = os.path.join(cards_folder, f"{card_name}.png")
    try:
        card_image = pygame.image.load(card_path)
        return pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
    except FileNotFoundError:
        print(f"카드 이미지 파일을 찾을 수 없습니다: {card_path}")
        sys.exit()

# 버튼 그리기
def draw_button(text, pos, width, height):
    """버튼을 그리는 함수"""
    x, y = pos
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x - width // 2, y - height // 2, width, height), border_radius=10)
    pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x - width // 2 + 5, y - height // 2 + 5, width - 10, height - 10), border_radius=10)
    text_surface = FONT_LARGE.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x - width // 2, y - height // 2, width, height)

# 승부 화면
def game_screen(profile_id, betting_amount):
    """게임 화면"""
    CARD_WIDTH, CARD_HEIGHT = 125, 180  # 카드 크기 설정

    popup_active = False
    popup_message = None
    popup_start_time = 0

    def initialize_deck():
        """52장의 카드를 초기화합니다."""
        suits = ['s', 'd', 'h', 'c']
        ranks = [str(i) for i in range(1, 14)]
        return [f"{suit}{rank}" for suit in suits for rank in ranks]

    def draw_random_card(deck):
        """덱에서 무작위 카드를 뽑고, 제거한 뒤 반환합니다."""
        if not deck:
            raise ValueError("덱에 더 이상 카드가 없습니다.")
        card = choice(deck)
        deck.remove(card)
        return card

    def calculate_score(cards):
        """카드 점수를 계산하는 함수"""
        score = 0
        aces = 0
        for card in cards:
            rank = int(card[1:])
            if rank == 1:
                aces += 1
                score += 11
            elif rank > 10:
                score += 10
            else:
                score += rank
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def draw_cards(cards, y, spacing):
        """카드를 가로로 나열하여 화면에 중앙 정렬되게 그리는 함수"""
        total_width = (len(cards) - 1) * spacing + CARD_WIDTH  # 카드들의 총 너비 계산
        x_start = (SCREEN_WIDTH - total_width) // 2  # 화면 중앙을 기준으로 카드 시작 위치 계산

        for i, card in enumerate(cards):
            x_pos = x_start + i * spacing
            card_image = load_card_image(card)
            screen.blit(card_image, (x_pos, y))

    def draw_popup_message(message):
        """팝업 메시지를 표시하는 함수"""
        nonlocal popup_active, popup_message, popup_start_time
        popup_width, popup_height = 500, 150
        x, y = (SCREEN_WIDTH - popup_width) // 2, (SCREEN_HEIGHT - popup_height) // 2 + 150

        # 팝업 테두리와 배경
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, popup_width, popup_height), border_radius=10)
        pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x + 5, y + 5, popup_width - 10, popup_height - 10), border_radius=10)

        # 텍스트 표시 (여러 줄 처리)
        lines = message.split("\n")  # 줄바꿈 기준으로 메시지를 나눔
        for i, line in enumerate(lines):
            text_surface = FONT_LARGE.render(line, True, BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y + 50 + i * 50))  # 50px 간격
            screen.blit(text_surface, text_rect)

        if not popup_active:  # 팝업이 처음 활성화되는 경우
            popup_active = True
            popup_message = message
            popup_start_time = pygame.time.get_ticks()  # 팝업 시작 시간 기록
        else:  # 팝업이 이미 활성화된 경우
            current_time = pygame.time.get_ticks()
            # 1초 후 팝업 자동 닫기
            if current_time - popup_start_time > 1000:
                popup_active = False
                popup_message = None

        pygame.display.flip()


    def update_player_balance(profile_id, balance_change):
        """프로필의 잔액을 업데이트"""
        profiles = load_profiles()
        profiles[profile_id] += balance_change
        save_profiles(profiles)

    def is_blackjack(cards):
        """블랙잭 여부를 확인"""
        if len(cards) == 2 and calculate_score(cards) == 21:
            return True
        return False

    # 덱 초기화 및 카드 배분
    deck = initialize_deck()
    dealer_cards = [draw_random_card(deck), draw_random_card(deck)]
    player_cards = [draw_random_card(deck), draw_random_card(deck)]

    player_score = calculate_score(player_cards)
    reveal_dealer_score = False
    game_over = False
    winner_text = None

    # 블랙잭 확인
    if is_blackjack(player_cards):
        if is_blackjack(dealer_cards):  # 딜러도 블랙잭인지 확인
            winner_text = "둘 다 블랙잭!\n무승부입니다!"
            game_over = True
            reveal_dealer_score = True
        else:
            winner_text = "플레이어 블랙잭!\n플레이어 승리!"
            update_player_balance(profile_id, betting_amount * 2.5)  # 블랙잭 승리 시 배당금 2.5배 지급
            game_over = True
            reveal_dealer_score = True
        
    while True:
        screen.fill(BACKGROUND_COLOR)

        # 딜러 카드 표시
        if reveal_dealer_score:
            draw_cards(dealer_cards, 20, CARD_WIDTH + 10)  # 딜러 카드 위치 (y = 20)
        else:
            screen.blit(load_card_image(dealer_cards[0]), (SCREEN_WIDTH // 2 - CARD_WIDTH - 5, 20))
            screen.blit(load_card_image("back"), (SCREEN_WIDTH // 2 + 5, 20))

        # 플레이어 카드 표시
        draw_cards(player_cards, 412.5, CARD_WIDTH + 10)  # 플레이어 카드 위치 (y = 412.5)

        # 점수 및 베팅금 텍스트
        dealer_text = FONT_LARGE.render(f"딜러 : {calculate_score(dealer_cards) if reveal_dealer_score else '??'}점", True, BUTTON_TEXT_COLOR)
        player_text = FONT_LARGE.render(f"플레이어 : {player_score}점", True, BUTTON_TEXT_COLOR)
        bet_text = FONT_LARGE.render(f"베팅금 : {betting_amount}원", True, BUTTON_TEXT_COLOR)

        # 텍스트 위치
        screen.blit(dealer_text, dealer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)))
        screen.blit(player_text, player_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
        screen.blit(bet_text, bet_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # 팝업 활성 상태 처리
        if popup_active:
            current_time = pygame.time.get_ticks()  # 현재 시간 확인

            # 팝업 자동 닫기 처리 (1초 후)
            if current_time - popup_start_time > 1000:  # 1초 후 팝업 자동 닫기
                popup_active = False
                popup_message = None
            else:
                # 팝업 그리기
                popup_width, popup_height = 500, 150
                x, y = (SCREEN_WIDTH - popup_width) // 2, (SCREEN_HEIGHT - popup_height) // 2 + 150

                pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, popup_width, popup_height), border_radius=10)
                pygame.draw.rect(screen, BUTTON_BACKGROUND_COLOR, (x + 5, y + 5, popup_width - 10, popup_height - 10), border_radius=10)

                # 팝업 텍스트 출력
                lines = popup_message.split("\n")
                for i, line in enumerate(lines):
                    text_surface = FONT_LARGE.render(line, True, BUTTON_TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y + 50 + i * 50))
                    screen.blit(text_surface, text_rect)

                pygame.display.flip()  # 팝업 상태일 때 화면 갱신
                return  # 팝업 활성화 상태에서는 다른 로직 무시

        
        # 게임 종료 처리
        if game_over:
            draw_popup_message(winner_text)

            # 팝업이 닫힐 때까지 대기
            while popup_active:
                current_time = pygame.time.get_ticks()  # 현재 시간 확인
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # 팝업 활성 상태이고 0.5초가 지난 경우에만 닫기 허용
                        if current_time - popup_start_time > 500:
                            popup_active = False

            # 프로필 데이터 로드
            profiles = load_profiles()
            if profiles[profile_id] is None or profiles[profile_id] < 100:  # 플레이어 잔액 확인
                # 잔액이 100원 미만인 경우 프로필 삭제
                delete_profile(profile_id)
                save_profiles(profiles)  # 변경 사항 저장
                draw_popup_message("게임 오버 되었습니다.\n프로필이 삭제되었습니다.")
                from lib.main_menu import main_menu
                main_menu()
                return
            else:
                from lib.betting_screen import betting_screen
                betting_screen(profile_id)
            return

        if not game_over:
            hit_button = draw_button("Hit", (SCREEN_WIDTH // 2 - 150, 650), 200, 70)
            stand_button = draw_button("Stand", (SCREEN_WIDTH // 2 + 150, 650), 200, 70)

        # 이벤트 처리
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        if not game_over:
            if mouse_click:
                if hit_button.collidepoint(mouse_pos):
                    noise_card()  # 카드 효과음
                    new_card = draw_random_card(deck)
                    player_cards.append(new_card)
                    player_score = calculate_score(player_cards)
                    if player_score >= 21:
                        if player_score == 21:
                            reveal_dealer_score = True
                            winner_text = "플레이어 승리!"
                            update_player_balance(profile_id, betting_amount * 2)
                        else:
                            winner_text = "딜러 승리!"
                            update_player_balance(profile_id, 0)
                        game_over = True
                if stand_button.collidepoint(mouse_pos):
                    noise_click()  # 클릭 효과음
                    reveal_dealer_score = True

                    # 딜러가 17점 이상이 될 때까지 카드 추가
                    while calculate_score(dealer_cards) < 17:
                        dealer_cards.append(draw_random_card(deck))
                        pygame.display.flip()
                        #pygame.time.wait(2000)

                    dealer_score = calculate_score(dealer_cards)

                    # 결과 판단
                    if dealer_score > 21 or player_score > dealer_score:
                        winner_text = "플레이어 승리!"
                        update_player_balance(profile_id, betting_amount * 2)  # 승리 시 베팅금 두 배 지급
                    elif dealer_score == player_score:
                        winner_text = "무승부!"
                        update_player_balance(profile_id, betting_amount)  # 베팅금 반환
                    else:
                        winner_text = "딜러 승리!"
                        update_player_balance(profile_id, 0)  # 베팅금 차감
                    game_over = True

        pygame.display.flip()
