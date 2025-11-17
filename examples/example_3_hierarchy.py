"""
Example 3: Hierarchy Analysis

This example demonstrates how to:
- Analyze design hierarchy
- Build hierarchy tree
- Display hierarchical structure
"""

from rtllib import Client


def analyze_hierarchy(verilog_file):
    """Analyze design hierarchy."""
    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        # Get hierarchical view
        modules = client.get_modules(hierarchical=True)

        # Build hierarchy tree
        for mod in modules:
            path = mod.get('path')
            if path:
                level = path.count('.')
                indent = "  " * level
                print(f"{indent}{mod['name']} ({len(mod['instances'])} sub-instances)")
            else:
                print(f"Top: {mod['name']}")


def main():
    # NOTE: Replace with your actual Verilog file path
    verilog_file = "/path/to/design.v"

    analyze_hierarchy(verilog_file)


if __name__ == "__main__":
    main()
