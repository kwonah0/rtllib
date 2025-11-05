"""
Tutorial 4: GraphQL 직접 호출
==============================

이 튜토리얼은 GraphQL을 직접 사용하여 서버와 통신하는 방법을 학습합니다.

학습 목표:
- GraphQL Query, Mutation, Subscription 이해
- gql 라이브러리 사용법 이해
- Strawberry GraphQL 스키마 구조 이해
- 에러 처리 및 타입 안전성 이해

GraphQL 기본 개념:
- Query: 데이터 읽기 (GET)
- Mutation: 데이터 변경 (POST/PUT/DELETE)
- Subscription: 실시간 데이터 스트림 (WebSocket)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gql import gql, Client as GQLClient
from gql.transport.httpx import HTTPXTransport
from gql.transport.websockets import WebsocketsTransport
import asyncio
import json


def demonstrate_query(url: str):
    """GraphQL Query 예제"""
    print("\n[GraphQL Query 예제]")
    print("-" * 40)

    # HTTP transport 생성
    transport = HTTPXTransport(url=url)
    client = GQLClient(transport=transport, fetch_schema_from_transport=False)

    # 1. Simple Query - Health Check
    print("\n1. Simple Query:")
    query = gql("""
        query {
            healthCheck {
                status
                backendType
            }
        }
    """)

    result = client.execute(query)
    print(f"Response: {json.dumps(result, indent=2)}")

    # 2. Query with nested fields - Get Modules
    print("\n2. Query with nested fields:")
    query = gql("""
        query {
            getModules {
                name
                file
                ports
                instances
            }
        }
    """)

    result = client.execute(query)
    print(f"Modules: {json.dumps(result, indent=2)}")

    # 3. Query with arguments - Get Ports
    print("\n3. Query with arguments:")
    query = gql("""
        query GetPorts($moduleName: String!) {
            getPorts(module: $moduleName) {
                name
                direction
                width
            }
        }
    """)

    # Variables 사용
    variables = {"moduleName": "top_module"}
    result = client.execute(query, variable_values=variables)
    print(f"Ports of top_module: {json.dumps(result, indent=2)}")


def demonstrate_mutation(url: str):
    """GraphQL Mutation 예제"""
    print("\n[GraphQL Mutation 예제]")
    print("-" * 40)

    transport = HTTPXTransport(url=url)
    client = GQLClient(transport=transport, fetch_schema_from_transport=False)

    # 1. Mutation - Read Verilog
    print("\n1. Mutation - Read Verilog:")
    mutation = gql("""
        mutation ReadVerilogFile($path: String!) {
            readVerilog(path: $path) {
                status
                file
                modulesFound
            }
        }
    """)

    variables = {"path": "/test/design.v"}
    result = client.execute(mutation, variable_values=variables)
    print(f"Read result: {json.dumps(result, indent=2)}")

    # 2. Mutation - Compile
    print("\n2. Mutation - Compile:")
    mutation = gql("""
        mutation {
            compile
        }
    """)

    result = client.execute(mutation)
    print(f"Compile result: {result}")

    # 3. Mutation - Elaborate
    print("\n3. Mutation - Elaborate:")
    mutation = gql("""
        mutation {
            elaborate
        }
    """)

    result = client.execute(mutation)
    print(f"Elaborate result: {result}")


async def demonstrate_subscription(ws_url: str, http_url: str):
    """GraphQL Subscription 예제 (비동기)"""
    print("\n[GraphQL Subscription 예제]")
    print("-" * 40)

    # WebSocket transport for subscriptions
    transport = WebsocketsTransport(url=ws_url)

    async with GQLClient(
        transport=transport,
        fetch_schema_from_transport=False,
    ) as session:

        # Subscription for log streaming
        subscription = gql("""
            subscription {
                logStream {
                    level
                    message
                    timestamp
                }
            }
        """)

        print("로그 스트리밍 시작 (5초간)...")
        print("서버 작업을 실행해서 로그를 생성합니다...")

        # 별도 태스크로 서버 작업 수행 (로그 생성용)
        async def trigger_logs():
            await asyncio.sleep(1)  # Subscription 연결 대기
            # HTTP 비동기 클라이언트로 작업 수행
            from gql.transport.httpx import HTTPXAsyncTransport
            http_transport = HTTPXAsyncTransport(url=http_url)
            async with GQLClient(transport=http_transport, fetch_schema_from_transport=False) as http_session:
                # Mutation 실행해서 로그 생성
                mutation = gql("""
                    mutation {
                        readVerilog(path: "/test/design.v") {
                            status
                        }
                    }
                """)
                await http_session.execute(mutation)

                compile_mutation = gql("mutation { compile }")
                await http_session.execute(compile_mutation)

        # 로그 트리거 태스크 시작
        trigger_task = asyncio.create_task(trigger_logs())

        # 5초간 로그 수신
        count = 0
        try:
            async def collect_logs():
                nonlocal count
                async for result in session.subscribe(subscription):
                    log = result.get("logStream", {})
                    if log:
                        count += 1
                        print(f"  [{log['level']}] {log['message'][:50]}...")

            # 5초 타임아웃 적용
            await asyncio.wait_for(collect_logs(), timeout=5.0)
        except asyncio.TimeoutError:
            print(f"\n5초 경과 - 스트리밍 종료")

        await trigger_task  # 태스크 정리
        print(f"총 {count}개 로그 수신")


def demonstrate_introspection(url: str):
    """GraphQL Introspection - 스키마 탐색"""
    print("\n[GraphQL Introspection]")
    print("-" * 40)

    transport = HTTPXTransport(url=url)
    client = GQLClient(transport=transport, fetch_schema_from_transport=False)

    # 사용 가능한 Query 목록 조회
    print("\n사용 가능한 Query 목록:")
    query = gql("""
        query {
            __type(name: "Query") {
                fields {
                    name
                    description
                    args {
                        name
                        type {
                            name
                        }
                    }
                }
            }
        }
    """)

    result = client.execute(query)
    for field in result["__type"]["fields"]:
        args = ", ".join([f"{arg['name']}: {arg['type']['name'] or 'Complex'}"
                         for arg in field["args"]])
        print(f"  - {field['name']}({args})")
        if field["description"]:
            print(f"    {field['description']}")

    # 사용 가능한 Mutation 목록 조회
    print("\n사용 가능한 Mutation 목록:")
    query = gql("""
        query {
            __type(name: "Mutation") {
                fields {
                    name
                    description
                }
            }
        }
    """)

    result = client.execute(query)
    for field in result["__type"]["fields"]:
        print(f"  - {field['name']}")
        if field["description"]:
            print(f"    {field['description']}")


def demonstrate_error_handling(url: str):
    """GraphQL 에러 처리"""
    print("\n[GraphQL 에러 처리]")
    print("-" * 40)

    transport = HTTPXTransport(url=url)
    client = GQLClient(transport=transport, fetch_schema_from_transport=False)

    # 1. 잘못된 필드 요청
    print("\n1. 잘못된 필드 요청:")
    try:
        query = gql("""
            query {
                nonExistentField
            }
        """)
        result = client.execute(query)
    except Exception as e:
        print(f"❌ 에러 발생: {e}")

    # 2. 타입 불일치
    print("\n2. 타입 불일치:")
    try:
        mutation = gql("""
            mutation {
                readVerilog(path: 123)  # String이어야 하는데 숫자 전달
            }
        """)
        result = client.execute(mutation)
    except Exception as e:
        print(f"❌ 에러 발생: {e}")


def main():
    print("=" * 70)
    print("Tutorial 4: GraphQL 직접 호출")
    print("=" * 70)

    # 먼저 서버 시작
    print("\n[준비] 서버 시작")
    print("-" * 40)

    from rtllib.server_manager import ServerManager
    manager = ServerManager(host="127.0.0.1", port=None)
    manager.start()

    url = f"http://{manager.host}:{manager.port}/graphql"
    ws_url = f"ws://{manager.host}:{manager.port}/graphql"

    print(f"✅ 서버 시작됨: {url}")

    try:
        # GraphQL 데모들 실행
        demonstrate_query(url)
        demonstrate_mutation(url)
        demonstrate_introspection(url)
        demonstrate_error_handling(url)

        # Subscription은 비동기로 실행
        print("\n비동기 Subscription 테스트 시작...")
        asyncio.run(demonstrate_subscription(ws_url, url))

    finally:
        # 서버 종료
        manager.stop()
        print("\n✅ 서버 종료됨")

    print("\n" + "=" * 70)
    print("Tutorial 4 완료!")
    print("=" * 70)
    print("""
핵심 포인트:
1. GraphQL은 단일 엔드포인트에서 모든 작업 수행
2. Query는 읽기, Mutation은 쓰기 작업
3. Subscription은 WebSocket을 통한 실시간 통신
4. Variables를 사용하여 동적 쿼리 생성 가능
5. Introspection으로 스키마 자동 탐색 가능
6. 타입 안전성이 보장되며 명확한 에러 메시지 제공
    """)


if __name__ == "__main__":
    main()