"""
Tutorial 5: 전체 통합 실습
===========================

이 튜토리얼은 모든 기능을 통합하여 실제 사용 시나리오를 시뮬레이션합니다.

학습 목표:
- 모든 컴포넌트의 통합 사용
- 실제 워크플로우 이해
- 에러 처리 및 리소스 관리 베스트 프랙티스
- 성능 고려사항 이해

시나리오:
RTL 디자인을 읽고, 컴파일하고, 분석하는 전체 파이프라인 실행
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib import Client
import time
import json
from datetime import datetime
from typing import Dict, List, Any
import threading


class RTLAnalyzer:
    """RTL 분석 워크플로우를 관리하는 헬퍼 클래스"""

    def __init__(self):
        self.client = None
        self.logs = []
        self.stats = {
            "start_time": None,
            "end_time": None,
            "operations": [],
            "errors": [],
            "log_count": 0,
        }
        self.lock = threading.Lock()

    def log_handler(self, log_data: Dict[str, Any]):
        """로그 수집 및 분석"""
        with self.lock:
            self.logs.append(log_data)
            self.stats["log_count"] += 1

            # 에러 로그 별도 수집
            if log_data.get("level") == "ERROR":
                self.stats["errors"].append(log_data)

            # 로그 출력 (색상 코딩)
            level = log_data.get("level", "INFO")
            message = log_data.get("message", "")[:60]
            color = {
                "DEBUG": "\033[90m",    # Gray
                "INFO": "\033[37m",     # White
                "WARNING": "\033[33m",  # Yellow
                "ERROR": "\033[31m",    # Red
            }.get(level, "\033[0m")
            print(f"    {color}[LOG] {message}...\\033[0m")

    def record_operation(self, name: str, success: bool, duration: float, result: Any = None):
        """작업 기록"""
        self.stats["operations"].append({
            "name": name,
            "success": success,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "result": result,
        })

    def analyze_design(self, verilog_path: str) -> Dict[str, Any]:
        """전체 RTL 분석 워크플로우 실행"""
        self.stats["start_time"] = datetime.now()

        print(f"\n{'=' * 70}")
        print(f"RTL 분석 시작: {verilog_path}")
        print(f"{'=' * 70}")

        try:
            # Step 1: 클라이언트 초기화
            print("\n[1/7] 클라이언트 초기화")
            print("-" * 40)
            start = time.time()
            self.client = Client(auto_start=True)
            duration = time.time() - start
            self.record_operation("client_init", True, duration)
            print(f"✅ 서버 시작 (포트 {self.client.port}, {duration:.2f}초)")

            # Step 2: 로그 스트리밍 시작
            print("\n[2/7] 로그 스트리밍 활성화")
            print("-" * 40)
            self.client.start_log_streaming(self.log_handler)
            time.sleep(1)  # 연결 대기
            print("✅ 로그 스트리밍 시작")

            # Step 3: 헬스 체크
            print("\n[3/7] 서버 상태 확인")
            print("-" * 40)
            start = time.time()
            health = self.client.health_check()
            duration = time.time() - start
            self.record_operation("health_check", True, duration, health)
            print(f"✅ 서버 상태: {health['status']} (백엔드: {health['backend_type']})")

            # Step 4: Verilog 파일 읽기
            print(f"\n[4/7] Verilog 파일 읽기: {verilog_path}")
            print("-" * 40)
            start = time.time()
            read_result = self.client.read_verilog(verilog_path)
            duration = time.time() - start
            self.record_operation("read_verilog", True, duration, read_result)
            print(f"✅ 파일 읽기 완료")
            print(f"   - 상태: {read_result['status']}")
            print(f"   - 모듈 수: {read_result['modules_found']}")

            # Step 5: 컴파일
            print("\n[5/7] 디자인 컴파일")
            print("-" * 40)
            start = time.time()
            compile_result = self.client.compile()
            duration = time.time() - start
            self.record_operation("compile", True, duration, compile_result)
            print(f"✅ {compile_result}")

            # Step 6: Elaboration
            print("\n[6/7] 디자인 Elaboration")
            print("-" * 40)
            start = time.time()
            elab_result = self.client.elaborate()
            duration = time.time() - start
            self.record_operation("elaborate", True, duration, elab_result)
            print(f"✅ {elab_result}")

            # Step 7: 디자인 분석
            print("\n[7/7] 디자인 분석")
            print("-" * 40)

            # 모듈 목록
            start = time.time()
            modules = self.client.get_modules()
            duration = time.time() - start
            self.record_operation("get_modules", True, duration, modules)
            print(f"✅ {len(modules)}개 모듈 발견:")

            analysis_result = {"modules": []}

            for module in modules:
                module_info = {
                    "name": module["name"],
                    "file": module["file"],
                    "ports": [],
                    "instances": [],
                }

                # 포트 정보
                ports = self.client.get_ports(module["name"])
                module_info["ports"] = ports
                print(f"\n   📦 {module['name']}")
                print(f"      파일: {module['file']}")
                print(f"      포트: {len(ports)}개")

                # 인스턴스 정보
                instances = self.client.get_instances(module["name"])
                module_info["instances"] = instances
                print(f"      인스턴스: {len(instances)}개")

                # 포트 상세
                if ports:
                    print("      포트 목록:")
                    for port in ports[:3]:  # 처음 3개만 표시
                        print(f"        - {port['name']}: {port['direction']} [{port['width']}]")
                    if len(ports) > 3:
                        print(f"        ... 외 {len(ports)-3}개")

                analysis_result["modules"].append(module_info)

            return analysis_result

        except Exception as e:
            print(f"\n❌ 에러 발생: {e}")
            self.stats["errors"].append({
                "type": "exception",
                "message": str(e),
                "timestamp": datetime.now().isoformat(),
            })
            return None

        finally:
            # 정리
            self.stats["end_time"] = datetime.now()

            print("\n" + "=" * 70)
            print("분석 완료 - 통계")
            print("=" * 70)

            # 시간 통계
            if self.stats["start_time"] and self.stats["end_time"]:
                duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
                print(f"총 실행 시간: {duration:.2f}초")

            # 작업 통계
            print(f"수행된 작업: {len(self.stats['operations'])}개")
            for op in self.stats["operations"]:
                status = "✅" if op["success"] else "❌"
                print(f"  {status} {op['name']}: {op['duration']:.3f}초")

            # 로그 통계
            print(f"수집된 로그: {self.stats['log_count']}개")

            # 에러 통계
            if self.stats["errors"]:
                print(f"⚠️  에러 발생: {len(self.stats['errors'])}개")
                for error in self.stats["errors"]:
                    print(f"  - {error.get('message', error)}")

            # 정리
            if self.client:
                if self.client.is_log_streaming_active():
                    self.client.stop_log_streaming()
                    print("\n로그 스트리밍 중지")

                self.client.close()
                print("서버 종료")


def demonstrate_error_recovery():
    """에러 복구 시연"""
    print("\n" + "=" * 70)
    print("에러 처리 및 복구 시연")
    print("=" * 70)

    client = None
    try:
        # 잘못된 포트로 연결 시도
        print("\n1. 잘못된 포트 연결 시도:")
        try:
            client = Client(host="127.0.0.1", port=99999, auto_start=False)
        except Exception as e:
            print(f"   ❌ 예상된 에러: {e}")

        # 자동 복구 (auto_start 사용)
        print("\n2. 자동 서버 시작으로 복구:")
        client = Client(auto_start=True)
        print(f"   ✅ 서버 자동 시작 성공 (포트 {client.port})")

        # 존재하지 않는 파일 읽기
        print("\n3. 존재하지 않는 파일 처리:")
        result = client.read_verilog("/non/existent/file.v")
        print(f"   상태: {result['status']}")

    finally:
        if client:
            client.close()


def main():
    print("=" * 70)
    print("Tutorial 5: 전체 통합 실습")
    print("=" * 70)
    print("""
