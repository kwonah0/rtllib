# RTL Library 튜토리얼

이 디렉토리는 rtllib 코드베이스를 이해하기 위한 실습 중심 튜토리얼을 포함합니다.

## 튜토리얼 구성

### Tutorial 1: 전체 아키텍처 이해
- 파일: `tutorial_1_basic.py`
- 학습 내용:
  - Client-Server 자동 시작 메커니즘
  - GraphQL을 통한 통신 흐름
  - Backend Protocol 패턴
  - 데이터 흐름: Client → HTTP → FastAPI → GraphQL → Backend

### Tutorial 2: 로그 스트리밍 시스템
- 파일: `tutorial_2_log_stream.py`
- 학습 내용:
  - PubSub 패턴 구현
  - WebSocket을 통한 GraphQL Subscription
  - 비동기 로그 처리와 동기 API 공존
  - 로그 흐름: Backend → LogHandler → PubSub → WebSocket → Client

### Tutorial 3: 클라이언트 SDK 심화
- 파일: `tutorial_3_server_manager.py`
- 학습 내용:
  - ServerManager의 자동 포트 할당
  - Subprocess 관리
  - 헬스체크 메커니즘
  - 리소스 정리 및 Context Manager

### Tutorial 4: GraphQL 직접 호출
- 파일: `tutorial_4_graphql.py`
- 학습 내용:
  - Query, Mutation, Subscription 사용법
  - gql 라이브러리 활용
  - GraphQL Introspection
  - 에러 처리 및 타입 안전성

### Tutorial 5: 전체 통합 실습
- 파일: `tutorial_5_integration.py`
- 학습 내용:
  - 전체 워크플로우 통합
  - 실제 사용 시나리오
  - 에러 처리 및 복구
  - 성능 모니터링

## 실행 방법

각 튜토리얼은 독립적으로 실행 가능합니다:

```bash
# rtllib 디렉토리에서 실행
cd /path/to/rtllib

# Tutorial 1 실행
uv run python tutorials/tutorial_1_basic.py

# Tutorial 2 실행
uv run python tutorials/tutorial_2_log_stream.py

# 이하 동일...
```

## 학습 순서

1. **Tutorial 1** - 기본 아키텍처 이해
2. **Tutorial 2** - 로그 스트리밍 (선택)
3. **Tutorial 3** - ServerManager 심화 (선택)
4. **Tutorial 4** - GraphQL 직접 사용 (선택)
5. **Tutorial 5** - 전체 통합 (필수)

## 코드 구조 이해

### 서버 (rtllib-server)
```
rtllib-server/
├── backend/
│   ├── protocol.py    # Backend 인터페이스 정의
│   └── dummy.py       # 테스트용 구현
├── schema.py          # GraphQL 스키마
├── server.py          # FastAPI 서버
├── pubsub.py         # 로그 브로드캐스팅
└── log_handler.py    # 로그 캡처
```

### 클라이언트 (rtllib)
```
rtllib/
├── client.py          # 메인 Client 클래스
├── server_manager.py  # 서버 프로세스 관리
├── log_stream.py     # WebSocket 로그 수신
└── types.py          # 타입 정의
```

## 핵심 개념

### 1. Protocol 패턴
```python
class Backend(Protocol):
    def read_verilog(self, path: str) -> dict: ...
    def compile(self) -> None: ...
```
- 구조적 서브타이핑으로 유연한 백엔드 구현

### 2. PubSub 패턴
```python
LogHandler → publish() → [Queue1, Queue2, ...] → Subscribers
```
- 여러 구독자에게 동시 브로드캐스팅

### 3. 자동 서버 관리
```python
with Client() as client:  # 자동 시작
    client.compile()      # 사용
# 자동 종료
```

## 다음 단계

튜토리얼 완료 후:
1. 코드 리뷰에서 발견된 이슈 개선
2. 테스트 작성
3. 보안 취약점 수정
4. PyInstaller 빌드 설정