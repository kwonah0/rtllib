"""Demo of real-time log streaming while performing sync operations.

This demonstrates that:
1. Log streaming runs in a background thread
2. Sync operations continue normally
3. Server logs appear in real-time on the client side
"""

import sys
import time
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib import Client


def custom_log_handler(log_data: dict) -> None:
    """Custom handler for log messages.

    Args:
        log_data: Log message data with keys: level, message, timestamp
    """
    level = log_data.get("level", "INFO")
    message = log_data.get("message", "")
    timestamp = log_data.get("timestamp", "")

    # Custom formatting with colors (if terminal supports it)
    level_colors = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
    }
    reset = "\033[0m"
    color = level_colors.get(level, "")

    print(f"{color}[SERVER LOG] [{level}] {message}{reset}")


def main():
    """Demonstrate log streaming with sync operations."""
    print("=" * 70)
    print("RTL Library Client - Log Streaming Demo")
    print("=" * 70)
    print("\nThis demo shows real-time log streaming from the server")
    print("while performing synchronous operations.\n")

    # Create client with auto-start
    print("1. Creating client and starting server...")
    with Client() as client:
        print("   ✓ Client created and connected!\n")

        # Start log streaming with custom handler
        print("2. Starting log streaming...")
        client.start_log_streaming(custom_log_handler)
        print("   ✓ Log streaming started! Server logs will appear below.\n")

        # Give streaming a moment to connect
        time.sleep(1)

        print("=" * 70)
        print("PERFORMING SYNC OPERATIONS (watch for server logs)")
        print("=" * 70)

        # Health check
        print("\n3. Checking server health...")
        health = client.health_check()
        print(f"   ✓ Status: {health['status']}")
        print(f"   ✓ Backend: {health['backend_type']}")
        time.sleep(0.5)

        # Read Verilog file
        print("\n4. Reading Verilog file...")
        result = client.read_verilog("/path/to/test.v")
        print(f"   ✓ Status: {result['status']}")
        print(f"   ✓ File: {result['file']}")
        print(f"   ✓ Modules found: {result['modules_found']}")
        time.sleep(0.5)

        # Compile
        print("\n5. Compiling...")
        message = client.compile()
        print(f"   ✓ {message}")
        time.sleep(0.5)

        # Elaborate
        print("\n6. Elaborating...")
        message = client.elaborate()
        print(f"   ✓ {message}")
        time.sleep(0.5)

        # Get modules
        print("\n7. Getting modules...")
        modules = client.get_modules()
        print(f"   ✓ Found {len(modules)} module(s)")
        for mod in modules:
            print(f"     - {mod['name']}: {mod['ports']} ports, {mod['instances']} instances")
        time.sleep(0.5)

        # Get ports for a module
        if modules:
            module_name = modules[0]['name']
            print(f"\n8. Getting ports for '{module_name}'...")
            ports = client.get_ports(module_name)
            print(f"   ✓ Found {len(ports)} port(s)")
            for port in ports:
                print(f"     - {port['name']}: {port['direction']} {port['width']}-bit")
            time.sleep(0.5)

            # Get instances for a module
            print(f"\n9. Getting instances in '{module_name}'...")
            instances = client.get_instances(module_name)
            print(f"   ✓ Found {len(instances)} instance(s)")
            for inst in instances:
                print(f"     - {inst['name']}: instance of {inst['module']}")

        print("\n" + "=" * 70)
        print("DEMO COMPLETED")
        print("=" * 70)

        # Check streaming status
        print(f"\n✓ Log streaming is {'active' if client.is_log_streaming_active() else 'inactive'}")

        # Give time to see final logs
        print("\nWaiting 2 seconds for final logs...")
        time.sleep(2)

        print("\nStopping log streaming...")
        client.stop_log_streaming()
        print("✓ Log streaming stopped")

    print("\n" + "=" * 70)
    print("Server has been stopped. Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
