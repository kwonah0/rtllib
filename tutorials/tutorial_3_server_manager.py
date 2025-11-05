"""
Tutorial 3: 클라이언트 SDK 심화 - ServerManager
================================================

이 튜토리얼은 ServerManager의 내부 동작을 깊이 이해합니다.

학습 목표:
- 자동 포트 할당 메커니즘 이해
- Subprocess 관리 방법 이해
- 헬스체크를 통한 서버 준비 확인 이해
- 로그 파일 관리 이해

ServerManager 책임:
- 빈 포트 찾기 (socket 사용)
- 서버 프로세스 시작/종료 (subprocess)
- 헬스체크 및 재시도
- 임시 로그 파일 관리
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib.server_manager import ServerManager
import socket
import time
import os
import tempfile


def find_free_port():
    """빈 포트를 찾는 방법 시연"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # 0은 OS가 자동으로 포트 할당
        s.listen(1)
        port = s.getsockname()[1]
    return port


def main():
    print("=" * 70)
    print("Tutorial 3: 클라이언트 SDK 심화 - ServerManager")
    print("=" * 70)

    # Step 1: 포트 할당 메커니즘 이해
    print("\n[Step 1] 자동 포트 할당 메커니즘")
    print("-" * 40)
    print("ServerManager가 포트를 찾는 방법:")
    print("1. 기본 포트(5000)부터 시작")
    print("2. socket.bind()로 사용 가능 여부 확인")
    print("3. 사용 중이면 다음 포트 시도 (최대 100개)")

    # 직접 빈 포트 찾기
    free_port = find_free_port()
    print(f"\n✅ OS가 할당한 빈 포트: {free_port}")

    # Step 2: ServerManager 직접 사용
    print("\n[Step 2] ServerManager 수동 제어")
    print("-" * 40)

    # ServerManager 생성 (포트 자동 할당)
    manager = ServerManager(
        host="127.0.0.1",
        port=None,  # None이면 자동 할당
        server_mode="python",  # python 모드로 실행
    )

    print(f"할당된 포트: {manager.port}")
    print(f"서버 모드: {manager.server_mode}")

    # Step 3: 서버 시작 과정 추적
    print("\n[Step 3] 서버 시작 과정 추적")
    print("-" * 40)

    print("서버 시작 중...")
    manager.start()

    # subprocess 정보 확인
    if manager.process:
        print(f"✅ 프로세스 ID: {manager.process.pid}")
        print(f"✅ 프로세스 상태: {'실행 중' if manager.process.poll() is None else '종료됨'}")

    # 로그 파일 위치
    if hasattr(manager, '_stdout_file'):
        print(f"✅ stdout 로그: {manager._stdout_file.name}")
    if hasattr(manager, '_stderr_file'):
        print(f"✅ stderr 로그: {manager._stderr_file.name}")

    # Step 4: 헬스체크 메커니즘
    print("\n[Step 4] 헬스체크 메커니즘")
    print("-" * 40)
    print("헬스체크 과정:")
    print("1. 초기 3초 대기 (서버 부팅 시간)")
    print("2. HTTP GET /health 또는 GraphQL healthCheck")
    print("3. 최대 30회 재시도 (1초 간격)")

    # 수동 헬스체크
    for i in range(5):
        if manager.is_running():
            print(f"✅ 서버 준비 완료! (시도 {i+1}/5)")
            break
        else:
            print(f"⏳ 대기 중... (시도 {i+1}/5)")
            time.sleep(1)

    # Step 5: 서버 로그 읽기
    print("\n[Step 5] 서버 로그 확인")
    print("-" * 40)

    if hasattr(manager, '_stdout_file'):
        # stdout 로그 읽기
        with open(manager._stdout_file.name, 'r') as f:
            logs = f.readlines()
            if logs:
                print("최근 서버 로그 (최대 5줄):")
                for line in logs[-5:]:
                    print(f"  > {line.strip()}")
            else:
                print("로그가 비어있습니다.")

    # Step 6: 여러 ServerManager 인스턴스 관리
    print("\n[Step 6] 다중 서버 관리")
    print("-" * 40)

    # 두 번째 서버 시작 (다른 포트)
    manager2 = ServerManager(host="127.0.0.1", port=None)
    manager2.start()

    print(f"서버 1: 포트 {manager.port} (PID: {manager.process.pid if manager.process else 'N/A'})")
    print(f"서버 2: 포트 {manager2.port} (PID: {manager2.process.pid if manager2.process else 'N/A'})")

    # Step 7: 리소스 정리
    print("\n[Step 7] 리소스 정리")
    print("-" * 40)

    # 서버 종료
    manager.stop()
    manager2.stop()

    print("✅ 서버 프로세스 종료")

    # 로그 파일 정리 확인
    if hasattr(manager, '_stdout_file'):
        log_file = manager._stdout_file.name
        if not os.path.exists(log_file):
            print("✅ 로그 파일 자동 삭제됨")
        else:
            print(f"⚠️  로그 파일이 남아있음: {log_file}")

    # Step 8: Context Manager 패턴
    print("\n[Step 8] Context Manager 사용")
    print("-" * 40)

    print("with 문을 사용한 자동 리소스 관리:")
    with ServerManager(host="127.0.0.1", port=None) as mgr:
        print(f"  서버 시작: 포트 {mgr.port}")
        time.sleep(1)
        print(f"  서버 상태: {'실행 중' if mgr.is_running() else '정지됨'}")
    # __exit__ 에서 자동으로 stop() 호출
    print("  서버 자동 종료됨")

    # Step 9: 에러 처리
    print("\n[Step 9] 에러 처리")
    print("-" * 40)

    # 이미 사용 중인 포트로 시작 시도
    used_port = 5000  # 이미 사용 중일 수 있는 포트
    try:
        # 먼저 포트 점유
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('127.0.0.1', used_port))
        test_socket.listen(1)

        # 같은 포트로 서버 시작 시도
        manager3 = ServerManager(host="127.0.0.1", port=used_port)
        manager3.start()
    except Exception as e:
        print(f"❌ 예상된 에러: {e}")
    finally:
        test_socket.close()

    print("\n" + "=" * 70)
    print("Tutorial 3 완료!")
    print("=" * 70)
    print("""
핵심 포인트:
1. ServerManager는 포트 할당, 프로세스 관리, 로그 관리를 담당
2. 자동 포트 찾기로 포트 충돌 방지
3. 헬스체크로 서버 준비 상태 확인
4. Context Manager 패턴으로 자동 리소스 정리
5. 여러 서버 인스턴스를 독립적으로 관리 가능
    """)


if __name__ == "__main__":
    main()