"""
Example 7: Error Handling

This example demonstrates how to:
- Handle file read errors
- Handle compilation errors
- Handle elaboration errors
- Implement safe error handling patterns
"""

from rtllib import Client


def safe_analyze(verilog_file):
    """Analyze design with proper error handling."""
    try:
        with Client() as client:
            # Try to read file
            result = client.read_verilog(verilog_file)
            if result['status'] != 'success':
                print(f"Failed to read file: {result}")
                return None

            # Try to compile
            try:
                client.compile()
            except Exception as e:
                print(f"Compilation error: {e}")
                return None

            # Try to elaborate
            try:
                client.elaborate()
            except Exception as e:
                print(f"Elaboration error: {e}")
                return None

            # Query design
            modules = client.get_modules()
            return modules

    except Exception as e:
        print(f"Client error: {e}")
        return None


def main():
    # NOTE: Replace with your actual Verilog file path
    verilog_file = "/path/to/design.v"

    modules = safe_analyze(verilog_file)
    if modules:
        print(f"Successfully analyzed {len(modules)} modules")
    else:
        print("Analysis failed")


if __name__ == "__main__":
    main()