이 튜토리얼은 실제 사용 시나리오를 시뮬레이션합니다:
1. 서버 자동 시작
2. 로그 스트리밍 활성화
3. RTL 파일 읽기 및 분석
4. 결과 수집 및 통계 생성
5. 에러 처리 및 리소스 정리
""")

    # 메인 워크플로우 실행
    analyzer = RTLAnalyzer()
    result = analyzer.analyze_design("/test/design.v")

    if result:
        print("\n" + "=" * 70)
        print("분석 결과 요약")
        print("=" * 70)
        print(f"총 모듈 수: {len(result['modules'])}")
        for module in result["modules"]:
            print(f"  - {module['name']}: {len(module['ports'])} ports, {len(module['instances'])} instances")

    # 에러 처리 시연
    demonstrate_error_recovery()

    print("\n" + "=" * 70)
    print("Tutorial 5 완료!")
    print("=" * 70)
    print("""
핵심 학습 내용:
1. ✅ 전체 아키텍처 이해
   - 서버 자동 관리 (ServerManager)
   - GraphQL 통신 (Query/Mutation/Subscription)
   - Backend Protocol 패턴

2. ✅ 로그 스트리밍 시스템
   - PubSub 패턴
   - WebSocket 실시간 통신
   - 비동기/동기 공존

3. ✅ 클라이언트 SDK
   - Context Manager 패턴
   - 자동 포트 할당
   - 헬스체크 메커니즘

4. ✅ 에러 처리 및 리소스 관리
   - 자동 복구
   - 리소스 정리
   - 통계 및 모니터링

다음 단계:
- 코드 리뷰에서 발견된 보안/품질 이슈 개선
- 테스트 커버리지 추가
- PyInstaller로 바이너리 빌드
    """)


if __name__ == "__main__":
    main()