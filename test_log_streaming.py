"""Simple test to debug log streaming."""

import sys
import time
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rtllib import Client


def log_handler(log_data):
    """Print received logs."""
    print(f">>> RECEIVED LOG: {log_data}")


async def main():
    """Test log streaming."""
    print("Starting test...")

    # Create client
    client = Client()
    client._ensure_connection()

    print(f"Connected to server at {client.host}:{client.port}")

    # Start log streaming
    print("Starting log streaming...")
    client.start_log_streaming(log_handler)

    # Wait a bit for subscription to connect
    await asyncio.sleep(2)

    # Now trigger some server operations
    print("\nPerforming operations to trigger logs...")

    print("1. Health check...")
    result = client.health_check()
    print(f"   Result: {result}")
    await asyncio.sleep(0.5)

    print("2. Read verilog...")
    result = client.read_verilog("/test.v")
    print(f"   Result: {result}")
    await asyncio.sleep(0.5)

    print("3. Compile...")
    result = client.compile()
    print(f"   Result: {result}")
    await asyncio.sleep(0.5)

    print("4. Elaborate...")
    result = client.elaborate()
    print(f"   Result: {result}")
    await asyncio.sleep(0.5)

    print("\nWaiting 5 seconds for logs...")
    await asyncio.sleep(5)

    print("\nStopping...")
    client.stop_log_streaming()
    client.close()

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
