# 빠른 시작 가이드

5분 안에 rtllib 시작하기.

## 설치

```bash
pip install rtllib
```

## 기본 워크플로우

### 1. 클라이언트 임포트 및 생성

```python
from rtllib import Client

# 클라이언트 생성 (서버 자동 시작)
client = Client()
```

### 2. 서버 상태 확인

```python
health = client.health_check()
print(health)
# {'status': 'ok', 'backend_type': 'dummy'}
```

### 3. Verilog 파일 로드

```python
result = client.read_verilog("/path/to/design.v")
print(f"상태: {result['status']}")
print(f"모듈 발견: {result['modules_found']}")
```

### 4. 컴파일 및 엘라보레이트

```python
# 컴파일
message = client.compile()
print(message)  # "Compilation completed"

# 엘라보레이트
message = client.elaborate()
print(message)  # "Elaboration completed"
```

### 5. 설계 쿼리

```python
# 모든 모듈 가져오기
modules = client.get_modules()
for mod in modules:
    print(f"모듈: {mod['name']}")
    print(f"  포트: {len(mod['ports'])}")
    print(f"  인스턴스: {len(mod['instances'])}")
    print(f"  넷: {len(mod['nets'])}")

# 특정 모듈의 포트 가져오기
ports = client.get_ports("top_module")
for port in ports:
    print(f"{port['name']}: {port['direction']} [{port['width']} bits]")
```

### 6. 정리

```python
# 클라이언트 종료 및 서버 중지
client.close()
```

## 컨텍스트 매니저 사용 (권장)

```python
from rtllib import Client

# 컨텍스트 매니저로 자동 정리
with Client() as client:
    # 설계 로드
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # 쿼리
    modules = client.get_modules()
    print(f"{len(modules)}개 모듈 발견")

# 여기서 서버가 자동으로 중지됩니다
```

## 완전한 예제

```python
from rtllib import Client

def analyze_design(verilog_file):
    """Verilog 설계를 분석하고 요약을 출력합니다."""
    with Client() as client:
        # 로드 및 처리
        result = client.read_verilog(verilog_file)
        if result['status'] != 'success':
            print(f"오류: {result}")
            return

        client.compile()
        client.elaborate()

        # 모듈 가져오기
        modules = client.get_modules()
        print(f"\n설계 요약:")
        print(f"  전체 모듈: {len(modules)}")

        # 각 모듈 분석
        for mod in modules:
            print(f"\n  모듈: {mod['name']}")
            print(f"    파일: {mod['file']}")
            print(f"    포트: {len(mod['ports'])}")
            print(f"    인스턴스: {len(mod['instances'])}")
            print(f"    넷: {len(mod['nets'])}")

            # 포트 상세 정보 표시
            for port in mod['ports']:
                print(f"      - {port['name']}: {port['direction']} [{port['width']}]")

if __name__ == "__main__":
    analyze_design("/path/to/your/design.v")
```

## 일반적인 패턴

### 필터와 함께 쿼리

```python
# 입력 포트만 가져오기
input_ports = client.get_ports("top", filter="direction == 'input'")

# 멀티비트 넷만 가져오기
buses = client.get_nets("top", filter="width > 1")
```

### 계층 구조 쿼리

```python
# 설계 계층 구조의 모든 인스턴스 가져오기
all_instances = client.get_modules(hierarchical=True)
for mod in all_instances:
    if mod['path']:
        print(f"계층 구조 인스턴스: {mod['path']}")
```

### 여러 파일 읽기

```python
# 파일리스트 생성
with open("files.f", "w") as f:
    f.write("/path/to/top.v\n")
    f.write("/path/to/cpu.v\n")
    f.write("/path/to/memory.v\n")

# 파일리스트에서 읽기
result = client.read_verilog_filelist("files.f")
print(f"{result['files_read']}개 파일 읽음")
print(f"{result['modules_found']}개 모듈 발견")
```

### 세션 기반 수정

```python
with Client() as client:
    # 설계 로드
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # 새 포트 추가
    result = client.add_port(
        module="top",
        port_name="debug_out",
        direction="output",
        width=8
    )
    print(f"포트 추가됨: {result['success']}")

    # 새 넷 추가
    result = client.add_net(
        module="top",
        net_name="debug_bus",
        width=8,
        net_type="wire"
    )
    print(f"넷 추가됨: {result['success']}")

    # 수정된 설계 쿼리
    ports = client.get_ports("top")
    print(f"Top 모듈에 이제 {len(ports)}개 포트")
```

## 외부 서버

서버를 별도로 관리하려는 경우:

```bash
# 터미널 1: 서버 시작
rtllib-server --port 8000
```

```python
# 터미널 2: 외부 서버에 연결
from rtllib import Client

client = Client(host="127.0.0.1", port=8000, auto_start=False)
health = client.health_check()
print(health)
```

## 다음 단계

- 📚 [명령어 레퍼런스](commands/queries.md) - 사용 가능한 모든 명령어 배우기
- 🔍 [쿼리](commands/queries.md) - 설계 정보 읽기
- ✏️ [뮤테이션](commands/mutations.md) - 설계 상태 수정
- 📖 [타입](commands/types.md) - 데이터 구조 이해
- 💡 [예제](examples/basic-operations.md) - 더 많은 사용 예제
