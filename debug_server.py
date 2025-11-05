"""Debug script to test server manager."""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rtllib.server_manager import ServerManager
import httpx

print("Testing ServerManager...")

manager = ServerManager()
print(f"Server mode: {manager.server_mode}")
print(f"Host: {manager.host}")
print(f"Port: {manager.port}")

# Find and assign port
if manager.port is None:
    manager.port = manager.find_free_port()
    print(f"Assigned port: {manager.port}")

# Try to start manually without waiting
print("\nStarting server process...")
server_path = Path(__file__).parent.parent / "rtllib-server"
print(f"Server path exists: {server_path.exists()} - {server_path}")

cmd = [
    "uv",
    "run",
    "--directory",
    str(server_path),
    "rtllib-server",
    "--host",
    manager.host,
    "--port",
    str(manager.port),
]
print(f"Command: {' '.join(cmd)}")

import subprocess
proc = subprocess.Popen(cmd)
print(f"Process started with PID: {proc.pid}")

# Wait a bit and check if process is still running
time.sleep(3)
if proc.poll() is not None:
    print(f"ERROR: Process terminated with code: {proc.poll()}")
else:
    print("Process is still running")

# Try health check
print(f"\nTrying health check at http://{manager.host}:{manager.port}/health")
for i in range(5):
    try:
        response = httpx.get(f"http://{manager.host}:{manager.port}/health", timeout=1.0)
        print(f"  Attempt {i+1}: Success! Status: {response.status_code}, Body: {response.text}")
        break
    except Exception as e:
        print(f"  Attempt {i+1}: Failed - {e}")
        time.sleep(1)

# Clean up
print("\nCleaning up...")
proc.terminate()
proc.wait()
print("Done!")
