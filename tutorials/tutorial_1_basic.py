"""
Tutorial 1: 전체 아키텍처 이해
================================

이 튜토리얼은 rtllib의 기본 구조를 이해하는 것을 목표로 합니다.

학습 목표:
- Client가 ServerManager를 통해 서버를 자동으로 시작하는 과정 이해
- GraphQL을 통한 클라이언트-서버 통신 이해
- 데이터 흐름 추적

데이터 흐름:
Client → HTTP Request → FastAPI → GraphQL Schema → Backend Protocol → DummyBackend
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib import Client
import json


def main():
    print("=" * 60)
    print("Tutorial 1: 전체 아키텍처 이해")
    print("=" * 60)

    # Step 1: 클라이언트 생성 및 서버 자동 시작
    print("\n[Step 1] 클라이언트 생성 시 자동으로 서버 시작")
    print("-" * 40)

    # Client 생성 시 내부적으로 일어나는 일:
    # 1. ServerManager 인스턴스 생성
    # 2. 빈 포트 자동 찾기 (기본값: 5000부터 시작)
    # 3. subprocess.Popen()으로 서버 프로세스 시작
    # 4. 헬스체크로 서버 준비 확인
    client = Client(auto_start=True)  # auto_start=True가 기본값

    print(f"✅ 서버가 포트 {client.port}에서 시작되었습니다.")
    print(f"   서버 호스트: {client.host}")
    print(f"   GraphQL 엔드포인트: http://{client.host}:{client.port}/graphql")

    # Step 2: GraphQL 통신 확인 (Health Check)
    print("\n[Step 2] GraphQL Query 실행 - Health Check")
    print("-" * 40)

    # health_check()는 내부적으로:
    # 1. GraphQL 쿼리 생성: query { healthCheck { status backendType } }
    # 2. HTTP POST 요청을 /graphql로 전송
    # 3. FastAPI가 요청 수신 → Strawberry가 GraphQL 파싱
    # 4. schema.py의 Query.health_check() 메서드 실행
    # 5. 응답 반환
    result = client.health_check()

    print(f"서버 응답: {json.dumps(result, indent=2)}")
    print(f"✅ 서버 상태: {result['status']}")
    print(f"✅ 백엔드 타입: {result['backend_type']}")

    # Step 3: GraphQL Mutation 실행
    print("\n[Step 3] GraphQL Mutation 실행 - Read Verilog")
    print("-" * 40)

    # read_verilog()는 Mutation을 실행:
    # mutation { readVerilog(path: "/test.v") { status file modulesFound } }
    result = client.read_verilog("/test.v")

    print(f"Verilog 읽기 결과: {json.dumps(result, indent=2)}")
    print(f"✅ 상태: {result['status']}")
    print(f"✅ 파일: {result['file']}")
    print(f"✅ 발견된 모듈 수: {result['modules_found']}")

    # Step 4: Backend Protocol 이해
    print("\n[Step 4] Backend Protocol 동작 이해")
    print("-" * 40)

    # compile() 실행 시 흐름:
    # 1. Client.compile() → GraphQL Mutation
    # 2. schema.py: Mutation.compile()
    # 3. backend/__init__.py: get_backend_instance() → 싱글톤 패턴
    # 4. backend/dummy.py: DummyBackend.compile() 실행
    # 5. 결과 반환
    result = client.compile()
    print(f"컴파일 결과: {result}")

    # Step 5: 서버 종료
    print("\n[Step 5] 서버 종료")
    print("-" * 40)

    # close() 실행 시:
    # 1. GraphQL 클라이언트 정리
    # 2. ServerManager.stop() 호출
    # 3. subprocess.terminate() → 서버 프로세스 종료
    # 4. 임시 로그 파일 정리
    client.close()
    print("✅ 서버가 정상적으로 종료되었습니다.")

    print("\n" + "=" * 60)
    print("Tutorial 1 완료!")
    print("=" * 60)
    print("""
핵심 포인트:
1. Client는 ServerManager를 통해 자동으로 서버를 관리
2. 모든 통신은 GraphQL over HTTP로 진행
3. Backend Protocol을 통해 다양한 백엔드 구현 가능
4. DummyBackend는 테스트/개발용 구현체
    """)


if __name__ == "__main__":
    main()