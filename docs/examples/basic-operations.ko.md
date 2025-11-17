# 기본 작업 예제

rtllib의 일반적인 사용 패턴 및 예제입니다.

## 📥 예제 다운로드

모든 예제는 독립 실행 가능한 Python 파일로 제공됩니다:

- **개별 파일**: 아래 예제 파일을 클릭하여 다운로드
- **전체 예제 (ZIP)**: [examples.zip 다운로드](https://github.com/kwonah0/rtllib/archive/refs/heads/main.zip) 후 `examples/` 폴더 압축 해제
- **Git Clone**: `git clone https://github.com/kwonah0/rtllib.git` 후 `examples/` 폴더로 이동

| 파일 | 설명 |
|------|------|
| [example_1_load_and_query.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_1_load_and_query.py) | 설계 로드 및 쿼리 |
| [example_2_analyze_ports.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_2_analyze_ports.py) | 포트 인터페이스 분석 |
| [example_3_hierarchy.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_3_hierarchy.py) | 계층 구조 분석 |
| [example_4_filters.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_4_filters.py) | 필터 사용 |
| [example_5_multiple_files.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_5_multiple_files.py) | 여러 파일 |
| [example_6_design_modification.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_6_design_modification.py) | 설계 수정 |
| [example_7_error_handling.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_7_error_handling.py) | 오류 처리 |
| [example_8_external_server.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_8_external_server.py) | 외부 서버 |
| [example_9_generate_report.py](https://github.com/kwonah0/rtllib/blob/main/examples/example_9_generate_report.py) | 리포트 생성 |

자세한 내용은 [examples README](https://github.com/kwonah0/rtllib/blob/main/examples/README.md)를 참조하세요.

## 예제 1: 설계 로드 및 쿼리

```python
from rtllib import Client

with Client() as client:
    # Verilog 파일 로드
    result = client.read_verilog("/path/to/cpu.v")
    print(f"{result['modules_found']}개 모듈 로드됨")

    # 설계 처리
    client.compile()
    client.elaborate()

    # 모든 모듈 가져오기
    modules = client.get_modules()
    for mod in modules:
        print(f"\n모듈: {mod['name']}")
        print(f"  파일: {mod['file']}")
        print(f"  포트: {len(mod['ports'])}")
        print(f"  인스턴스: {len(mod['instances'])}")
        print(f"  넷: {len(mod['nets'])}")
```

## 예제 2: 포트 인터페이스 분석

```python
from rtllib import Client

def analyze_module_interface(module_name, verilog_file):
    """모듈 포트 인터페이스를 분석하고 출력합니다."""
    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        ports = client.get_ports(module_name)

        # 방향별로 포트 그룹화
        inputs = [p for p in ports if p['direction'] == 'input']
        outputs = [p for p in ports if p['direction'] == 'output']
        inouts = [p for p in ports if p['direction'] == 'inout']

        print(f"모듈: {module_name}")
        print(f"\n입력 ({len(inputs)}):")
        for port in inputs:
            print(f"  {port['name']:<20} [{port['width']:>3} bits]")

        print(f"\n출력 ({len(outputs)}):")
        for port in outputs:
            print(f"  {port['name']:<20} [{port['width']:>3} bits]")

        if inouts:
            print(f"\nInout ({len(inouts)}):")
            for port in inouts:
                print(f"  {port['name']:<20} [{port['width']:>3} bits]")

# 사용
analyze_module_interface("cpu", "/path/to/cpu.v")
```

## 예제 3: 계층 구조 분석

```python
from rtllib import Client

def analyze_hierarchy(verilog_file):
    """설계 계층 구조를 분석합니다."""
    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        # 계층 구조 뷰 가져오기
        modules = client.get_modules(hierarchical=True)

        # 계층 구조 트리 구축
        for mod in modules:
            path = mod.get('path')
            if path:
                level = path.count('.')
                indent = "  " * level
                print(f"{indent}{mod['name']} ({len(mod['instances'])}개 하위 인스턴스)")
            else:
                print(f"Top: {mod['name']}")

# 사용
analyze_hierarchy("/path/to/design.v")
```

## 예제 4: 필터 사용

```python
from rtllib import Client

with Client() as client:
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # 와이드 포트만 가져오기 (> 1 비트)
    wide_ports = client.get_ports("cpu", filter="width > 1")
    print(f"와이드 포트: {len(wide_ports)}")

    # 입력 포트만 가져오기
    inputs = client.get_ports("cpu", filter="direction == 'input'")
    print(f"입력 포트: {len(inputs)}")

    # 와이어 넷만 가져오기
    wires = client.get_nets("cpu", filter="net_type == 'wire'")
    print(f"와이어 넷: {len(wires)}")
```

## 예제 5: 여러 파일

```python
from rtllib import Client

# 파일리스트 생성
with open("design.f", "w") as f:
    f.write("# Top-level\n")
    f.write("/path/to/top.v\n")
    f.write("\n")
    f.write("# Subsystems\n")
    f.write("/path/to/cpu.v\n")
    f.write("/path/to/memory.v\n")
    f.write("/path/to/io.v\n")

# 파일리스트에서 로드
with Client() as client:
    result = client.read_verilog_filelist("design.f")

    if result['status'] == 'success':
        print(f"{result['files_read']}개 파일 성공적으로 읽음")
        print(f"{result['modules_found']}개 모듈 발견")

        client.compile()
        client.elaborate()

        modules = client.get_modules()
        for mod in modules:
            print(f"  - {mod['name']} ({len(mod['instances'])}개 인스턴스)")
    else:
        print(f"오류: {result['message']}")
```

## 예제 6: 설계 수정

```python
from rtllib import Client

with Client() as client:
    # 설계 로드
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    # 현재 포트 가져오기
    ports_before = client.get_ports("cpu")
    print(f"수정 전 포트: {len(ports_before)}")

    # 디버그 포트 추가
    result = client.add_port(
        module="cpu",
        port_name="debug_out",
        direction="output",
        width=32
    )

    if result['success']:
        print(f"포트 추가됨: {result['port_name']}")

        # 디버그 버스 넷 추가
        client.add_net(
            module="cpu",
            net_name="debug_bus",
            width=32,
            net_type="wire"
        )

        # 수정 확인
        ports_after = client.get_ports("cpu")
        nets = client.get_nets("cpu")

        print(f"수정 후 포트: {len(ports_after)} (+{len(ports_after) - len(ports_before)})")
        print(f"넷: {len(nets)}")
    else:
        print(f"오류: {result['message']}")
```

## 예제 7: 오류 처리

```python
from rtllib import Client

def safe_analyze(verilog_file):
    """적절한 오류 처리로 설계를 분석합니다."""
    try:
        with Client() as client:
            # 파일 읽기 시도
            result = client.read_verilog(verilog_file)
            if result['status'] != 'success':
                print(f"파일 읽기 실패: {result}")
                return None

            # 컴파일 시도
            try:
                client.compile()
            except Exception as e:
                print(f"컴파일 오류: {e}")
                return None

            # 엘라보레이트 시도
            try:
                client.elaborate()
            except Exception as e:
                print(f"엘라보레이트 오류: {e}")
                return None

            # 설계 쿼리
            modules = client.get_modules()
            return modules

    except Exception as e:
        print(f"클라이언트 오류: {e}")
        return None

# 사용
modules = safe_analyze("/path/to/design.v")
if modules:
    print(f"{len(modules)}개 모듈 성공적으로 분석됨")
else:
    print("분석 실패")
```

## 예제 8: 외부 서버

```python
from rtllib import Client
import subprocess
import time

# 외부에서 서버 시작
server_process = subprocess.Popen(
    ["rtllib-server", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# 서버 시작 대기
time.sleep(2)

try:
    # 외부 서버에 연결
    client = Client(host="127.0.0.1", port=8000, auto_start=False)

    # 클라이언트 사용
    health = client.health_check()
    print(f"서버 상태: {health['status']}")

    # ... 나머지 작업 ...

finally:
    # 정리
    client.close()
    server_process.terminate()
    server_process.wait()
```

## 예제 9: 리포트 생성

```python
from rtllib import Client
import json

def generate_design_report(verilog_file, output_file):
    """설계의 JSON 리포트를 생성합니다."""
    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        modules = client.get_modules()

        report = {
            "file": verilog_file,
            "modules": []
        }

        for mod in modules:
            module_data = {
                "name": mod['name'],
                "file": mod['file'],
                "statistics": {
                    "ports": len(mod['ports']),
                    "instances": len(mod['instances']),
                    "nets": len(mod['nets'])
                },
                "ports": [
                    {
                        "name": p['name'],
                        "direction": p['direction'],
                        "width": p['width']
                    }
                    for p in mod['ports']
                ]
            }
            report["modules"].append(module_data)

        # 리포트 작성
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"리포트가 {output_file}에 작성됨")

# 사용
generate_design_report("/path/to/design.v", "design_report.json")
```

## 다음 단계

- 📖 [쿼리 레퍼런스](../commands/queries.md) - 모든 쿼리 명령어
- ✏️ [뮤테이션 레퍼런스](../commands/mutations.md) - 모든 뮤테이션 명령어
- 📊 [타입 레퍼런스](../commands/types.md) - 데이터 타입
