import os

# 프로필 파일 경로
data_folder = os.path.join(os.path.dirname(__file__), "../data")
users_conf_path = os.path.join(data_folder, "users.conf")

def load_profiles():
    """users.conf에서 프로필 데이터를 읽어옵니다."""
    if not os.path.exists(users_conf_path):
        # 기본 프로필 생성
        default_profiles = {"user1": 1000, "user2": None, "user3": None}
        save_profiles(default_profiles)
        return default_profiles

    profiles = {}
    with open(users_conf_path, "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split("=")
            profiles[key] = int(value) if value.isdigit() else None
    return profiles

def save_profiles(profiles):
    """users.conf에 프로필 데이터를 저장합니다."""
    with open(users_conf_path, "w", encoding="utf-8") as file:
        for key, value in profiles.items():
            file.write(f"{key}={value if value is not None else 'null'}\n")

def update_profile(profile_name, money):
    """프로필의 잔액을 업데이트합니다."""
    profiles = load_profiles()
    if profile_name not in profiles:
        raise ValueError(f"{profile_name} 프로필이 존재하지 않습니다.")
    profiles[profile_name] = money
    save_profiles(profiles)

def create_profile(profile_name):
    """새 프로필 생성"""
    profiles = load_profiles()
    if profile_name in profiles and profiles[profile_name] is not None:
        raise ValueError("프로필 이름이 이미 존재하거나 사용 중입니다.")
    profiles[profile_name] = 1000  # 기본 잔액
    save_profiles(profiles)
    
def delete_profile(profile_name):
    """프로필 삭제"""
    profiles = load_profiles()
    if profile_name not in profiles:
        raise ValueError(f"{profile_name} 프로필이 존재하지 않습니다.")
    profiles[profile_name] = None  # 프로필 값을 None으로 설정
    save_profiles(profiles)
    print(f"{profile_name} 프로필이 삭제되었습니다.")
