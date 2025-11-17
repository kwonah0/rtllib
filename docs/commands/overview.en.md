# Commands Overview

Complete reference for all rtllib client commands.

## Command Categories

### [Queries](queries.md)

Commands for reading design information (read-only operations).

| Command | Description |
|---------|-------------|
| [health_check](queries.md#health_check) | Check server status |
| [get_modules](queries.md#get_modules) | Get all modules with nested data |
| [get_ports](queries.md#get_ports) | Get module ports |
| [get_instances](queries.md#get_instances) | Get module instances |
| [get_nets](queries.md#get_nets) | Get module nets/wires |

### [Mutations](mutations.md)

Commands for modifying design state.

| Command | Description |
|---------|-------------|
| [read_verilog](mutations.md#read_verilog) | Read single Verilog file |
| [read_verilog_filelist](mutations.md#read_verilog_filelist) | Read multiple files from filelist |
| [compile](mutations.md#compile) | Compile loaded design |
| [elaborate](mutations.md#elaborate) | Elaborate design hierarchy |
| [add_port](mutations.md#add_port) | Add port to module (session) |
| [add_net](mutations.md#add_net) | Add net to module (session) |

### [Types](types.md)

Data types returned by commands.

| Type | Description |
|------|-------------|
| [HealthCheckResult](types.md#healthcheckresult) | Server health status |
| [ModuleInfo](types.md#moduleinfo) | Complete module information |
| [PortInfo](types.md#portinfo) | Port information |
| [InstanceInfo](types.md#instanceinfo) | Instance information |
| [NetInfo](types.md#netinfo) | Net/wire information |
| [ReadVerilogResult](types.md#readverilogresult) | Read file result |
| [ReadFilelistResult](types.md#readfilelistresult) | Read filelist result |
| [AddPortResult](types.md#addportresult) | Add port result |
| [AddNetResult](types.md#addnetresult) | Add net result |

## Typical Workflow

```python
from rtllib import Client

with Client() as client:
    # 1. Check health
    health = client.health_check()

    # 2. Load design
    client.read_verilog("/path/to/design.v")
    # or
    client.read_verilog_filelist("/path/to/files.f")

    # 3. Process design
    client.compile()
    client.elaborate()

    # 4. Query design
    modules = client.get_modules()
    ports = client.get_ports("module_name")
    instances = client.get_instances("module_name")
    nets = client.get_nets("module_name")

    # 5. Modify design (optional, session-based)
    client.add_port("module", "port_name", "input", 8)
    client.add_net("module", "net_name", 32, "wire")
```

## Command Groups by Use Case

### Design Loading

- [read_verilog](mutations.md#read_verilog) - Single file
- [read_verilog_filelist](mutations.md#read_verilog_filelist) - Multiple files

### Design Processing

- [compile](mutations.md#compile) - Syntax/semantic analysis
- [elaborate](mutations.md#elaborate) - Hierarchy expansion

### Design Query

- [get_modules](queries.md#get_modules) - All modules
- [get_ports](queries.md#get_ports) - Ports of a module
- [get_instances](queries.md#get_instances) - Instances in a module
- [get_nets](queries.md#get_nets) - Nets in a module

### Design Modification

- [add_port](mutations.md#add_port) - Add port to module
- [add_net](mutations.md#add_net) - Add net to module

### System

- [health_check](queries.md#health_check) - Server status

## Common Parameters

Many commands support these common parameters:

### filter (optional)

Filter expression for selective queries.

```python
# Examples
ports = client.get_ports("top", filter="direction == 'input'")
nets = client.get_nets("top", filter="width > 1")
```

### hierarchical (optional, default=False)

Include hierarchical information in queries.

```python
# Get flat list with hierarchical paths
modules = client.get_modules(hierarchical=True)
for mod in modules:
    if mod['path']:
        print(f"Path: {mod['path']}")
```

## Return Value Patterns

### Success/Status Checking

```python
# For mutations with 'success' field
result = client.add_port("top", "new_port", "input", 8)
if result['success']:
    print("Operation succeeded")
else:
    print(f"Error: {result['message']}")

# For mutations with 'status' field
result = client.read_verilog("/path/to/file.v")
if result['status'] == 'success':
    print("File loaded successfully")
```

### List Processing

```python
# All query commands return lists
modules = client.get_modules()  # list[ModuleInfo]
for mod in modules:
    print(mod['name'])

# Access nested data
for mod in modules:
    for port in mod['ports']:  # list[PortInfo]
        print(f"  {port['name']}")
```

## Next Steps

- 📖 [Queries Reference](queries.md) - Detailed query commands
- ✏️ [Mutations Reference](mutations.md) - Detailed mutation commands
- 📊 [Types Reference](types.md) - Data type specifications
- 💡 [Examples](../examples/basic-operations.md) - Usage examples
