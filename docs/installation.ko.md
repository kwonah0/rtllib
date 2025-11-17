# 설치 가이드

rtllib 설치 및 설정 방법입니다.

## 요구사항

- Python 3.10 이상
- pip 또는 uv (권장)

## 기본 설치

### pip 사용

```bash
pip install rtllib
```

### uv 사용 (권장)

```bash
uv add rtllib
```

## 서버 설치

rtllib는 서버-클라이언트 아키텍처를 사용합니다. 서버를 실행하는 세 가지 방법이 있습니다:

### 1. 자동 시작 (기본값, 권장)

클라이언트가 자동으로 서버를 시작하고 중지합니다:

```python
from rtllib import Client

# 서버가 자동으로 시작됩니다
with Client() as client:
    health = client.health_check()
    print(health)
# 서버가 자동으로 중지됩니다
```

**장점:**
- 설정 불필요
- 자동 리소스 관리
- 간단한 사용

**단점:**
- 각 Python 프로세스마다 서버 인스턴스 하나
- 긴 시작 시간 (Python 임포트 오버헤드)

### 2. 바이너리 서버 (프로덕션용)

빠른 시작을 위해 미리 빌드된 바이너리를 다운로드하세요:

```bash
# GitHub Releases에서 다운로드
curl -LO https://github.com/yourusername/rtllib-server/releases/latest/download/rtllib-server

# 실행 가능하게 만들기
chmod +x rtllib-server

# 서버 시작
./rtllib-server --port 8000
```

Python 클라이언트:

```python
from rtllib import Client

# 외부 서버에 연결 (자동 시작 안 함)
client = Client(host="127.0.0.1", port=8000, auto_start=False)
health = client.health_check()
print(health)
```

**장점:**
- 빠른 시작 (~100ms)
- 여러 클라이언트 간 공유 가능
- Python 런타임 불필요

**단점:**
- 별도 설치 필요
- 수동 프로세스 관리

### 3. 소스에서 서버 실행

개발이나 디버깅용:

```bash
# rtllib-server 저장소 클론
git clone https://github.com/yourusername/rtllib-server.git
cd rtllib-server

# 의존성 설치
uv sync

# 서버 실행
uv run python -m rtllib_server.cli --port 8000
```

Python 클라이언트:

```python
from rtllib import Client

client = Client(host="127.0.0.1", port=8000, auto_start=False)
```

**장점:**
- 소스 수준 디버깅
- 커스터마이징 가능
- 최신 개발 버전

**단점:**
- 개발 환경 필요
- 느린 시작

## 설정

### 클라이언트 설정

```python
from rtllib import Client

# 기본 설정 (자동 시작, 포트 5000)
client = Client()

# 커스텀 포트
client = Client(port=8000)

# 외부 서버
client = Client(host="127.0.0.1", port=8000, auto_start=False)

# 요청 타임아웃 설정
client = Client(timeout=30.0)  # 30초
```

### 서버 설정

바이너리 또는 소스 실행 시 서버 옵션:

```bash
# 커스텀 포트
rtllib-server --port 8000

# 커스텀 호스트
rtllib-server --host 0.0.0.0 --port 8000

# 로그 레벨 설정
rtllib-server --log-level debug
```

## 설치 확인

설치를 확인하려면:

```python
from rtllib import Client

with Client() as client:
    health = client.health_check()
    print(f"서버 상태: {health['status']}")
    print(f"백엔드: {health['backend_type']}")
```

예상 출력:

```python
서버 상태: ok
백엔드: dummy
```

## 문제 해결

### 서버가 시작되지 않음

자동 시작을 사용하는 경우:

```python
# 자세한 로깅 활성화
import logging
logging.basicConfig(level=logging.DEBUG)

from rtllib import Client
client = Client()
```

### 포트가 이미 사용 중

다른 포트 사용:

```python
client = Client(port=8001)
```

### 연결 오류

서버가 실행 중인지 확인:

```bash
# 바이너리를 사용하는 경우
ps aux | grep rtllib-server

# 프로세스 확인
netstat -an | grep 5000
```

### 임포트 오류

rtllib가 설치되어 있는지 확인:

```bash
pip list | grep rtllib
# or
uv pip list | grep rtllib
```

## 개발 설치

rtllib 개발에 기여하려는 경우:

```bash
# 클라이언트 저장소 클론
git clone https://github.com/yourusername/rtllib.git
cd rtllib

# 개발 의존성과 함께 설치
uv sync --all-extras

# 테스트 실행
uv run pytest
```

## 다음 단계

- 📚 [빠른 시작 가이드](quickstart.md) - 첫 번째 rtllib 프로그램 작성
- 🔍 [명령어 개요](commands/overview.md) - 사용 가능한 모든 명령어
- 💡 [예제](examples/basic-operations.md) - 일반적인 사용 패턴
