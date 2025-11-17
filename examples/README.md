# rtllib Examples

Practical examples demonstrating rtllib usage patterns.

## 📋 Available Examples

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [example_1_load_and_query.py](example_1_load_and_query.py) | Load and query design | Basic workflow, module information |
| [example_2_analyze_ports.py](example_2_analyze_ports.py) | Analyze port interfaces | Port grouping, formatting |
| [example_3_hierarchy.py](example_3_hierarchy.py) | Hierarchy analysis | Hierarchical queries, tree structure |
| [example_4_filters.py](example_4_filters.py) | Filter usage | Query filters, selective retrieval |
| [example_5_multiple_files.py](example_5_multiple_files.py) | Multiple files | Filelist, multi-file designs |
| [example_6_design_modification.py](example_6_design_modification.py) | Design modification | Session-based changes, add ports/nets |
| [example_7_error_handling.py](example_7_error_handling.py) | Error handling | Safe patterns, exception handling |
| [example_8_external_server.py](example_8_external_server.py) | External server | Server management, external connection |
| [example_9_generate_report.py](example_9_generate_report.py) | Generate report | JSON export, design statistics |

## 🚀 Quick Start

### Prerequisites

```bash
# Install rtllib
pip install rtllib
```

### Running Examples

Each example is a standalone Python script:

```bash
# Run an example
python example_1_load_and_query.py
```

**Note:** Most examples require you to modify the Verilog file paths before running.

## 📝 Modifying Examples

Before running, update the file paths in each example:

```python
# Change this line:
verilog_file = "/path/to/cpu.v"

# To your actual file:
verilog_file = "/home/user/designs/my_cpu.v"
```

## 💡 Usage Patterns

### Basic Pattern

```python
from rtllib import Client

with Client() as client:
    # 1. Load design
    client.read_verilog("/path/to/design.v")

    # 2. Process
    client.compile()
    client.elaborate()

    # 3. Query
    modules = client.get_modules()
```

### With Error Handling

```python
try:
    with Client() as client:
        result = client.read_verilog(file_path)
        if result['status'] != 'success':
            print(f"Error: {result['message']}")
            return

        client.compile()
        client.elaborate()
        modules = client.get_modules()
except Exception as e:
    print(f"Error: {e}")
```

## 📚 Documentation

- [Command Reference](https://kwonah0.github.io/rtllib/)
- [API Documentation](../docs/)

## 🔧 Requirements

- Python 3.10+
- rtllib

## 📦 Example Categories

### Beginner
- Example 1: Load and Query
- Example 4: Filters
- Example 7: Error Handling

### Intermediate
- Example 2: Analyze Ports
- Example 3: Hierarchy
- Example 5: Multiple Files

### Advanced
- Example 6: Design Modification
- Example 8: External Server
- Example 9: Generate Report

---

# rtllib 예제

rtllib 사용 패턴을 보여주는 실용적인 예제 모음입니다.

## 📋 사용 가능한 예제

| 예제 | 설명 | 핵심 개념 |
|------|------|-----------|
| [example_1_load_and_query.py](example_1_load_and_query.py) | 설계 로드 및 쿼리 | 기본 워크플로우, 모듈 정보 |
| [example_2_analyze_ports.py](example_2_analyze_ports.py) | 포트 인터페이스 분석 | 포트 그룹화, 포맷팅 |
| [example_3_hierarchy.py](example_3_hierarchy.py) | 계층 구조 분석 | 계층 구조 쿼리, 트리 구조 |
| [example_4_filters.py](example_4_filters.py) | 필터 사용 | 쿼리 필터, 선택적 조회 |
| [example_5_multiple_files.py](example_5_multiple_files.py) | 여러 파일 | 파일리스트, 멀티파일 설계 |
| [example_6_design_modification.py](example_6_design_modification.py) | 설계 수정 | 세션 기반 변경, 포트/넷 추가 |
| [example_7_error_handling.py](example_7_error_handling.py) | 오류 처리 | 안전한 패턴, 예외 처리 |
| [example_8_external_server.py](example_8_external_server.py) | 외부 서버 | 서버 관리, 외부 연결 |
| [example_9_generate_report.py](example_9_generate_report.py) | 리포트 생성 | JSON 내보내기, 설계 통계 |

## 🚀 빠른 시작

### 사전 요구사항

```bash
# rtllib 설치
pip install rtllib
```

### 예제 실행

각 예제는 독립 실행 가능한 Python 스크립트입니다:

```bash
# 예제 실행
python example_1_load_and_query.py
```

**참고:** 대부분의 예제는 실행 전에 Verilog 파일 경로를 수정해야 합니다.

## 📝 예제 수정

실행 전에 각 예제의 파일 경로를 업데이트하세요:

```python
# 이 줄을 변경:
verilog_file = "/path/to/cpu.v"

# 실제 파일로:
verilog_file = "/home/user/designs/my_cpu.v"
```

## 💡 사용 패턴

### 기본 패턴

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
```

### 오류 처리 포함

```python
try:
    with Client() as client:
        result = client.read_verilog(file_path)
        if result['status'] != 'success':
            print(f"오류: {result['message']}")
            return

        client.compile()
        client.elaborate()
        modules = client.get_modules()
except Exception as e:
    print(f"오류: {e}")
```

## 📚 문서

- [명령어 레퍼런스](https://kwonah0.github.io/rtllib/)
- [API 문서](../docs/)

## 🔧 요구사항

- Python 3.10+
- rtllib

## 📦 예제 카테고리

### 초급
- Example 1: 로드 및 쿼리
- Example 4: 필터
- Example 7: 오류 처리

### 중급
- Example 2: 포트 분석
- Example 3: 계층 구조
- Example 5: 여러 파일

### 고급
- Example 6: 설계 수정
- Example 8: 외부 서버
- Example 9: 리포트 생성
