"""
Example 9: Generate Report

This example demonstrates how to:
- Generate JSON report of design
- Collect module statistics
- Export design information
"""

from rtllib import Client
import json


def generate_design_report(verilog_file, output_file):
    """Generate JSON report of design."""
    with Client() as client:
        client.read_verilog(verilog_file)
        client.compile()
        client.elaborate()

        modules = client.get_modules()

        report = {
            "file": verilog_file,
            "modules": []
        }

        for mod in modules:
            module_data = {
                "name": mod['name'],
                "file": mod['file'],
                "statistics": {
                    "ports": len(mod['ports']),
                    "instances": len(mod['instances']),
                    "nets": len(mod['nets'])
                },
                "ports": [
                    {
                        "name": p['name'],
                        "direction": p['direction'],
                        "width": p['width']
                    }
                    for p in mod['ports']
                ]
            }
            report["modules"].append(module_data)

        # Write report
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Report written to {output_file}")


def main():
    # NOTE: Replace with your actual file paths
    verilog_file = "/path/to/design.v"
    output_file = "design_report.json"

    generate_design_report(verilog_file, output_file)


if __name__ == "__main__":
    main()
