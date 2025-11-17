"""
Example 6: Design Modification

This example demonstrates how to:
- Add ports to a module (session-based)
- Add nets to a module (session-based)
- Verify modifications
"""

from rtllib import Client


def main():
    # NOTE: Replace with your actual Verilog file path
    verilog_file = "/path/to/cpu.v"
    module_name = "cpu"

    with Client() as client:
        # Load design
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        # Get current ports
        ports_before = client.get_ports(module_name)
        print(f"Ports before: {len(ports_before)}")

        # Add debug port
        result = client.add_port(
            module=module_name,
            port_name="debug_out",
            direction="output",
            width=32
        )

        if result['success']:
            print(f"Added debug port: {result['port_name']}")

            # Add debug bus net
            client.add_net(
                module=module_name,
                net_name="debug_bus",
                width=32,
                net_type="wire"
            )

            # Verify modifications
            ports_after = client.get_ports(module_name)
            nets = client.get_nets(module_name)

            print(f"Ports after: {len(ports_after)} (+{len(ports_after) - len(ports_before)})")
            print(f"Nets: {len(nets)}")
        else:
            print(f"Error: {result['message']}")


if __name__ == "__main__":
    main()
