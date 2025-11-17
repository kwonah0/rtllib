"""
Example 2: Analyze Port Interfaces

This example demonstrates how to:
- Analyze module port interfaces
- Group ports by direction
- Format port information
"""

from rtllib import Client


def analyze_module_interface(module_name, verilog_file):
    """Analyze and print module port interface."""
    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        ports = client.get_ports(module_name)

        # Group ports by direction
        inputs = [p for p in ports if p['direction'] == 'input']
        outputs = [p for p in ports if p['direction'] == 'output']
        inouts = [p for p in ports if p['direction'] == 'inout']

        print(f"Module: {module_name}")
        print(f"\nInputs ({len(inputs)}):")
        for port in inputs:
            print(f"  {port['name']:<20} [{port['width']:>3} bits]")

        print(f"\nOutputs ({len(outputs)}):")
        for port in outputs:
            print(f"  {port['name']:<20} [{port['width']:>3} bits]")

        if inouts:
            print(f"\nInout ({len(inouts)}):")
            for port in inouts:
                print(f"  {port['name']:<20} [{port['width']:>3} bits]")


def main():
    # NOTE: Replace with your actual module name and Verilog file path
    module_name = "cpu"
    verilog_file = "/path/to/cpu.v"

    analyze_module_interface(module_name, verilog_file)


if __name__ == "__main__":
    main()
