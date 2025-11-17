"""
Example 8: External Server

This example demonstrates how to:
- Start an external server
- Connect to an external server
- Use the client with external server
- Clean up server process
"""

from rtllib import Client
import subprocess
import time


def main():
    # Start server externally
    server_process = subprocess.Popen(
        ["rtllib-server", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    time.sleep(2)

    try:
        # Connect to external server
        client = Client(host="127.0.0.1", port=8000, auto_start=False)

        # Use client
        health = client.health_check()
        print(f"Server status: {health['status']}")

        # ... rest of operations ...

    finally:
        # Clean up
        client.close()
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    main()
