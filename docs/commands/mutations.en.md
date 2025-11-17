# Mutation Commands Reference

All mutation commands for modifying design state on the RTL Library server.

---

## read_verilog

Read and parse a single Verilog file.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| path | str | ✅ | - | Path to the Verilog file |

**Returns:** `ReadVerilogResult`

| Field | Type | Description |
|-------|------|-------------|
| status | str | Operation status: "success" or "error" |
| file | str | Path of the file that was read |
| modules_found | int | Number of modules discovered in the file |

**Example (Python):**

```python
from rtllib import Client

client = Client()
result = client.read_verilog("/path/to/design.v")
print(f"Status: {result['status']}")
print(f"Modules found: {result['modules_found']}")
```

**Example (GraphQL):**

```graphql
mutation ReadVerilog($path: String!) {
  read_verilog(path: $path) {
    status
    file
    modules_found
  }
}
```

**Related:** [read_verilog_filelist](#read_verilog_filelist)

---

## read_verilog_filelist

Read multiple Verilog files from a filelist.

The filelist format supports:
- File paths (one per line)
- Comments (lines starting with `#` or `//`)
- Options like `+incdir+`, `-v`, `-y` (backend-specific)

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| filelist_path | str | ✅ | - | Path to the filelist file |

**Returns:** `ReadFilelistResult`

| Field | Type | Description |
|-------|------|-------------|
| success | bool | Whether operation succeeded |
| files_read | int | Number of files successfully read |
| modules_found | int | Total number of modules discovered |
| message | str | Status or error message |

**Example (Python):**

```python
result = client.read_verilog_filelist("/path/to/files.f")
if result['success']:
    print(f"Read {result['files_read']} files")
    print(f"Found {result['modules_found']} modules")
else:
    print(f"Error: {result['message']}")
```

**Example Filelist Format:**

```text
# Design files
/path/to/top.v
/path/to/cpu.v
/path/to/memory.v

// Include directories
+incdir+/path/to/includes

# Library files
-v /path/to/lib/cells.v
```

**Example (GraphQL):**

```graphql
mutation ReadFilelist($filelistPath: String!) {
  read_verilog_filelist(filelist_path: $filelistPath) {
    success
    files_read
    modules_found
    message
  }
}
```

**Related:** [read_verilog](#read_verilog)

---

## compile

Compile the loaded Verilog code.

This step analyzes syntax and semantics of the loaded design.

**Parameters:** None

**Returns:** `str` - Completion message

**Example (Python):**

```python
# Load files first
client.read_verilog("/path/to/design.v")

# Then compile
message = client.compile()
print(message)  # "Compilation completed"
```

**Example (GraphQL):**

```graphql
mutation {
  compile
}
```

**Related:** [elaborate](#elaborate), [read_verilog](#read_verilog)

---

## elaborate

Elaborate the compiled design.

This step expands the design hierarchy and resolves all module instances.

**Parameters:** None

**Returns:** `str` - Completion message

**Example (Python):**

```python
# Load and compile first
client.read_verilog("/path/to/design.v")
client.compile()

# Then elaborate
message = client.elaborate()
print(message)  # "Elaboration completed"

# Now you can query the design
modules = client.get_modules()
```

**Example (GraphQL):**

```graphql
mutation {
  elaborate
}
```

**Related:** [compile](#compile), [get_modules](queries.md#get_modules)

---

## add_port

Add a port to a module (session-based modification, not persisted).

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | Target module name |
| port_name | str | ✅ | - | Name for the new port |
| direction | str | ✅ | - | Port direction: "input", "output", or "inout" |
| width | int | ✅ | - | Bit width of the port |

**Returns:** `AddPortResult`

| Field | Type | Description |
|-------|------|-------------|
| success | bool | Whether operation succeeded |
| module | str | Module that was modified |
| port_name | str | Name of the added port |
| message | str | Status or error message |

**Example (Python):**

```python
result = client.add_port(
    module="top",
    port_name="new_signal",
    direction="input",
    width=8
)

if result['success']:
    print(f"Added port {result['port_name']} to {result['module']}")
else:
    print(f"Error: {result['message']}")
```

**Example (GraphQL):**

```graphql
mutation AddPort(
  $module: String!,
  $portName: String!,
  $direction: String!,
  $width: Int!
) {
  add_port(
    module: $module,
    port_name: $portName,
    direction: $direction,
    width: $width
  ) {
    success
    module
    port_name
    message
  }
}
```

**Related:** [get_ports](queries.md#get_ports), [add_net](#add_net)

---

## add_net

Add a net/wire to a module (session-based modification, not persisted).

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | Target module name |
| net_name | str | ✅ | - | Name for the new net |
| width | int | ✅ | - | Bit width of the net |
| net_type | str | ❌ | "wire" | Net type: "wire", "reg", or "logic" |

**Returns:** `AddNetResult`

| Field | Type | Description |
|-------|------|-------------|
| success | bool | Whether operation succeeded |
| module | str | Module that was modified |
| net_name | str | Name of the added net |
| message | str | Status or error message |

**Example (Python):**

```python
# Add a wire
result = client.add_net(
    module="top",
    net_name="internal_bus",
    width=32,
    net_type="wire"
)

# Add a register
result = client.add_net(
    module="top",
    net_name="state_reg",
    width=4,
    net_type="reg"
)

if result['success']:
    print(f"Added {result['net_name']} to {result['module']}")
```

**Example (GraphQL):**

```graphql
mutation AddNet(
  $module: String!,
  $netName: String!,
  $width: Int!,
  $netType: String!
) {
  add_net(
    module: $module,
    net_name: $netName,
    width: $width,
    net_type: $netType
  ) {
    success
    module
    net_name
    message
  }
}
```

**Related:** [get_nets](queries.md#get_nets), [add_port](#add_port)

---

## Workflow Example

Complete workflow using mutations:

```python
from rtllib import Client

# Initialize client (auto-starts server)
with Client() as client:
    # 1. Check server health
    health = client.health_check()
    print(f"Server status: {health['status']}")

    # 2. Read Verilog file
    result = client.read_verilog("/path/to/design.v")
    print(f"Loaded {result['modules_found']} modules")

    # 3. Compile
    client.compile()

    # 4. Elaborate
    client.elaborate()

    # 5. Query design
    modules = client.get_modules()
    print(f"Design has {len(modules)} modules")

    # 6. Modify design (session-based)
    client.add_port("top", "debug_out", "output", 8)
    client.add_net("top", "debug_bus", 8, "wire")

    # 7. Query modified design
    ports = client.get_ports("top")
    print(f"Top module now has {len(ports)} ports")
```

---

## Summary Table

Quick reference for all mutation commands:

| Command | Purpose | Key Parameters | Returns |
|---------|---------|----------------|---------|
| read_verilog | Read single file | path | ReadVerilogResult |
| read_verilog_filelist | Read multiple files | filelist_path | ReadFilelistResult |
| compile | Compile design | None | str (message) |
| elaborate | Elaborate design | None | str (message) |
| add_port | Add port to module | module, port_name, direction, width | AddPortResult |
| add_net | Add net to module | module, net_name, width, net_type | AddNetResult |

---

## Important Notes

!!! warning "Session-Based Modifications"
    The `add_port` and `add_net` mutations are **session-based** and do not persist changes to the original Verilog files. They only modify the in-memory representation on the server.

!!! info "Operation Order"
    For proper operation, follow this order:
    1. read_verilog or read_verilog_filelist
    2. compile
    3. elaborate
    4. Query or modify the design

!!! tip "Error Handling"
    Always check the `status`, `success`, or `message` fields in return values to handle errors appropriately.
