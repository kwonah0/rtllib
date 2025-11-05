"""Demo using externally started server.

To use this demo:
1. Start the server in a separate terminal:
   cd ../rtllib-server && uv run rtllib-server --port 7000
2. Run this script:
   uv run python demo/external_server_usage.py
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib import Client


def main():
    """Demonstrate basic usage with external server."""
    print("=" * 60)
    print("RTL Library Client - External Server Demo")
    print("=" * 60)
    print("\nConnecting to server at http://127.0.0.1:7000")

    # Connect to external server (no auto-start)
    with Client(host="127.0.0.1", port=7000) as client:
        print("Connected!\n")

        # Health check
        print("1. Checking server health...")
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Backend: {health['backend_type']}")

        # Read Verilog file
        print("\n2. Reading Verilog file...")
        result = client.read_verilog("/path/to/test.v")
        print(f"   Status: {result['status']}")
        print(f"   File: {result['file']}")
        print(f"   Modules found: {result['modules_found']}")

        # Compile
        print("\n3. Compiling...")
        message = client.compile()
        print(f"   {message}")

        # Elaborate
        print("\n4. Elaborating...")
        message = client.elaborate()
        print(f"   {message}")

        # Get modules
        print("\n5. Getting modules...")
        modules = client.get_modules()
        for mod in modules:
            print(f"   - {mod['name']}: {mod['ports']} ports, {mod['instances']} instances")

        # Get ports for a module
        print("\n6. Getting ports for 'top_module'...")
        ports = client.get_ports("top_module")
        for port in ports:
            print(f"   - {port['name']}: {port['direction']} {port['width']}-bit")

        # Get instances for a module
        print("\n7. Getting instances in 'top_module'...")
        instances = client.get_instances("top_module")
        for inst in instances:
            print(f"   - {inst['name']}: instance of {inst['module']}")

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
