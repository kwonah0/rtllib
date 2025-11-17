# rtllib

Verilog/SystemVerilog HDL 설계를 위한 Python 클라이언트 라이브러리입니다.

## 개요

rtllib는 Verilog/SystemVerilog RTL 설계를 로드하고 쿼리하고 수정하기 위한 Python 인터페이스를 제공합니다. Yosys 같은 백엔드와 통신하는 서버-클라이언트 아키텍처를 기반으로 합니다.

## 주요 기능

- **설계 로드**: Verilog/SystemVerilog 파일 읽기
- **계층 구조 쿼리**: 모듈, 포트, 인스턴스, 넷 정보 조회
- **GraphQL API**: 유연하고 타입 안전한 쿼리
- **세션 기반 수정**: 포트와 넷 추가 (세션 내)
- **자동 서버 관리**: 내장 서버 자동 시작/중지
- **타입 안전**: 모든 API 응답에 대한 완전한 TypedDict 타입

## 빠른 시작

```python
from rtllib import Client

with Client() as client:
    # 설계 로드
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # 모듈 쿼리
    modules = client.get_modules()
    for mod in modules:
        print(f"Module: {mod['name']}")
        print(f"  Ports: {len(mod['ports'])}")
        print(f"  Instances: {len(mod['instances'])}")
```

## 설치

```bash
pip install rtllib
```

## 문서 구조

- **[명령어 개요](commands/overview.md)** - 모든 사용 가능한 명령어
- **[쿼리](commands/queries.md)** - 읽기 전용 작업
- **[뮤테이션](commands/mutations.md)** - 설계 수정 작업
- **[타입](commands/types.md)** - 데이터 타입 레퍼런스
- **[예제](examples/basic-operations.md)** - 일반적인 사용 패턴

## 기본 워크플로우

```python
from rtllib import Client

with Client() as client:
    # 1. 설계 로드
    client.read_verilog("/path/to/design.v")

    # 2. 처리
    client.compile()
    client.elaborate()

    # 3. 쿼리
    modules = client.get_modules()
    ports = client.get_ports("module_name")
    instances = client.get_instances("module_name")
    nets = client.get_nets("module_name")

    # 4. 수정 (선택사항, 세션 기반)
    client.add_port("module", "new_port", "input", 8)
    client.add_net("module", "new_net", 32, "wire")
```

## 주요 기능

### 중첩 객체 API

모든 쿼리는 완전한 중첩 객체를 반환합니다:

```python
modules = client.get_modules()
# 각 모듈은 포트, 인스턴스, 넷을 포함합니다
for mod in modules:
    for port in mod['ports']:  # 중첩된 PortInfo 리스트
        print(f"  {port['name']}: {port['direction']}")
```

### 필터링

백엔드별 필터 표현식 지원:

```python
# 입력 포트만 가져오기
inputs = client.get_ports("top", filter="direction == 'input'")

# 멀티비트 넷만 가져오기
buses = client.get_nets("top", filter="width > 1")
```

### 계층 구조 쿼리

설계 계층 구조 탐색:

```python
modules = client.get_modules(hierarchical=True)
for mod in modules:
    if mod['path']:
        print(f"Instance: {mod['path']}")
```

### 타입 안전

모든 응답에 대한 완전한 TypedDict 타입:

```python
from rtllib.types import ModuleInfo, PortInfo

modules: list[ModuleInfo] = client.get_modules()
ports: list[PortInfo] = client.get_ports("top")
```

## 다음 단계

- 🔍 [쿼리 레퍼런스](commands/queries.md) - 모든 쿼리 명령어
- ✏️ [뮤테이션 레퍼런스](commands/mutations.md) - 모든 수정 명령어
- 📖 [타입 레퍼런스](commands/types.md) - 데이터 구조 이해하기
- 💡 [예제](examples/basic-operations.md) - 더 많은 사용 예제

## 라이선스

MIT License

## 기여

이슈와 풀 리퀘스트를 환영합니다!
