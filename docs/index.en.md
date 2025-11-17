# RTL Library Client SDK

Python client SDK for communicating with RTL Library GraphQL server.

## Overview

The `rtllib` package provides a Python API for interacting with RTL (Register Transfer Level) design tools through a GraphQL-based server. It enables you to:

- 📖 **Read Verilog files** and parse design hierarchies
- 🔍 **Query design information** (modules, ports, instances, nets)
- ✏️ **Modify designs** in-session (add ports, nets)
- 🚀 **Auto-manage server** with built-in ServerManager

## Key Features

- **Simple API**: Clean, Pythonic interface for all operations
- **GraphQL-based**: Modern GraphQL communication layer
- **Auto-start Server**: Automatically starts and manages RTL server
- **Type-safe**: Full TypedDict support for all data types
- **Context Manager**: Easy resource management with `with` statements

## Quick Example

```python
from rtllib import Client

# Auto-start server and connect
with Client() as client:
    # Read and process Verilog
    client.read_verilog("/path/to/design.v")
    client.compile()
    client.elaborate()

    # Query design
    modules = client.get_modules()
    for mod in modules:
        ports = mod['ports']
        print(f"{mod['name']}: {len(ports)} ports")
```

## Installation

```bash
pip install rtllib
# or
uv pip install rtllib
```

## Documentation Structure

- **[Commands](commands/overview.md)** - Complete command reference
  - [Queries](commands/queries.md) - Read design information
  - [Mutations](commands/mutations.md) - Modify design state
  - [Types](commands/types.md) - Data type reference
- **[Examples](examples/basic-operations.md)** - Usage examples

## Use Cases

### Design Analysis
Query and analyze RTL designs programmatically

### Design Modification
Add ports, nets, and other elements in-session

### Automation
Integrate RTL operations into Python scripts and workflows

### Testing
Automated testing of RTL designs with Python test frameworks

## Next Steps

- 📖 Browse [Command Reference](commands/queries.md)
- 💡 Check out [Examples](examples/basic-operations.md)

## Requirements

- Python 3.10
- rtllib-server (GraphQL server binary or Python package)

## License

See project repository for license information.
