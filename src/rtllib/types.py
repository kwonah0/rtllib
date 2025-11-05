"""Type definitions for RTL library client."""

from typing import TypedDict
from typing_extensions import NotRequired


class PortInfo(TypedDict):
    """Information about a module port."""

    name: str
    direction: str
    width: int
    path: NotRequired[str]


class InstanceInfo(TypedDict):
    """Information about a module instance."""

    name: str
    module: str
    parent: str
    path: NotRequired[str]


class NetInfo(TypedDict):
    """Information about a net/wire."""

    name: str
    width: int
    net_type: str
    path: NotRequired[str]


class ModuleInfo(TypedDict):
    """Information about a Verilog module with nested objects."""

    name: str
    file: str
    ports: list[PortInfo]
    instances: list[InstanceInfo]
    nets: list[NetInfo]
    path: NotRequired[str]


class ReadVerilogResult(TypedDict):
    """Result of reading a Verilog file."""

    status: str
    file: str
    modules_found: int


class ReadFilelistResult(TypedDict):
    """Result of reading a Verilog filelist."""

    success: bool
    files_read: int
    modules_found: int
    message: str


class AddPortResult(TypedDict):
    """Result of adding a port to a module."""

    success: bool
    module: str
    port_name: str
    message: str


class AddNetResult(TypedDict):
    """Result of adding a net to a module."""

    success: bool
    module: str
    net_name: str
    message: str


class HealthCheckResult(TypedDict):
    """Health check result."""

    status: str
    backend_type: str


class LogData(TypedDict):
    """Log data from server log streaming."""

    level: str
    message: str
    timestamp: str
