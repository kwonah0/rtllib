# 데이터 타입 레퍼런스

쿼리 및 뮤테이션 명령어가 반환하는 모든 데이터 타입입니다.

---

## HealthCheckResult

서버 상태 확인 결과.

```python
{
    "status": str,        # "ok" 또는 오류 메시지
    "backend_type": str   # "dummy" 또는 "real"
}
```

**예제:**
```python
{'status': 'ok', 'backend_type': 'dummy'}
```

**사용처:** [health_check](queries.md#health_check)

---

## ModuleInfo

중첩된 포트, 인스턴스, 넷을 포함한 모듈의 완전한 정보.

```python
{
    "name": str,                      # 모듈 이름
    "file": str,                      # 소스 파일 경로
    "path": Optional[str],            # 계층 구조 경로 (계층 구조 쿼리인 경우)
    "ports": list[PortInfo],          # 포트 리스트
    "instances": list[InstanceInfo],  # 인스턴스 리스트
    "nets": list[NetInfo]             # 넷/와이어 리스트
}
```

**예제:**
```python
{
    'name': 'top_module',
    'file': '/path/to/top.v',
    'path': None,
    'ports': [
        {'name': 'clk', 'direction': 'input', 'width': 1, 'path': None},
        {'name': 'data_out', 'direction': 'output', 'width': 32, 'path': None}
    ],
    'instances': [
        {'name': 'cpu_inst', 'module': 'cpu', 'parent': 'top_module', 'path': None}
    ],
    'nets': [
        {'name': 'internal_bus', 'width': 32, 'net_type': 'wire', 'path': None}
    ]
}
```

**사용처:** [get_modules](queries.md#get_modules)

---

## PortInfo

모듈 포트에 대한 정보.

```python
{
    "name": str,            # 포트 이름
    "direction": str,       # "input", "output", 또는 "inout"
    "width": int,           # 비트 폭
    "path": Optional[str]   # 계층 구조 경로 (계층 구조 쿼리인 경우)
}
```

**예제:**
```python
{'name': 'data_in', 'direction': 'input', 'width': 32, 'path': None}
```

**사용처:** [get_ports](queries.md#get_ports), [ModuleInfo](#moduleinfo)

---

## InstanceInfo

모듈 인스턴스에 대한 정보.

```python
{
    "name": str,            # 인스턴스 이름
    "module": str,          # 인스턴스화되는 모듈 타입
    "parent": str,          # 부모 모듈 이름
    "path": Optional[str]   # 계층 구조 경로 (계층 구조 쿼리인 경우)
}
```

**예제:**
```python
{'name': 'cpu_inst', 'module': 'cpu', 'parent': 'top_module', 'path': None}
```

**사용처:** [get_instances](queries.md#get_instances), [ModuleInfo](#moduleinfo)

---

## NetInfo

넷/와이어에 대한 정보.

```python
{
    "name": str,            # 넷 이름
    "width": int,           # 비트 폭
    "net_type": str,        # "wire", "reg", 등
    "path": Optional[str]   # 계층 구조 경로 (계층 구조 쿼리인 경우)
}
```

**예제:**
```python
{'name': 'data_bus', 'width': 32, 'net_type': 'wire', 'path': None}
```

**사용처:** [get_nets](queries.md#get_nets), [ModuleInfo](#moduleinfo)

---

## ReadVerilogResult

Verilog 파일 읽기 결과.

```python
{
    "status": str,         # "success" 또는 "error"
    "message": str,        # 상태 메시지
    "modules_found": int   # 발견된 모듈 수
}
```

**예제:**
```python
{'status': 'success', 'message': 'File loaded successfully', 'modules_found': 3}
```

**사용처:** [read_verilog](mutations.md#read_verilog)

---

## ReadFilelistResult

파일리스트 읽기 결과.

```python
{
    "status": str,         # "success" 또는 "error"
    "message": str,        # 상태 메시지
    "files_read": int,     # 읽은 파일 수
    "modules_found": int   # 발견된 모듈 수
}
```

**예제:**
```python
{
    'status': 'success',
    'message': 'Filelist loaded successfully',
    'files_read': 5,
    'modules_found': 12
}
```

**사용처:** [read_verilog_filelist](mutations.md#read_verilog_filelist)

---

## AddPortResult

포트 추가 작업 결과.

```python
{
    "success": bool,    # 작업 성공 여부
    "message": str,     # 상태 메시지
    "port_name": str    # 추가된 포트 이름
}
```

**예제:**
```python
{'success': True, 'message': 'Port added successfully', 'port_name': 'debug_out'}
```

**사용처:** [add_port](mutations.md#add_port)

---

## AddNetResult

넷 추가 작업 결과.

```python
{
    "success": bool,   # 작업 성공 여부
    "message": str,    # 상태 메시지
    "net_name": str    # 추가된 넷 이름
}
```

**예제:**
```python
{'success': True, 'message': 'Net added successfully', 'net_name': 'debug_bus'}
```

**사용처:** [add_net](mutations.md#add_net)

---

## 타입 관계

```
ModuleInfo
├── ports: list[PortInfo]
├── instances: list[InstanceInfo]
└── nets: list[NetInfo]

get_modules() -> list[ModuleInfo]
get_ports() -> list[PortInfo]
get_instances() -> list[InstanceInfo]
get_nets() -> list[NetInfo]
```

## 일반적인 패턴

### 중첩 객체 접근

```python
# get_modules는 중첩 객체를 반환합니다
modules: list[ModuleInfo] = client.get_modules()

for mod in modules:
    # 모듈 정보
    print(f"모듈: {mod['name']}")
    print(f"파일: {mod['file']}")

    # 중첩된 포트
    for port in mod['ports']:  # list[PortInfo]
        print(f"  포트: {port['name']} ({port['direction']})")

    # 중첩된 인스턴스
    for inst in mod['instances']:  # list[InstanceInfo]
        print(f"  인스턴스: {inst['name']} ({inst['module']})")

    # 중첩된 넷
    for net in mod['nets']:  # list[NetInfo]
        print(f"  넷: {net['name']} ({net['net_type']})")
```

### 타입 힌트 사용

```python
from rtllib import Client
from rtllib.types import ModuleInfo, PortInfo, InstanceInfo, NetInfo

client = Client()

# 타입 힌트와 함께
modules: list[ModuleInfo] = client.get_modules()
ports: list[PortInfo] = client.get_ports("top")
instances: list[InstanceInfo] = client.get_instances("top")
nets: list[NetInfo] = client.get_nets("top")

# TypedDict는 IDE 자동완성을 제공합니다
for mod in modules:
    name: str = mod['name']           # IDE가 'name'을 제안합니다
    file: str = mod['file']           # IDE가 'file'을 제안합니다
    ports: list[PortInfo] = mod['ports']  # IDE가 'ports'를 제안합니다
```

### 성공 확인

```python
# 'status' 필드가 있는 타입 (ReadVerilogResult, ReadFilelistResult)
result = client.read_verilog("/path/to/file.v")
if result['status'] == 'success':
    print(f"성공: {result['modules_found']}개 모듈 발견")
else:
    print(f"실패: {result['message']}")

# 'success' 필드가 있는 타입 (AddPortResult, AddNetResult)
result = client.add_port("module", "port", "input", 8)
if result['success']:
    print(f"성공: {result['port_name']} 추가됨")
else:
    print(f"실패: {result['message']}")
```

### 계층 구조 경로

```python
# hierarchical=False인 경우 (기본값)
modules = client.get_modules(hierarchical=False)
for mod in modules:
    assert mod['path'] is None  # 최상위 모듈만

# hierarchical=True인 경우
modules = client.get_modules(hierarchical=True)
for mod in modules:
    if mod['path'] is None:
        print(f"최상위: {mod['name']}")
    else:
        print(f"인스턴스: {mod['path']}.{mod['name']}")
```

### Optional 필드 처리

```python
modules = client.get_modules(hierarchical=True)

for mod in modules:
    # 'path'는 Optional[str]입니다
    if mod['path']:
        # 이것은 계층 구조 인스턴스입니다
        full_path = f"{mod['path']}.{mod['name']}"
    else:
        # 이것은 최상위 모듈입니다
        full_path = mod['name']

    print(f"경로: {full_path}")
```

### 데이터 변환

```python
# ModuleInfo를 간단한 딕셔너리로 변환
def module_summary(mod: ModuleInfo) -> dict:
    return {
        'name': mod['name'],
        'file': mod['file'],
        'port_count': len(mod['ports']),
        'instance_count': len(mod['instances']),
        'net_count': len(mod['nets'])
    }

modules = client.get_modules()
summaries = [module_summary(mod) for mod in modules]
```

### 리스트 필터링

```python
modules = client.get_modules()

# 포트가 있는 모듈만
with_ports = [mod for mod in modules if mod['ports']]

# 인스턴스가 있는 모듈만
with_instances = [mod for mod in modules if mod['instances']]

# 특정 이름 패턴
cpu_modules = [mod for mod in modules if 'cpu' in mod['name'].lower()]
```

## 다음 단계

- 🔍 [쿼리 레퍼런스](queries.md) - 쿼리 명령어 배우기
- ✏️ [뮤테이션 레퍼런스](mutations.md) - 뮤테이션 명령어 배우기
- 💡 [예제](../examples/basic-operations.md) - 실제 사용 예제
