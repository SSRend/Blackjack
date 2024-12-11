# 블랙잭 게임 프로젝트

## 영상
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/pfahNW5eyLI/0.jpg)](https://www.youtube.com/watch?v=pfahNW5eyLI)
클릭 시, 유튜브로 이동합니다.

## 소개
이 프로젝트는 Python과 Pygame 라이브러리를 사용하여 구현한 블랙잭 게임입니다. 사용자는 프로필을 생성하고, 게임에 베팅하며, 딜러와 경쟁하여 승리 여부를 확인할 수 있습니다. 

## 주요 기능
- **프로필 관리**: 프로필 생성, 삭제, 잔액 확인 및 잔액 부족 시 자동 삭제 기능.
- **게임 로직**:
  - 52장의 카드 덱 초기화 및 무작위 카드 분배.
  - 딜러와 플레이어의 점수를 계산하고 블랙잭 여부 확인.
  - 승패 판단 후 잔액 업데이트.
- **UI 및 상호작용**:
  - 직관적인 버튼과 팝업 메시지로 사용자 경험 강화.
  - 일정 시간 후 자동으로 닫히는 팝업.
- **음향 효과**: 클릭 및 카드 배분 시 효과음.

## 실행 방법
1. Python 3.8 이상을 설치하세요.
2. Blackjack.zip을 다운로드 받고, 압축을 해제합니다.
3. 프로젝트 폴더로 이동 후, 필요한 라이브러리를 설치합니다:
   ```bash
   pip install pygame
4. 다음 명령어로 게임을 실행하세요.
   python main.py
4a. 또는, vscode로 해당 폴더를 열어 main.py를 실행하면 됩니다.

## 학습한 점
Pygame 활용: UI 구성, 이벤트 처리, 화면 갱신의 기본 구조를 이해했습니다.
타이머 및 팝업 구현: 일정 시간 후 자동으로 닫히는 타이머 기반 팝업을 구현하며 시간을 효과적으로 처리하는 방법을 배웠습니다.
게임 로직 설계: 블랙잭 규칙에 따라 점수를 계산하고 승패를 판단하는 알고리즘을 설계했습니다.
오류 처리: 덱의 카드가 부족한 상황, 프로필 관련 예외 상황 등을 처리하며 예외 처리의 중요성을 느꼈습니다.

## 향후 개선점
더 세련된 UI와 애니메이션 추가.
네트워크 기능을 통해 멀티플레이 지원.
AI 딜러를 개선하여 더 도전적인 게임 제공.

## AI 도구 활용

이 프로젝트의 개발 과정에서 OpenAI의 **ChatGPT**를 다음과 같은 목적으로 사용하였습니다:

1. **코드 디버깅**: 복잡한 오류를 이해하고 해결책을 탐색하는 데 도움을 받았습니다.
2. **코드 최적화**: 더 효율적인 코드 작성 방식을 제안받았습니다.
3. **문서 작성**: `README.md` 작성 및 라이선스, 프로젝트 설명을 개선하기 위해 사용하였습니다.

챗GPT는 단순히 조언자로 활용되었으며, 최종 코드와 문서는 스스로의 판단과 수정 과정을 거쳐 작성되었습니다.

## 라이선스
이 프로젝트는 MIT License를 따릅니다.

- **게임 OST**: [출처 링크](https://www.youtube.com/watch?v=DCTggKrpMWs)
- **카드 효과음**: [출처 링크](https://cdn.pixabay.com/download/audio/2022/03/10/audio_e2a2453389.mp3?filename=card-sounds-35956.mp3)
- **클릭 효과음**: [출처 링크](https://assets.mixkit.co/active_storage/sfx/1119/1119.wav)


