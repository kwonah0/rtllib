# 쿼리 명령어 레퍼런스

RTL Library 서버에서 설계 정보를 조회하는 모든 쿼리 명령어입니다.

---

## health_check

서버 상태 및 상태를 확인합니다.

**매개변수:** 없음

**반환:** `HealthCheckResult`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| status | str | 서버 상태: "ok" 또는 오류 메시지 |
| backend_type | str | 백엔드 타입: "dummy" 또는 "real" |

**예제 (Python):**

```python
from rtllib import Client

client = Client()
result = client.health_check()
print(result)
# {'status': 'ok', 'backend_type': 'dummy'}
```

**예제 (GraphQL):**

```graphql
query {
  health_check {
    status
    backend_type
  }
}
```

**관련:** 없음

---

## get_modules

중첩된 포트/인스턴스/넷 정보와 함께 설계의 모든 모듈을 가져옵니다.

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| filter | str | ❌ | None | 필터 표현식 (백엔드별) |
| hierarchical | bool | ❌ | False | 경로와 함께 계층 구조 인스턴스를 평면 리스트로 포함 |

**반환:** `list[ModuleInfo]`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| name | str | 모듈 이름 |
| file | str | 소스 파일 경로 |
| path | str 또는 None | 계층 구조 경로 (hierarchical=True인 경우) |
| ports | list[PortInfo] | 포트 정보 리스트 |
| instances | list[InstanceInfo] | 인스턴스 정보 리스트 |
| nets | list[NetInfo] | 넷/와이어 정보 리스트 |

**예제 (Python):**

```python
# 모든 모듈 가져오기
modules = client.get_modules()
for mod in modules:
    print(f"{mod['name']}: {len(mod['ports'])} 포트, {len(mod['instances'])} 인스턴스")

# 필터 사용
top_modules = client.get_modules(filter="name == 'top'")

# 계층 구조 뷰 사용
all_instances = client.get_modules(hierarchical=True)
```

**예제 (GraphQL):**

```graphql
query GetModules($filter: String, $hierarchical: Boolean!) {
  modules(filter: $filter, hierarchical: $hierarchical) {
    name
    file
    path
    ports {
      name
      direction
      width
    }
    instances {
      name
      module
      parent
    }
    nets {
      name
      width
      net_type
    }
  }
}
```

