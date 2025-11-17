"""
Example 1: Load and Query Design

This example demonstrates how to:
- Load a Verilog file
- Compile and elaborate the design
- Query module information
"""

from rtllib import Client


def main():
    # NOTE: Replace with your actual Verilog file path
    verilog_file = "/path/to/cpu.v"

    with Client() as client:
        # Load Verilog file
        result = client.read_verilog(verilog_file)
        print(f"Loaded {result['modules_found']} modules")

        # Process design
        client.compile()
        client.elaborate()

        # Get all modules
        modules = client.get_modules()
        for mod in modules:
            print(f"\nModule: {mod['name']}")
            print(f"  File: {mod['file']}")
            print(f"  Ports: {len(mod['ports'])}")
            print(f"  Instances: {len(mod['instances'])}")
            print(f"  Nets: {len(mod['nets'])}")


if __name__ == "__main__":
    main()
