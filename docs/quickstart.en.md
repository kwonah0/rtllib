# Quick Start Guide

Get started with rtllib in 5 minutes.

## Installation

```bash
pip install rtllib
```

## Basic Workflow

### 1. Import and Create Client

```python
from rtllib import Client

# Create client (auto-starts server)
client = Client()
```

### 2. Check Server Health

```python
health = client.health_check()
print(health)
# {'status': 'ok', 'backend_type': 'dummy'}
```

### 3. Load Verilog File

```python
result = client.read_verilog("/path/to/design.v")
print(f"Status: {result['status']}")
print(f"Modules found: {result['modules_found']}")
```

### 4. Compile and Elaborate

```python
# Compile
message = client.compile()
print(message)  # "Compilation completed"

# Elaborate
message = client.elaborate()
print(message)  # "Elaboration completed"
```

### 5. Query Design

```python
# Get all modules
modules = client.get_modules()
for mod in modules:
    print(f"Module: {mod['name']}")
    print(f"  Ports: {len(mod['ports'])}")
    print(f"  Instances: {len(mod['instances'])}")
    print(f"  Nets: {len(mod['nets'])}")

# Get ports of a specific module
ports = client.get_ports("top_module")
for port in ports:
    print(f"{port['name']}: {port['direction']} [{port['width']} bits]")
```

### 6. Clean Up

```python
# Close client and stop server
client.close()
```

## Using Context Manager (Recommended)

```python
from rtllib import Client

# Automatic cleanup with context manager
with Client() as client:
    # Load design
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # Query
    modules = client.get_modules()
    print(f"Found {len(modules)} modules")

# Server automatically stopped here
```

## Complete Example

```python
from rtllib import Client

def analyze_design(verilog_file):
    """Analyze a Verilog design and print summary."""
    with Client() as client:
        # Load and process
        result = client.read_verilog(verilog_file)
        if result['status'] != 'success':
            print(f"Error: {result}")
            return

        client.compile()
        client.elaborate()

        # Get modules
        modules = client.get_modules()
        print(f"\nDesign Summary:")
        print(f"  Total modules: {len(modules)}")

        # Analyze each module
        for mod in modules:
            print(f"\n  Module: {mod['name']}")
            print(f"    File: {mod['file']}")
            print(f"    Ports: {len(mod['ports'])}")
            print(f"    Instances: {len(mod['instances'])}")
            print(f"    Nets: {len(mod['nets'])}")

            # Show port details
            for port in mod['ports']:
                print(f"      - {port['name']}: {port['direction']} [{port['width']}]")

if __name__ == "__main__":
    analyze_design("/path/to/your/design.v")
```

## Common Patterns

### Query with Filter

```python
# Get only input ports
input_ports = client.get_ports("top", filter="direction == 'input'")

# Get multi-bit nets
buses = client.get_nets("top", filter="width > 1")
```

### Hierarchical Query

```python
# Get all instances in design hierarchy
all_instances = client.get_modules(hierarchical=True)
for mod in all_instances:
    if mod['path']:
        print(f"Hierarchical instance: {mod['path']}")
```

### Reading Multiple Files

```python
# Create a filelist
with open("files.f", "w") as f:
    f.write("/path/to/top.v\n")
    f.write("/path/to/cpu.v\n")
    f.write("/path/to/memory.v\n")

# Read filelist
result = client.read_verilog_filelist("files.f")
print(f"Read {result['files_read']} files")
print(f"Found {result['modules_found']} modules")
```

### Session-based Modifications

```python
with Client() as client:
    # Load design
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # Add a new port
    result = client.add_port(
        module="top",
        port_name="debug_out",
        direction="output",
        width=8
    )
    print(f"Added port: {result['success']}")

    # Add a new net
    result = client.add_net(
        module="top",
        net_name="debug_bus",
        width=8,
        net_type="wire"
    )
    print(f"Added net: {result['success']}")

    # Query modified design
    ports = client.get_ports("top")
    print(f"Top now has {len(ports)} ports")
```

## External Server

If you want to manage the server separately:

```bash
# Terminal 1: Start server
rtllib-server --port 8000
```

```python
# Terminal 2: Connect to external server
from rtllib import Client

client = Client(host="127.0.0.1", port=8000, auto_start=False)
health = client.health_check()
print(health)
```

## Next Steps

- 📚 [Command Reference](commands/queries.md) - Learn all available commands
- 🔍 [Queries](commands/queries.md) - Read design information
- ✏️ [Mutations](commands/mutations.md) - Modify design state
- 📖 [Types](commands/types.md) - Understand data structures
- 💡 [Examples](examples/basic-operations.md) - More usage examples