**관련:** [get_ports](#get_ports), [get_instances](#get_instances), [get_nets](#get_nets)

---

## get_ports

특정 모듈의 모든 포트를 가져옵니다.

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | 모듈 이름 |
| filter | str | ❌ | None | 필터 표현식 (예: "direction == 'input'") |
| hierarchical | bool | ❌ | False | 하위 인스턴스의 포트 포함 |

**반환:** `list[PortInfo]`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| name | str | 포트 이름 |
| direction | str | 포트 방향: "input", "output", 또는 "inout" |
| width | int | 비트 폭 |
| path | str 또는 None | 계층 구조 경로 (hierarchical=True인 경우) |

**예제 (Python):**

```python
# 모든 포트 가져오기
ports = client.get_ports("top_module")

# 입력 포트만 가져오기
input_ports = client.get_ports("top_module", filter="direction == 'input'")

# 계층 구조와 함께 포트 가져오기
all_ports = client.get_ports("top_module", hierarchical=True)

# 포트 표시
for port in ports:
    print(f"{port['name']}: {port['direction']} [{port['width']} bits]")
```

**예제 (GraphQL):**

```graphql
query GetPorts($module: String!, $filter: String, $hierarchical: Boolean!) {
  ports(module: $module, filter: $filter, hierarchical: $hierarchical) {
    name
    direction
    width
    path
  }
}
```

**관련:** [get_modules](#get_modules), [ModuleInfo](types.md#moduleinfo)

---

## get_instances

특정 모듈 내의 모든 인스턴스를 가져옵니다.

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | 모듈 이름 |
| filter | str | ❌ | None | 필터 표현식 (예: "module == 'cpu'") |
| hierarchical | bool | ❌ | False | 재귀적으로 하위 인스턴스 포함 |

**반환:** `list[InstanceInfo]`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| name | str | 인스턴스 이름 |
| module | str | 인스턴스화된 모듈 이름 |
| parent | str | 부모 모듈 이름 |
| path | str 또는 None | 계층 구조 경로 (hierarchical=True인 경우) |

**예제 (Python):**

```python
# 모든 인스턴스 가져오기
instances = client.get_instances("top_module")

# 특정 모듈 타입 필터링
cpu_instances = client.get_instances("top_module", filter="module == 'cpu'")

# 계층 구조와 함께
all_instances = client.get_instances("top_module", hierarchical=True)

# 인스턴스 표시
for inst in instances:
    print(f"{inst['name']}: {inst['module']} (부모: {inst['parent']})")
```

**예제 (GraphQL):**

```graphql
query GetInstances($module: String!, $filter: String, $hierarchical: Boolean!) {
  instances(module: $module, filter: $filter, hierarchical: $hierarchical) {
    name
    module
    parent
    path
  }
}
```

**관련:** [get_modules](#get_modules), [ModuleInfo](types.md#moduleinfo)

---

## get_nets

특정 모듈 내의 모든 넷/와이어를 가져옵니다.

**매개변수:**

| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | 모듈 이름 |
| filter | str | ❌ | None | 필터 표현식 (예: "width > 1") |
| hierarchical | bool | ❌ | False | 하위 인스턴스의 넷 포함 |

**반환:** `list[NetInfo]`

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| name | str | 넷 이름 |
| width | int | 비트 폭 |
| net_type | str | 넷 타입: "wire", "reg", 등 |
| path | str 또는 None | 계층 구조 경로 (hierarchical=True인 경우) |

**예제 (Python):**

```python
# 모든 넷 가져오기
nets = client.get_nets("top_module")

# 버스만 가져오기 (width > 1)
buses = client.get_nets("top_module", filter="width > 1")

# 계층 구조와 함께
all_nets = client.get_nets("top_module", hierarchical=True)

# 넷 표시
for net in nets:
    print(f"{net['name']}: {net['net_type']} [{net['width']} bits]")
```

**예제 (GraphQL):**

```graphql
query GetNets($module: String!, $filter: String, $hierarchical: Boolean!) {
  nets(module: $module, filter: $filter, hierarchical: $hierarchical) {
    name
    width
    net_type
    path
  }
}
```

**관련:** [get_modules](#get_modules), [ModuleInfo](types.md#moduleinfo)

---

## 일반적인 패턴

### 중첩 데이터 접근

```python
# get_modules는 완전한 중첩 정보를 반환합니다
modules = client.get_modules()

for mod in modules:
    # 포트 접근
    for port in mod['ports']:
        print(f"  포트: {port['name']}")

    # 인스턴스 접근
    for inst in mod['instances']:
        print(f"  인스턴스: {inst['name']} ({inst['module']})")

    # 넷 접근
    for net in mod['nets']:
        print(f"  넷: {net['name']}")
```

### 필터 사용

```python
# 입력 포트만
inputs = client.get_ports("cpu", filter="direction == 'input'")

# 와이드 포트 (> 1비트)
wide = client.get_ports("cpu", filter="width > 1")

# 와이어만
wires = client.get_nets("cpu", filter="net_type == 'wire'")

# 특정 모듈 인스턴스
alu_insts = client.get_instances("cpu", filter="module == 'alu'")
```

### 계층 구조 쿼리

```python
# 경로와 함께 평면화된 모든 인스턴스 가져오기
all_modules = client.get_modules(hierarchical=True)

for mod in all_modules:
    if mod['path']:
        # 이것은 계층 구조 인스턴스입니다
        print(f"인스턴스: {mod['path']}.{mod['name']}")
    else:
        # 이것은 최상위 모듈입니다
        print(f"최상위: {mod['name']}")
```

### 일괄 쿼리

```python
# 모든 모듈의 모든 정보 가져오기
modules = client.get_modules()

for mod in modules:
    module_name = mod['name']

    # 중첩 데이터는 이미 사용 가능합니다
    print(f"\n모듈: {module_name}")
    print(f"  포트: {len(mod['ports'])}")
    print(f"  인스턴스: {len(mod['instances'])}")
    print(f"  넷: {len(mod['nets'])}")

    # 세부 정보 표시
    for port in mod['ports']:
        print(f"    - {port['name']}: {port['direction']}")
```

### 오류 처리

```python
try:
    ports = client.get_ports("nonexistent_module")
except Exception as e:
    print(f"오류: {e}")

# 빈 결과 확인
ports = client.get_ports("module")
if not ports:
    print("포트를 찾을 수 없습니다")
```

## 성능 팁

### get_modules 사용 (권장)

중첩 데이터가 필요한 경우 `get_modules`를 사용하세요:

```python
# 좋음: 한 번의 호출
modules = client.get_modules()
for mod in modules:
    # 포트, 인스턴스, 넷은 이미 사용 가능합니다
    print(f"{mod['name']}: {len(mod['ports'])} 포트")
```

### 개별 쿼리 피하기

가능하면 여러 개별 쿼리를 피하세요:

```python
# 나쁨: N+1 쿼리
module_names = ["cpu", "memory", "io"]
for name in module_names:
    ports = client.get_ports(name)  # 각각에 대해 네트워크 호출
    # ...

# 좋음: 한 번의 쿼리
modules = client.get_modules()
modules_map = {mod['name']: mod for mod in modules}
for name in module_names:
    ports = modules_map[name]['ports']  # 로컬 데이터
    # ...
```

## 다음 단계

- ✏️ [뮤테이션 레퍼런스](mutations.md) - 설계 수정 명령어
- 📊 [타입 레퍼런스](types.md) - 모든 데이터 타입
- 💡 [예제](../examples/basic-operations.md) - 더 많은 사용 예제
