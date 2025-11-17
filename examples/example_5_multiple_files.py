"""
Example 5: Multiple Files

This example demonstrates how to:
- Create a filelist
- Load multiple Verilog files
- Process multi-file designs
"""

from rtllib import Client


def main():
    # Create filelist
    filelist_path = "design.f"
    with open(filelist_path, "w") as f:
        f.write("# Top-level\n")
        f.write("/path/to/top.v\n")
        f.write("\n")
        f.write("# Subsystems\n")
        f.write("/path/to/cpu.v\n")
        f.write("/path/to/memory.v\n")
        f.write("/path/to/io.v\n")

    # Load from filelist
    with Client() as client:
        result = client.read_verilog_filelist(filelist_path)

        if result['status'] == 'success':
            print(f"Successfully read {result['files_read']} files")
            print(f"Found {result['modules_found']} modules")

            client.compile()
            client.elaborate()

            modules = client.get_modules()
            for mod in modules:
                print(f"  - {mod['name']} ({len(mod['instances'])} instances)")
        else:
            print(f"Error: {result['message']}")


if __name__ == "__main__":
    main()
