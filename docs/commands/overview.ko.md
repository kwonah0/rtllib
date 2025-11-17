# 명령어 개요

모든 rtllib 클라이언트 명령어에 대한 완전한 레퍼런스입니다.

## 명령어 카테고리

### [쿼리](queries.md)

설계 정보를 읽는 명령어 (읽기 전용 작업).

| 명령어 | 설명 |
|---------|-------------|
| [health_check](queries.md#health_check) | 서버 상태 확인 |
| [get_modules](queries.md#get_modules) | 중첩 데이터와 함께 모든 모듈 가져오기 |
| [get_ports](queries.md#get_ports) | 모듈 포트 가져오기 |
| [get_instances](queries.md#get_instances) | 모듈 인스턴스 가져오기 |
| [get_nets](queries.md#get_nets) | 모듈 넷/와이어 가져오기 |

### [뮤테이션](mutations.md)

설계 상태를 수정하는 명령어.

| 명령어 | 설명 |
|---------|-------------|
| [read_verilog](mutations.md#read_verilog) | 단일 Verilog 파일 읽기 |
| [read_verilog_filelist](mutations.md#read_verilog_filelist) | 파일리스트에서 여러 파일 읽기 |
| [compile](mutations.md#compile) | 로드된 설계 컴파일 |
| [elaborate](mutations.md#elaborate) | 설계 계층 구조 엘라보레이트 |
| [add_port](mutations.md#add_port) | 모듈에 포트 추가 (세션) |
| [add_net](mutations.md#add_net) | 모듈에 넷 추가 (세션) |

### [타입](types.md)

명령어가 반환하는 데이터 타입.

| 타입 | 설명 |
|------|-------------|
| [HealthCheckResult](types.md#healthcheckresult) | 서버 상태 |
| [ModuleInfo](types.md#moduleinfo) | 완전한 모듈 정보 |
| [PortInfo](types.md#portinfo) | 포트 정보 |
| [InstanceInfo](types.md#instanceinfo) | 인스턴스 정보 |
| [NetInfo](types.md#netinfo) | 넷/와이어 정보 |
| [ReadVerilogResult](types.md#readverilogresult) | 파일 읽기 결과 |
| [ReadFilelistResult](types.md#readfilelistresult) | 파일리스트 읽기 결과 |
| [AddPortResult](types.md#addportresult) | 포트 추가 결과 |
| [AddNetResult](types.md#addnetresult) | 넷 추가 결과 |

## 일반적인 워크플로우

```python
from rtllib import Client

with Client() as client:
    # 1. 상태 확인
    health = client.health_check()

    # 2. 설계 로드
    client.read_verilog("/path/to/design.v")
    # 또는
    client.read_verilog_filelist("/path/to/files.f")

    # 3. 설계 처리
    client.compile()
    client.elaborate()

    # 4. 설계 쿼리
    modules = client.get_modules()
    ports = client.get_ports("module_name")
    instances = client.get_instances("module_name")
    nets = client.get_nets("module_name")

    # 5. 설계 수정 (선택사항, 세션 기반)
    client.add_port("module", "port_name", "input", 8)
    client.add_net("module", "net_name", 32, "wire")
```

## 사용 사례별 명령어 그룹

### 설계 로드

- [read_verilog](mutations.md#read_verilog) - 단일 파일
- [read_verilog_filelist](mutations.md#read_verilog_filelist) - 여러 파일

### 설계 처리

- [compile](mutations.md#compile) - 구문/의미 분석
- [elaborate](mutations.md#elaborate) - 계층 구조 확장

### 설계 쿼리

- [get_modules](queries.md#get_modules) - 모든 모듈
- [get_ports](queries.md#get_ports) - 모듈의 포트
- [get_instances](queries.md#get_instances) - 모듈의 인스턴스
- [get_nets](queries.md#get_nets) - 모듈의 넷

### 설계 수정

- [add_port](mutations.md#add_port) - 모듈에 포트 추가
- [add_net](mutations.md#add_net) - 모듈에 넷 추가

### 시스템

- [health_check](queries.md#health_check) - 서버 상태

## 공통 매개변수

많은 명령어가 다음 공통 매개변수를 지원합니다:

### filter (선택사항)

선택적 쿼리를 위한 필터 표현식.

```python
# 예제
ports = client.get_ports("top", filter="direction == 'input'")
nets = client.get_nets("top", filter="width > 1")
```

### hierarchical (선택사항, 기본값=False)

쿼리에 계층 구조 정보 포함.

```python
# 계층 구조 경로와 함께 평면 리스트 가져오기
modules = client.get_modules(hierarchical=True)
for mod in modules:
    if mod['path']:
        print(f"경로: {mod['path']}")
```

## 반환 값 패턴

### 성공/상태 확인

```python
# 'success' 필드가 있는 뮤테이션의 경우
result = client.add_port("top", "new_port", "input", 8)
if result['success']:
    print("작업 성공")
else:
    print(f"오류: {result['message']}")

# 'status' 필드가 있는 뮤테이션의 경우
result = client.read_verilog("/path/to/file.v")
if result['status'] == 'success':
    print("파일 로드 성공")
```

### 리스트 처리

```python
# 모든 쿼리 명령어는 리스트를 반환합니다
modules = client.get_modules()  # list[ModuleInfo]
for mod in modules:
    print(mod['name'])

# 중첩 데이터 접근
for mod in modules:
    for port in mod['ports']:  # list[PortInfo]
        print(f"  {port['name']}")
```

## 다음 단계

- 📖 [쿼리 레퍼런스](queries.md) - 상세한 쿼리 명령어
- ✏️ [뮤테이션 레퍼런스](mutations.md) - 상세한 뮤테이션 명령어
- 📊 [타입 레퍼런스](types.md) - 데이터 타입 사양
- 💡 [예제](../examples/basic-operations.md) - 사용 예제
