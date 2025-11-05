"""
Tutorial 2: 로그 스트리밍 시스템 이해
=====================================

이 튜토리얼은 실시간 로그 스트리밍 시스템의 동작 원리를 이해합니다.

학습 목표:
- PubSub 패턴을 사용한 로그 브로드캐스팅 이해
- WebSocket을 통한 GraphQL Subscription 이해
- 비동기 로그 처리와 동기 API의 공존 이해

로그 흐름:
Backend 로그 → LogHandler → PubSub.publish() → GraphQL Subscription → WebSocket → LogStreamClient → 콜백
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib import Client
import time
import threading


class LogAnalyzer:
    """로그 메시지를 분석하고 통계를 수집하는 헬퍼 클래스"""

    def __init__(self):
        self.log_count = 0
        self.log_levels = {}
        self.lock = threading.Lock()

    def handle_log(self, log_data):
        """로그 콜백 함수"""
        with self.lock:
            self.log_count += 1
            level = log_data.get("level", "UNKNOWN")
            message = log_data.get("message", "")
            timestamp = log_data.get("timestamp", "")

            # 레벨별 카운트
            self.log_levels[level] = self.log_levels.get(level, 0) + 1

            # 로그 출력 (색상 코딩)
            color_map = {
                "DEBUG": "\033[36m",    # Cyan
                "INFO": "\033[32m",     # Green
                "WARNING": "\033[33m",  # Yellow
                "ERROR": "\033[31m",    # Red
            }
            color = color_map.get(level, "\033[0m")
            reset = "\033[0m"

            print(f"  {color}[{timestamp[-8:]}] [{level:7}] {message[:60]}...{reset}")

    def print_stats(self):
        """수집한 통계 출력"""
        with self.lock:
            print(f"\n로그 통계:")
            print(f"  총 로그 수: {self.log_count}")
            for level, count in self.log_levels.items():
                print(f"  {level}: {count}개")


def main():
    print("=" * 70)
    print("Tutorial 2: 로그 스트리밍 시스템 이해")
    print("=" * 70)

    analyzer = LogAnalyzer()

    # Step 1: 클라이언트 생성
    print("\n[Step 1] 클라이언트 및 서버 시작")
    print("-" * 40)
    client = Client()
    print(f"✅ 서버가 포트 {client.port}에서 시작되었습니다.")

    # Step 2: 로그 스트리밍 시작
    print("\n[Step 2] 로그 스트리밍 활성화")
    print("-" * 40)
    print("로그 스트리밍 동작 원리:")
    print("1. LogStreamClient가 별도 스레드에서 실행됨")
    print("2. WebSocket으로 GraphQL Subscription 연결")
    print("3. 서버의 StreamingLogHandler가 모든 로그 캡처")
    print("4. LogHandler → PubSub → Subscription → WebSocket → Client")

    client.start_log_streaming(analyzer.handle_log)
    print("✅ 로그 스트리밍이 시작되었습니다.")

    # WebSocket 연결 대기
    print("\n⏳ WebSocket 연결 대기 중...")
    time.sleep(2)

    # Step 3: 다양한 작업 실행하며 로그 관찰
    print("\n[Step 3] 서버 작업 실행 및 로그 관찰")
    print("-" * 40)

    print("\n📍 Health Check 실행:")
    client.health_check()
    time.sleep(0.5)

    print("\n📍 Verilog 파일 읽기:")
    client.read_verilog("/design/top.v")
    time.sleep(0.5)

    print("\n📍 컴파일 실행:")
    client.compile()
    time.sleep(0.5)

    print("\n📍 Elaboration 실행:")
    client.elaborate()
    time.sleep(0.5)

    print("\n📍 모듈 목록 조회:")
    modules = client.get_modules()
    print(f"   → {len(modules)}개 모듈 발견")
    time.sleep(0.5)

    # Step 4: 스트리밍 상태 확인
    print("\n[Step 4] 스트리밍 상태 확인")
    print("-" * 40)
    if client.is_log_streaming_active():
        print("✅ 로그 스트리밍이 활성 상태입니다.")
    else:
        print("❌ 로그 스트리밍이 비활성 상태입니다.")

    # 통계 출력
    analyzer.print_stats()

    # Step 5: PubSub 시스템 이해
    print("\n[Step 5] PubSub 시스템 동작 원리")
    print("-" * 40)
    print("""
PubSub 시스템 구성요소:
1. LogPubSub (pubsub.py):
   - 싱글톤 인스턴스로 동작
   - 구독자들의 asyncio.Queue 관리
   - publish() 메서드로 모든 구독자에게 브로드캐스트

2. StreamingLogHandler (log_handler.py):
   - Python logging.Handler 상속
   - emit() 메서드에서 로그를 PubSub에 게시
   - Event loop를 통해 비동기 태스크 생성

3. GraphQL Subscription (schema.py):
   - log_stream() 비동기 제너레이터
   - PubSub에서 Queue를 구독
   - 메시지를 받아 GraphQL 응답으로 변환

4. LogStreamClient (log_stream.py):
   - 별도 스레드에서 실행
   - WebSocket으로 Subscription 유지
   - 받은 로그를 콜백 함수로 전달
    """)

    # Step 6: 로그 스트리밍 중지
    print("\n[Step 6] 로그 스트리밍 중지")
    print("-" * 40)
    client.stop_log_streaming()
    print("✅ 로그 스트리밍이 중지되었습니다.")

    # 클라이언트 종료
    client.close()
    print("✅ 서버가 종료되었습니다.")

    print("\n" + "=" * 70)
    print("Tutorial 2 완료!")
    print("=" * 70)
    print("""
핵심 포인트:
1. 로그 스트리밍은 별도 스레드에서 비동기로 실행
2. 메인 스레드의 동기 API와 충돌하지 않음
3. PubSub 패턴으로 다수의 구독자 지원 가능
4. WebSocket을 통해 실시간 양방향 통신 구현
    """)


if __name__ == "__main__":
    main()