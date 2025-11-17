# Query Commands Reference

All query commands for retrieving design information from the RTL Library server.

---

## health_check

Check server health and status.

**Parameters:** None

**Returns:** `HealthCheckResult`

| Field | Type | Description |
|-------|------|-------------|
| status | str | Server status: "ok" or error message |
| backend_type | str | Backend type: "dummy" or "real" |

**Example (Python):**

```python
from rtllib import Client

client = Client()
result = client.health_check()
print(result)
# {'status': 'ok', 'backend_type': 'dummy'}
```

**Example (GraphQL):**

```graphql
query {
  health_check {
    status
    backend_type
  }
}
```

**Related:** None

---

## get_modules

Get all modules in the design with nested port/instance/net information.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| filter | str | ❌ | None | Filter expression (backend-specific) |
| hierarchical | bool | ❌ | False | Include hierarchical instances as flat list with paths |

**Returns:** `list[ModuleInfo]`

| Field | Type | Description |
|-------|------|-------------|
| name | str | Module name |
| file | str | Source file path |
| path | str or None | Hierarchical path (if hierarchical=True) |
| ports | list[PortInfo] | List of port information |
| instances | list[InstanceInfo] | List of instance information |
| nets | list[NetInfo] | List of net/wire information |

**Example (Python):**

```python
# Get all modules
modules = client.get_modules()
for mod in modules:
    print(f"{mod['name']}: {len(mod['ports'])} ports, {len(mod['instances'])} instances")

# With filter
top_modules = client.get_modules(filter="name == 'top'")

# With hierarchical view
all_instances = client.get_modules(hierarchical=True)
```

**Example (GraphQL):**

```graphql
query GetModules($filter: String, $hierarchical: Boolean!) {
  modules(filter: $filter, hierarchical: $hierarchical) {
    name
    file
    path
    ports {
      name
      direction
      width
    }
    instances {
      name
      module
      parent
    }
    nets {
      name
      width
      net_type
    }
  }
}
```

**Related:** [get_ports](#get_ports), [get_instances](#get_instances), [get_nets](#get_nets)

---

## get_ports

Get all ports of a specific module.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | Module name |
| filter | str | ❌ | None | Filter expression (e.g., "direction == 'input'") |
| hierarchical | bool | ❌ | False | Include ports from sub-instances |

**Returns:** `list[PortInfo]`

| Field | Type | Description |
|-------|------|-------------|
| name | str | Port name |
| direction | str | Port direction: "input", "output", or "inout" |
| width | int | Bit width |
| path | str or None | Hierarchical path (if hierarchical=True) |

**Example (Python):**

```python
# Get all ports
ports = client.get_ports("top_module")

# Get only input ports
input_ports = client.get_ports("top_module", filter="direction == 'input'")

# Get ports with hierarchy
all_ports = client.get_ports("top_module", hierarchical=True)

# Display ports
for port in ports:
    print(f"{port['name']}: {port['direction']} [{port['width']} bits]")
```

**Example (GraphQL):**

```graphql
query GetPorts($module: String!, $filter: String, $hierarchical: Boolean!) {
  ports(module: $module, filter: $filter, hierarchical: $hierarchical) {
    name
    direction
    width
    path
  }
}
```

**Related:** [get_modules](#get_modules), [add_port](mutations.md#add_port)

---

## get_instances

Get all instances in a specific module.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | Module name |
| filter | str | ❌ | None | Filter expression (e.g., "module == 'cpu'") |
| hierarchical | bool | ❌ | False | Include instances from sub-hierarchy |

**Returns:** `list[InstanceInfo]`

| Field | Type | Description |
|-------|------|-------------|
| name | str | Instance name |
| module | str | Module type this instance instantiates |
| parent | str | Parent module name |
| path | str or None | Hierarchical path (if hierarchical=True) |

**Example (Python):**

```python
# Get all instances
instances = client.get_instances("top_module")

# Filter by module type
cpu_instances = client.get_instances("top_module", filter="module == 'cpu'")

# Get full hierarchy
all_instances = client.get_instances("top_module", hierarchical=True)

# Display instances
for inst in instances:
    print(f"{inst['name']}: instance of {inst['module']}")
```

**Example (GraphQL):**

```graphql
query GetInstances($module: String!, $filter: String, $hierarchical: Boolean!) {
  instances(module: $module, filter: $filter, hierarchical: $hierarchical) {
    name
    module
    parent
    path
  }
}
```

**Related:** [get_modules](#get_modules)

---

## get_nets

Get all nets/wires in a specific module.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| module | str | ✅ | - | Module name |
| filter | str | ❌ | None | Filter expression (e.g., "width > 1") |
| hierarchical | bool | ❌ | False | Include nets from sub-instances |

**Returns:** `list[NetInfo]`

| Field | Type | Description |
|-------|------|-------------|
| name | str | Net/wire name |
| width | int | Bit width |
| net_type | str | Net type: "wire", "reg", or "logic" |
| path | str or None | Hierarchical path (if hierarchical=True) |

**Example (Python):**

```python
# Get all nets
nets = client.get_nets("top_module")

# Filter by width
buses = client.get_nets("top_module", filter="width > 1")

# Get all nets in hierarchy
all_nets = client.get_nets("top_module", hierarchical=True)

# Display nets
for net in nets:
    print(f"{net['name']}: {net['net_type']} [{net['width']} bits]")
```

**Example (GraphQL):**

```graphql
query GetNets($module: String!, $filter: String, $hierarchical: Boolean!) {
  nets(module: $module, filter: $filter, hierarchical: $hierarchical) {
    name
    width
    net_type
    path
  }
}
```

**Related:** [get_modules](#get_modules), [add_net](mutations.md#add_net)

---

## Summary Table

Quick reference for all query commands:

| Command | Purpose | Key Parameters | Returns |
|---------|---------|----------------|---------|
| health_check | Check server status | None | HealthCheckResult |
| get_modules | Get all modules | filter, hierarchical | list[ModuleInfo] |
| get_ports | Get module ports | module, filter, hierarchical | list[PortInfo] |
| get_instances | Get module instances | module, filter, hierarchical | list[InstanceInfo] |
| get_nets | Get module nets | module, filter, hierarchical | list[NetInfo] |
