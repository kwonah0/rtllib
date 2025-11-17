# 뮤테이션 명령어 레퍼런스

RTL Library 서버에서 설계 상태를 수정하는 모든 뮤테이션 명령어입니다.

---

## read_verilog

단일 Verilog/SystemVerilog 파일을 읽습니다.

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| file_path | str | ✅ | - | Verilog 파일 경로 |

**반환:** `ReadVerilogResult`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| status | str | "success" 또는 "error" |
| message | str | 상태 메시지 |
| modules_found | int | 발견된 모듈 수 |

**예제 (Python):**

```python
from rtllib import Client

with Client() as client:
    result = client.read_verilog("/path/to/cpu.v")

    if result['status'] == 'success':
        print(f"{result['modules_found']}개 모듈 발견")
    else:
        print(f"오류: {result['message']}")
```

**예제 (GraphQL):**

```graphql
mutation ReadVerilog($filePath: String!) {
  read_verilog(file_path: $filePath) {
    status
    message
    modules_found
  }
}
```

**관련:** [read_verilog_filelist](#read_verilog_filelist), [compile](#compile)

---

## read_verilog_filelist

파일리스트 파일에서 여러 Verilog 파일을 읽습니다.

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| filelist_path | str | ✅ | - | .f 파일리스트 파일 경로 |

**반환:** `ReadFilelistResult`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| status | str | "success" 또는 "error" |
| message | str | 상태 메시지 |
| files_read | int | 읽은 파일 수 |
| modules_found | int | 발견된 모듈 수 |

**예제 (Python):**

```python
# files.f 생성
with open("design.f", "w") as f:
    f.write("# Top level\n")
    f.write("/path/to/top.v\n")
    f.write("\n")
    f.write("# Subsystems\n")
    f.write("/path/to/cpu.v\n")
    f.write("/path/to/memory.v\n")

# 파일리스트 읽기
with Client() as client:
    result = client.read_verilog_filelist("design.f")

    if result['status'] == 'success':
        print(f"{result['files_read']}개 파일 읽음")
        print(f"{result['modules_found']}개 모듈 발견")
    else:
        print(f"오류: {result['message']}")
```

**예제 (GraphQL):**

```graphql
mutation ReadFilelist($filelistPath: String!) {
  read_verilog_filelist(filelist_path: $filelistPath) {
    status
    message
    files_read
    modules_found
  }
}
```

**관련:** [read_verilog](#read_verilog), [compile](#compile)

---

## compile

로드된 Verilog 설계를 컴파일합니다.

**매개변수:** 없음

**반환:** `str` (상태 메시지)

**예제 (Python):**

```python
with Client() as client:
    client.read_verilog("/path/to/design.v")

    # 설계 컴파일
    message = client.compile()
    print(message)  # "Compilation completed"
```

**예제 (GraphQL):**

```graphql
mutation {
  compile
}
```

**관련:** [elaborate](#elaborate), [read_verilog](#read_verilog)

---

## elaborate

설계 계층 구조를 엘라보레이트합니다.

**매개변수:** 없음

**반환:** `str` (상태 메시지)

**예제 (Python):**

```python
with Client() as client:
    client.read_verilog("/path/to/design.v")
    client.compile()

    # 계층 구조 엘라보레이트
    message = client.elaborate()
    print(message)  # "Elaboration completed"
```

**예제 (GraphQL):**

```graphql
mutation {
  elaborate
}
```

**관련:** [compile](#compile), [get_modules](queries.md#get_modules)

---

## add_port

모듈에 새 포트를 추가합니다 (세션 기반).

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | 모듈 이름 |
| port_name | str | ✅ | - | 새 포트 이름 |
| direction | str | ✅ | - | "input", "output", 또는 "inout" |
| width | int | ✅ | - | 비트 폭 |

**반환:** `AddPortResult`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| success | bool | 작업 성공 여부 |
| message | str | 상태 메시지 |
| port_name | str | 추가된 포트 이름 |

**예제 (Python):**

```python
with Client() as client:
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    # 디버그 포트 추가
    result = client.add_port(
        module="cpu",
        port_name="debug_out",
        direction="output",
        width=32
    )

    if result['success']:
        print(f"포트 추가됨: {result['port_name']}")

        # 포트 확인
        ports = client.get_ports("cpu")
        print(f"총 포트: {len(ports)}")
    else:
        print(f"오류: {result['message']}")
```

**예제 (GraphQL):**

```graphql
mutation AddPort(
  $module: String!,
  $portName: String!,
  $direction: String!,
  $width: Int!
) {
  add_port(
    module: $module,
    port_name: $portName,
    direction: $direction,
    width: $width
  ) {
    success
    message
    port_name
  }
}
```

**중요:** 세션 기반 수정은 디스크에 기록되지 않습니다. 현재 세션 동안만 유효합니다.

**관련:** [add_net](#add_net), [get_ports](queries.md#get_ports)

---

## add_net

모듈에 새 넷/와이어를 추가합니다 (세션 기반).

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | 모듈 이름 |
| net_name | str | ✅ | - | 새 넷 이름 |
| width | int | ✅ | - | 비트 폭 |
| net_type | str | ✅ | - | "wire" 또는 "reg" |

**반환:** `AddNetResult`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| success | bool | 작업 성공 여부 |
| message | str | 상태 메시지 |
| net_name | str | 추가된 넷 이름 |

**예제 (Python):**

```python
with Client() as client:
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    # 디버그 버스 추가
    result = client.add_net(
        module="cpu",
        net_name="debug_bus",
        width=32,
        net_type="wire"
    )

    if result['success']:
        print(f"넷 추가됨: {result['net_name']}")

        # 넷 확인
        nets = client.get_nets("cpu")
        print(f"총 넷: {len(nets)}")
    else:
        print(f"오류: {result['message']}")
```

**예제 (GraphQL):**

```graphql
mutation AddNet(
  $module: String!,
  $netName: String!,
  $width: Int!,
  $netType: String!
) {
  add_net(
    module: $module,
    net_name: $netName,
    width: $width,
    net_type: $netType
  ) {
    success
    message
    net_name
  }
}
```

**중요:** 세션 기반 수정은 디스크에 기록되지 않습니다. 현재 세션 동안만 유효합니다.

**관련:** [add_port](#add_port), [get_nets](queries.md#get_nets)

---

## 일반적인 워크플로우

### 기본 로드 및 처리

```python
from rtllib import Client

with Client() as client:
    # 1. 파일 읽기
    result = client.read_verilog("/path/to/design.v")
    if result['status'] != 'success':
        print(f"읽기 실패: {result['message']}")
        return

    # 2. 컴파일
    client.compile()

    # 3. 엘라보레이트
    client.elaborate()

    # 4. 쿼리
    modules = client.get_modules()
    print(f"{len(modules)}개 모듈 발견")
```

### 여러 파일

```python
# 방법 1: 파일리스트 사용
with Client() as client:
    result = client.read_verilog_filelist("design.f")
    print(f"{result['files_read']}개 파일, {result['modules_found']}개 모듈")

    client.compile()
    client.elaborate()

# 방법 2: 여러 read_verilog 호출
with Client() as client:
    client.read_verilog("/path/to/top.v")
    client.read_verilog("/path/to/cpu.v")
    client.read_verilog("/path/to/memory.v")

    client.compile()
    client.elaborate()
```

### 세션 수정

```python
with Client() as client:
    # 설계 로드
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    # 수정 전
    ports_before = client.get_ports("cpu")
    print(f"수정 전: {len(ports_before)} 포트")

    # 포트 추가
    client.add_port("cpu", "test_mode", "input", 1)
    client.add_port("cpu", "debug_out", "output", 32)

    # 넷 추가
    client.add_net("cpu", "debug_bus", 32, "wire")
    client.add_net("cpu", "test_signal", 1, "wire")

    # 수정 후
    ports_after = client.get_ports("cpu")
    nets = client.get_nets("cpu")

    print(f"수정 후: {len(ports_after)} 포트")
    print(f"넷: {len(nets)}")
```

### 오류 처리

```python
from rtllib import Client

def safe_load_design(verilog_file):
    """안전한 오류 처리로 설계를 로드합니다."""
    try:
        with Client() as client:
            # 파일 읽기
            result = client.read_verilog(verilog_file)
            if result['status'] != 'success':
                print(f"파일 읽기 실패: {result['message']}")
                return None

            # 컴파일
            try:
                client.compile()
            except Exception as e:
                print(f"컴파일 오류: {e}")
                return None

            # 엘라보레이트
            try:
                client.elaborate()
            except Exception as e:
                print(f"엘라보레이트 오류: {e}")
                return None

            # 성공
            return client.get_modules()

    except Exception as e:
        print(f"클라이언트 오류: {e}")
        return None

# 사용
modules = safe_load_design("/path/to/design.v")
if modules:
    print(f"{len(modules)}개 모듈 성공적으로 분석됨")
else:
    print("분석 실패")
```

## 중요한 참고사항

### 세션 기반 수정

`add_port`와 `add_net`는 **세션 기반** 작업입니다:

- ✅ 현재 세션 동안 유효
- ❌ 디스크에 기록되지 않음
- ❌ 소스 파일 수정 안 함
- ❌ 세션 간에 지속되지 않음

```python
# 세션 1
with Client() as client:
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    client.add_port("cpu", "debug", "output", 8)
    ports = client.get_ports("cpu")
    # debug 포트가 표시됨

# 세션 2 (새 클라이언트)
with Client() as client:
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    ports = client.get_ports("cpu")
    # debug 포트가 사라짐 - 세션 기반
```

### 명령어 순서

컴파일 및 엘라보레이트의 올바른 순서를 따르세요:

```python
# 올바른 순서
client.read_verilog(...)    # 1. 파일 읽기
client.compile()            # 2. 컴파일
client.elaborate()          # 3. 엘라보레이트
client.get_modules()        # 4. 쿼리

# 잘못된 순서 (오류 발생 가능)
client.elaborate()          # ❌ 먼저 컴파일해야 함
client.compile()
```

### 파일리스트 형식

파일리스트(.f) 파일은 다음을 지원합니다:

- 한 줄에 하나의 파일 경로
- `#`로 시작하는 주석
- 빈 줄 (무시됨)

```text
# design.f 예제
# Top level modules
/path/to/top.v

# CPU subsystem
/path/to/cpu.v
/path/to/alu.v

# Memory subsystem
/path/to/memory.v
/path/to/cache.v
```

## 다음 단계

- 🔍 [쿼리 레퍼런스](queries.md) - 설계 읽기 명령어
- 📊 [타입 레퍼런스](types.md) - 모든 데이터 타입
- 💡 [예제](../examples/basic-operations.md) - 더 많은 사용 예제
