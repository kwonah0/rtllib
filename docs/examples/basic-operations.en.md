# Basic Operations Examples

Common usage patterns and examples for rtllib.

## Example 1: Load and Query Design

```python
from rtllib import Client

with Client() as client:
    # Load Verilog file
    result = client.read_verilog("/path/to/cpu.v")
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
```

## Example 2: Analyze Port Interfaces

```python
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

# Usage
analyze_module_interface("cpu", "/path/to/cpu.v")
```

## Example 3: Hierarchy Analysis

```python
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

# Usage
analyze_hierarchy("/path/to/design.v")
```

## Example 4: Filter Usage

```python
from rtllib import Client

with Client() as client:
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # Get only wide ports (> 1 bit)
    wide_ports = client.get_ports("cpu", filter="width > 1")
    print(f"Wide ports: {len(wide_ports)}")

    # Get only input ports
    inputs = client.get_ports("cpu", filter="direction == 'input'")
    print(f"Input ports: {len(inputs)}")

    # Get only wire nets
    wires = client.get_nets("cpu", filter="net_type == 'wire'")
    print(f"Wire nets: {len(wires)}")
```

## Example 5: Multiple Files

```python
from rtllib import Client

# Create filelist
with open("design.f", "w") as f:
    f.write("# Top-level\n")
    f.write("/path/to/top.v\n")
    f.write("\n")
    f.write("# Subsystems\n")
    f.write("/path/to/cpu.v\n")
    f.write("/path/to/memory.v\n")
    f.write("/path/to/io.v\n")

# Load from filelist
with Client() as client:
    result = client.read_verilog_filelist("design.f")

    if result['success']:
        print(f"Successfully read {result['files_read']} files")
        print(f"Found {result['modules_found']} modules")

        client.compile()
        client.elaborate()

        modules = client.get_modules()
        for mod in modules:
            print(f"  - {mod['name']} ({len(mod['instances'])} instances)")
    else:
        print(f"Error: {result['message']}")
```

## Example 6: Design Modification

```python
from rtllib import Client

with Client() as client:
    # Load design
    client.read_verilog("/path/to/cpu.v")
    client.compile()
    client.elaborate()

    # Get current ports
    ports_before = client.get_ports("cpu")
    print(f"Ports before: {len(ports_before)}")

    # Add debug port
    result = client.add_port(
        module="cpu",
        port_name="debug_out",
        direction="output",
        width=32
    )

    if result['success']:
        print(f"Added debug port: {result['port_name']}")

        # Add debug bus net
        client.add_net(
            module="cpu",
            net_name="debug_bus",
            width=32,
            net_type="wire"
        )

        # Verify modifications
        ports_after = client.get_ports("cpu")
        nets = client.get_nets("cpu")

        print(f"Ports after: {len(ports_after)} (+{len(ports_after) - len(ports_before)})")
        print(f"Nets: {len(nets)}")
    else:
        print(f"Error: {result['message']}")
```

## Example 7: Error Handling

```python
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

# Usage
modules = safe_analyze("/path/to/design.v")
if modules:
    print(f"Successfully analyzed {len(modules)} modules")
else:
    print("Analysis failed")
```

## Example 8: External Server

```python
from rtllib import Client
import subprocess
import time

# Start server externally
server_process = subprocess.Popen(
    ["rtllib-server", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(2)

try:
    # Connect to external server
    client = Client(host="127.0.0.1", port=8000, auto_start=False)

    # Use client
    health = client.health_check()
    print(f"Server status: {health['status']}")

    # ... rest of operations ...

finally:
    # Clean up
    client.close()
    server_process.terminate()
    server_process.wait()
```

## Example 9: Generate Report

```python
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

# Usage
generate_design_report("/path/to/design.v", "design_report.json")
```

## Next Steps

- 📖 [Queries Reference](../commands/queries.md) - All query commands
- ✏️ [Mutations Reference](../commands/mutations.md) - All mutation commands
- 📊 [Types Reference](../commands/types.md) - Data types
