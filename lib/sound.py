import os
import pygame

# Pygame 초기화
pygame.init()

# 설정 파일 경로 설정
data_folder = os.path.join(os.path.dirname(__file__), "../data")
audio_config_path = os.path.join(data_folder, "audio.conf")

# 오디오 파일 경로 설정
assets_folder = os.path.join(os.path.dirname(__file__), "../assets")
music_path = os.path.join(assets_folder, "casino_theme.mp3")
card_sound_path = os.path.join(assets_folder, "card_slide.mp3")
click_sound_path = os.path.join(assets_folder, "click.wav")  # 클릭 효과음 경로 추가

# 오디오 설정 읽기
def load_audio_config():
    """오디오 설정을 불러오는 함수"""
    if not os.path.exists(audio_config_path):
        raise FileNotFoundError(f"설정 파일 {audio_config_path}이(가) 없습니다.")
    
    music_volume = 50
    sound_effect_volume = 50

    with open(audio_config_path, "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split("=")
            if key == "music":
                music_volume = int(value)
            elif key == "sound_effect":
                sound_effect_volume = int(value)

    return music_volume, sound_effect_volume

# 오디오 설정 저장
def save_audio_config(music_volume, sound_effect_volume):
    with open(audio_config_path, "w", encoding="utf-8") as file:
        file.write(f"music={music_volume}\n")
        file.write(f"sound_effect={sound_effect_volume}\n")

# 볼륨 설정
music_volume, sound_effect_volume = load_audio_config()
pygame.mixer.music.set_volume(music_volume / 100.0)

def play_music():
    """배경 음악을 재생하는 함수"""
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # 무한 반복
        music_volume, _ = load_audio_config()
        pygame.mixer.music.set_volume(music_volume / 100)  # 볼륨 조정 (0.0~1.0)
    except pygame.error as e:
        print(f"오디오 파일 로드 오류: {e}")

def noise_card():
    """카드 사운드 효과"""
    try:
        sound_effect = pygame.mixer.Sound(card_sound_path)
        _, sound_effect_volume = load_audio_config()
        sound_effect.set_volume(sound_effect_volume / 100)  # 볼륨 조정 (0.0~1.0)
        sound_effect.play()
    except pygame.error as e:
        print(f"사운드 효과 파일 로드 오류: {e}")

def noise_click():
    """클릭 효과음"""
    try:
        click_sound = pygame.mixer.Sound(click_sound_path)
        _, sound_effect_volume = load_audio_config()
        click_sound.set_volume(sound_effect_volume / 100)  # 볼륨 조정 (0.0~1.0)
        click_sound.play()
    except pygame.error as e:
        print(f"클릭 효과음 파일 로드 오류: {e}")

def set_volume(music_volume=None, sound_effect_volume=None):
    """볼륨을 설정하고 저장하는 함수"""
    current_music_volume, current_sound_effect_volume = load_audio_config()
    music_volume = music_volume if music_volume is not None else current_music_volume
    sound_effect_volume = sound_effect_volume if sound_effect_volume is not None else current_sound_effect_volume

    # 볼륨 저장
    save_audio_config(music_volume, sound_effect_volume)

    # Pygame 볼륨 적용
    pygame.mixer.music.set_volume(music_volume / 100)
    print(f"음악 볼륨: {music_volume}, 효과음 볼륨: {sound_effect_volume}")

# 예제 실행
if __name__ == "__main__":
    try:
        play_music()  # 프로그램 실행 시 음악 재생
        noise_card()  # 카드 효과음 재생
        noise_click()  # 클릭 효과음 재생
    except FileNotFoundError as e:
        print(e)
