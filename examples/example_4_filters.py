"""
Example 4: Filter Usage

This example demonstrates how to:
- Use filters to query specific items
- Filter ports by direction
- Filter ports by width
- Filter nets by type
"""

from rtllib import Client


def main():
    # NOTE: Replace with your actual Verilog file path
    verilog_file = "/path/to/design.v"
    module_name = "cpu"

    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        # Get only wide ports (> 1 bit)
        wide_ports = client.get_ports(module_name, filter="width > 1")
        print(f"Wide ports: {len(wide_ports)}")

        # Get only input ports
        inputs = client.get_ports(module_name, filter="direction == 'input'")
        print(f"Input ports: {len(inputs)}")

        # Get only wire nets
        wires = client.get_nets(module_name, filter="net_type == 'wire'")
        print(f"Wire nets: {len(wires)}")


if __name__ == "__main__":
    main()
