"""Basic usage demo of RTL Library Client."""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rtllib import Client


def main():
    """Demonstrate basic usage of RTL Library Client."""
    print("=" * 60)
    print("RTL Library Client - Basic Usage Demo")
    print("=" * 60)

    # Create client with auto-start (will start server automatically)
    print("\n1. Creating client (server will auto-start)...")
    with Client() as client:
        print("   Client created and connected!")

        # Health check
        print("\n2. Checking server health...")
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Backend: {health['backend_type']}")

        # Read Verilog file
        print("\n3. Reading Verilog file...")
        result = client.read_verilog("/path/to/test.v")
        print(f"   Status: {result['status']}")
        print(f"   File: {result['file']}")
        print(f"   Modules found: {result['modules_found']}")

        # Compile
        print("\n4. Compiling...")
        message = client.compile()
        print(f"   {message}")

        # Elaborate
        print("\n5. Elaborating...")
        message = client.elaborate()
        print(f"   {message}")

        # Get modules
        print("\n6. Getting modules...")
        modules = client.get_modules()
        for mod in modules:
            print(f"   - {mod['name']}: {mod['ports']} ports, {mod['instances']} instances")

        # Get ports for a module
        print("\n7. Getting ports for 'top_module'...")
        ports = client.get_ports("top_module")
        for port in ports:
            print(f"   - {port['name']}: {port['direction']} {port['width']}-bit")

        # Get instances for a module
        print("\n8. Getting instances in 'top_module'...")
        instances = client.get_instances("top_module")
        for inst in instances:
            print(f"   - {inst['name']}: instance of {inst['module']}")

    print("\n" + "=" * 60)
    print("Demo completed! Server has been stopped.")
    print("=" * 60)


if __name__ == "__main__":
    main()
