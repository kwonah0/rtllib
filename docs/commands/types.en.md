# Data Types Reference

All data types returned by query and mutation commands.

---

## HealthCheckResult

Server health check result.

```python
{
    "status": str,        # "ok" or error message
    "backend_type": str   # "dummy" or "real"
}
```

**Example:**
```python
{'status': 'ok', 'backend_type': 'dummy'}
```

**Used by:** [health_check](queries.md#health_check)

---

## ModuleInfo

Complete information about a module including nested ports, instances, and nets.

```python
{
    "name": str,                      # Module name
    "file": str,                      # Source file path
    "path": Optional[str],            # Hierarchical path (if hierarchical query)
    "ports": list[PortInfo],          # List of ports
    "instances": list[InstanceInfo],  # List of instances
    "nets": list[NetInfo]             # List of nets/wires
}
```

**Example:**
```python
{
    'name': 'top_module',
    'file': '/path/to/top.v',
    'path': None,
    'ports': [
        {'name': 'clk', 'direction': 'input', 'width': 1, 'path': None},
        {'name': 'data_out', 'direction': 'output', 'width': 32, 'path': None}
    ],
    'instances': [
        {'name': 'cpu_inst', 'module': 'cpu', 'parent': 'top_module', 'path': None}
    ],
    'nets': [
        {'name': 'internal_bus', 'width': 32, 'net_type': 'wire', 'path': None}
    ]
}
```

**Used by:** [get_modules](queries.md#get_modules)

---

## PortInfo

Information about a module port.

```python
{
    "name": str,            # Port name
    "direction": str,       # "input", "output", or "inout"
    "width": int,           # Bit width
    "path": Optional[str]   # Hierarchical path (if hierarchical query)
}
```

**Example:**
```python
{'name': 'data_in', 'direction': 'input', 'width': 32, 'path': None}
```

**Used by:** [get_ports](queries.md#get_ports), [ModuleInfo](#moduleinfo)

---

## InstanceInfo

Information about a module instance.

```python
{
    "name": str,            # Instance name
    "module": str,          # Module type being instantiated
    "parent": str,          # Parent module name
    "path": Optional[str]   # Hierarchical path (if hierarchical query)
}
```

**Example:**
```python
{'name': 'cpu_inst', 'module': 'cpu', 'parent': 'top_module', 'path': None}
```

**Hierarchical Example:**
```python
{'name': 'alu_inst', 'module': 'alu', 'parent': 'cpu', 'path': 'top.cpu.alu_inst'}
```

**Used by:** [get_instances](queries.md#get_instances), [ModuleInfo](#moduleinfo)

---

## NetInfo

Information about a net/wire.

```python
{
    "name": str,            # Net/wire name
    "width": int,           # Bit width
    "net_type": str,        # "wire", "reg", or "logic"
    "path": Optional[str]   # Hierarchical path (if hierarchical query)
}
```

**Example:**
```python
{'name': 'internal_bus', 'width': 32, 'net_type': 'wire', 'path': None}
```

**Used by:** [get_nets](queries.md#get_nets), [ModuleInfo](#moduleinfo)

---

## ReadVerilogResult

Result of reading a single Verilog file.

```python
{
    "status": str,         # "success" or "error"
    "file": str,           # File path that was read
    "modules_found": int   # Number of modules discovered
}
```

**Example:**
```python
{'status': 'success', 'file': '/path/to/design.v', 'modules_found': 3}
```

**Used by:** [read_verilog](mutations.md#read_verilog)

---

## ReadFilelistResult

Result of reading multiple Verilog files from a filelist.

```python
{
    "success": bool,        # Operation success flag
    "files_read": int,      # Number of files successfully read
    "modules_found": int,   # Total modules discovered
    "message": str          # Status or error message
}
```

**Example:**
```python
{
    'success': True,
    'files_read': 5,
    'modules_found': 12,
    'message': 'Successfully read 5 files'
}
```

**Used by:** [read_verilog_filelist](mutations.md#read_verilog_filelist)

---

## AddPortResult

Result of adding a port to a module.

```python
{
    "success": bool,     # Operation success flag
    "module": str,       # Module that was modified
    "port_name": str,    # Name of the added port
    "message": str       # Status or error message
}
```

**Example:**
```python
{
    'success': True,
    'module': 'top',
    'port_name': 'debug_out',
    'message': 'Port added successfully'
}
```

**Used by:** [add_port](mutations.md#add_port)

---

## AddNetResult

Result of adding a net/wire to a module.

```python
{
    "success": bool,     # Operation success flag
    "module": str,       # Module that was modified
    "net_name": str,     # Name of the added net
    "message": str       # Status or error message
}
```

**Example:**
```python
{
    'success': True,
    'module': 'top',
    'net_name': 'internal_bus',
    'message': 'Net added successfully'
}
```

**Used by:** [add_net](mutations.md#add_net)

---

## Type Relationships

### Nested Structure

```
ModuleInfo
├── ports: list[PortInfo]
├── instances: list[InstanceInfo]
└── nets: list[NetInfo]
```

### Query Results

| Query Command | Returns |
|---------------|---------|
| health_check | HealthCheckResult |
| get_modules | list[ModuleInfo] |
| get_ports | list[PortInfo] |
| get_instances | list[InstanceInfo] |
| get_nets | list[NetInfo] |

### Mutation Results

| Mutation Command | Returns |
|------------------|---------|
| read_verilog | ReadVerilogResult |
| read_verilog_filelist | ReadFilelistResult |
| compile | str |
| elaborate | str |
| add_port | AddPortResult |
| add_net | AddNetResult |

---

## Type Hints

When using Python type hints with the rtllib client:

```python
from rtllib import Client
from rtllib.types import (
    ModuleInfo,
    PortInfo,
    InstanceInfo,
    NetInfo,
    HealthCheckResult,
    ReadVerilogResult,
    AddPortResult,
    AddNetResult
)

client = Client()

# Type-safe usage
health: HealthCheckResult = client.health_check()
modules: list[ModuleInfo] = client.get_modules()
ports: list[PortInfo] = client.get_ports("top")
```

All types are defined as `TypedDict` in `rtllib.types` module for proper type checking support.

---

## Common Patterns

### Checking Success

```python
# For mutations with success field
result = client.add_port("top", "new_port", "input", 8)
if result['success']:
    print("Operation succeeded")
else:
    print(f"Error: {result['message']}")

# For read_verilog
result = client.read_verilog("/path/to/file.v")
if result['status'] == 'success':
    print(f"Found {result['modules_found']} modules")
```

### Accessing Nested Data

```python
modules = client.get_modules()
for module in modules:
    print(f"Module: {module['name']}")

    # Access nested ports
    for port in module['ports']:
        print(f"  Port: {port['name']} ({port['direction']}, {port['width']} bits)")

    # Access nested instances
    for inst in module['instances']:
        print(f"  Instance: {inst['name']} of type {inst['module']}")

    # Access nested nets
    for net in module['nets']:
        print(f"  Net: {net['name']} ({net['net_type']}, {net['width']} bits)")
```
