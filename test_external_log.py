"""Test log streaming with external server."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rtllib import Client


def log_handler(log_data):
    """Print received logs."""
    print(f"[CLIENT LOG RECEIVED] Level={log_data.get('level')} Message={log_data.get('message')}")


def main():
    """Test with external server."""
    print("Connecting to external server at 127.0.0.1:9999...")

    # Connect to external server
    client = Client(host="127.0.0.1", port=8888)
    client._ensure_connection()

    print("Connected! Starting log streaming...")
    client.start_log_streaming(log_handler)

    print("Waiting 2 seconds for subscription to connect...")
    time.sleep(2)

    print("\nTriggering operations...")

    print("1. Health check...")
    result = client.health_check()
    print(f"   Result: {result}")
    time.sleep(1)

    print("2. Read verilog...")
    result = client.read_verilog("/test.v")
    print(f"   Result: {result}")
    time.sleep(1)

    print("3. Compile...")
    result = client.compile()
    print(f"   Result: {result}")
    time.sleep(1)

    print("\nWaiting 5 seconds for any remaining logs...")
    time.sleep(5)

    print("Stopping log streaming...")
    client.stop_log_streaming()
    client.close()

    print("Done!")


if __name__ == "__main__":
    main()