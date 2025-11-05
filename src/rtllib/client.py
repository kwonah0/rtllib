"""RTL Library Client SDK."""

import logging
from typing import Optional, Callable
from gql import gql, Client as GQLClient
from gql.transport.httpx import HTTPXTransport

from rtllib.server_manager import ServerManager
from rtllib.config import settings
from rtllib.types import (
    ModuleInfo,
    InstanceInfo,
    PortInfo,
    NetInfo,
    ReadVerilogResult,
    ReadFilelistResult,
    AddPortResult,
    AddNetResult,
    HealthCheckResult,
)
from rtllib.log_stream import LogStreamClient

logger = logging.getLogger(__name__)


class Client:
    """RTL Library Client for communicating with the server."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        auto_start: Optional[bool] = None,
        server_mode: Optional[str] = None,
    ):
        """Initialize the client.

        Args:
            host: Server host (defaults to config)
            port: Server port, None for auto-assign (defaults to config)
            auto_start: Auto-start server if True (defaults to config)
            server_mode: "python" or "binary" (defaults to config)
        """
        self._auto_start = auto_start if auto_start is not None else settings.auto_start
        self._server_manager: Optional[ServerManager] = None
        self._gql_client: Optional[GQLClient] = None
        self._log_stream_client: Optional[LogStreamClient] = None
        self._external_server = False

        # If host and port provided, assume external server
        if host is not None and port is not None:
            self._external_server = True
            self.host = host
            self.port = port
        else:
            # Will be set by server manager
            self.host = host or settings.server.host
            self.port = port if port is not None else getattr(settings.server, "port", None)

            if self._auto_start:
                self._server_manager = ServerManager(
                    server_mode=server_mode,
                    host=self.host,
                    port=self.port,
                )

    def _ensure_connection(self) -> None:
        """Ensure connection to server is established."""
        if self._gql_client is not None:
            return

        # Start server if needed
        if self._server_manager and not self._server_manager.is_running():
            self.host, self.port = self._server_manager.start()

        # Create GraphQL client
        url = f"http://{self.host}:{self.port}/graphql"
        logger.info(f"Connecting to server at {url}")

        transport = HTTPXTransport(url=url, timeout=settings.timeouts.request)
        self._gql_client = GQLClient(transport=transport, fetch_schema_from_transport=False)

    def health_check(self) -> HealthCheckResult:
        """Check server health.

        Returns:
            HealthCheckResult: Health check result
        """
        self._ensure_connection()

        query = gql("""
            query {
                health_check {
                    status
                    backend_type
                }
            }
        """)

        result = self._gql_client.execute(query)
        return result["health_check"]

    def read_verilog(self, path: str) -> ReadVerilogResult:
        """Read and parse a Verilog file.

        Args:
            path: Path to the Verilog file

        Returns:
            ReadVerilogResult: Result of the operation
        """
        self._ensure_connection()

        mutation = gql("""
            mutation ReadVerilog($path: String!) {
                read_verilog(path: $path) {
                    status
                    file
                    modules_found
                }
            }
        """)

        result = self._gql_client.execute(mutation, variable_values={"path": path})
        return result["read_verilog"]

    def compile(self) -> str:
        """Compile the loaded Verilog code.

        Returns:
            str: Result message
        """
        self._ensure_connection()

        mutation = gql("""
            mutation {
                compile
            }
        """)

        result = self._gql_client.execute(mutation)
        return result["compile"]

    def elaborate(self) -> str:
        """Elaborate the compiled design.

        Returns:
            str: Result message
        """
        self._ensure_connection()

        mutation = gql("""
            mutation {
                elaborate
            }
        """)

        result = self._gql_client.execute(mutation)
        return result["elaborate"]

    def get_modules(
        self,
        filter: Optional[str] = None,
        hierarchical: bool = False
    ) -> list[ModuleInfo]:
        """Get all modules in the design.

        Args:
            filter: Optional filter expression (backend-specific)
            hierarchical: If True, include hierarchical instances as flat list with paths

        Returns:
            list[ModuleInfo]: List of module information with nested objects
        """
        self._ensure_connection()

        query = gql("""
            query GetModules($filter: String, $hierarchical: Boolean!) {
                modules(filter: $filter, hierarchical: $hierarchical) {
                    name
                    file
                    path
                    ports {
                        name
                        direction
                        width
                        path
                    }
                    instances {
                        name
                        module
                        parent
                        path
                    }
                    nets {
                        name
                        width
                        net_type
                        path
                    }
                }
            }
        """)

        result = self._gql_client.execute(query, variable_values={
            "filter": filter,
            "hierarchical": hierarchical
        })
        return result["modules"]

    def get_instances(
        self,
        module: str,
        filter: Optional[str] = None,
        hierarchical: bool = False
    ) -> list[InstanceInfo]:
        """Get all instances in a specific module.

        Args:
            module: Name of the module
            filter: Optional filter expression (backend-specific)
            hierarchical: If True, include instances from sub-hierarchy

        Returns:
            list[InstanceInfo]: List of instance information
        """
        self._ensure_connection()

        query = gql("""
            query GetInstances($module: String!, $filter: String, $hierarchical: Boolean!) {
                instances(module: $module, filter: $filter, hierarchical: $hierarchical) {
                    name
                    module
                    parent
                    path
                }
            }
        """)

        result = self._gql_client.execute(query, variable_values={
            "module": module,
            "filter": filter,
            "hierarchical": hierarchical
        })
        return result["instances"]

    def get_ports(
        self,
        module: str,
        filter: Optional[str] = None,
        hierarchical: bool = False
    ) -> list[PortInfo]:
        """Get all ports of a specific module.

        Args:
            module: Name of the module
            filter: Optional filter expression (backend-specific)
            hierarchical: If True, include ports from sub-instances

        Returns:
            list[PortInfo]: List of port information
        """
        self._ensure_connection()

        query = gql("""
            query GetPorts($module: String!, $filter: String, $hierarchical: Boolean!) {
                ports(module: $module, filter: $filter, hierarchical: $hierarchical) {
                    name
                    direction
                    width
                    path
                }
            }
        """)

        result = self._gql_client.execute(query, variable_values={
            "module": module,
            "filter": filter,
            "hierarchical": hierarchical
        })
        return result["ports"]

    def get_nets(
        self,
        module: str,
        filter: Optional[str] = None,
        hierarchical: bool = False
    ) -> list[NetInfo]:
        """Get all nets/wires in a specific module.

        Args:
            module: Name of the module
            filter: Optional filter expression (backend-specific)
            hierarchical: If True, include nets from sub-instances

        Returns:
            list[NetInfo]: List of net information
        """
        self._ensure_connection()

        query = gql("""
            query GetNets($module: String!, $filter: String, $hierarchical: Boolean!) {
                nets(module: $module, filter: $filter, hierarchical: $hierarchical) {
                    name
                    width
                    net_type
                    path
                }
            }
        """)

        result = self._gql_client.execute(query, variable_values={
            "module": module,
            "filter": filter,
            "hierarchical": hierarchical
        })
        return result["nets"]

    def read_verilog_filelist(self, filelist_path: str) -> ReadFilelistResult:
        """Read multiple Verilog files from a filelist.

        The filelist should follow Verilog standard format, supporting:
        - File paths (one per line)
        - Comments (# and //)
        - Options like +incdir+, -v, -y

        Args:
            filelist_path: Path to the filelist file

        Returns:
            ReadFilelistResult: Result of the operation
        """
        self._ensure_connection()

        mutation = gql("""
            mutation ReadVerilogFilelist($filelist_path: String!) {
                read_verilog_filelist(filelist_path: $filelist_path) {
                    success
                    files_read
                    modules_found
                    message
                }
            }
        """)

        result = self._gql_client.execute(mutation, variable_values={"filelist_path": filelist_path})
        return result["read_verilog_filelist"]

    def add_port(
        self,
        module: str,
        port_name: str,
        direction: str,
        width: int
    ) -> AddPortResult:
        """Add a port to a module (session-based modification).

        Args:
            module: Name of the module
            port_name: Name of the port to add
            direction: Port direction ("input", "output", "inout")
            width: Bit width of the port

        Returns:
            AddPortResult: Result of the operation
        """
        self._ensure_connection()

        mutation = gql("""
            mutation AddPort($module: String!, $port_name: String!, $direction: String!, $width: Int!) {
                add_port(module: $module, port_name: $port_name, direction: $direction, width: $width) {
                    success
                    module
                    port_name
                    message
                }
            }
        """)

        result = self._gql_client.execute(mutation, variable_values={
            "module": module,
            "port_name": port_name,
            "direction": direction,
            "width": width
        })
        return result["add_port"]

    def add_net(
        self,
        module: str,
        net_name: str,
        width: int,
        net_type: str = "wire"
    ) -> AddNetResult:
        """Add a net/wire to a module (session-based modification).

        Args:
            module: Name of the module
            net_name: Name of the net to add
            width: Bit width of the net
            net_type: Type of the net ("wire", "reg", "logic")

        Returns:
            AddNetResult: Result of the operation
        """
        self._ensure_connection()

        mutation = gql("""
            mutation AddNet($module: String!, $net_name: String!, $width: Int!, $net_type: String!) {
                add_net(module: $module, net_name: $net_name, width: $width, net_type: $net_type) {
                    success
                    module
                    net_name
                    message
                }
            }
        """)

        result = self._gql_client.execute(mutation, variable_values={
            "module": module,
            "net_name": net_name,
            "width": width,
            "net_type": net_type
        })
        return result["add_net"]

    def start_log_streaming(self, log_callback: Optional[Callable[[dict], None]] = None) -> None:
        """Start streaming logs from the server in real-time.

        This runs in a background thread and does not block sync operations.
        Logs will be received asynchronously while you continue to use other client methods.

        Args:
            log_callback: Optional callback function to handle log messages.
                         Function receives a dict with keys: level, message, timestamp.
                         If None, logs will be printed to stdout.

        Example:
            >>> def my_log_handler(log_data):
            ...     print(f"[{log_data['level']}] {log_data['message']}")
            >>> client.start_log_streaming(my_log_handler)
            >>> # Continue with normal operations while logs stream in background
            >>> client.compile()
        """
        self._ensure_connection()

        if self._log_stream_client and self._log_stream_client.is_running():
            logger.warning("Log streaming is already active")
            return

        self._log_stream_client = LogStreamClient(
            host=self.host,
            port=self.port,
            log_callback=log_callback,
        )
        self._log_stream_client.start()
        logger.info("Log streaming started")

    def stop_log_streaming(self) -> None:
        """Stop the log streaming."""
        if self._log_stream_client:
            self._log_stream_client.stop()
            self._log_stream_client = None
            logger.info("Log streaming stopped")

    def is_log_streaming_active(self) -> bool:
        """Check if log streaming is currently active.

        Returns:
            bool: True if log streaming is running
        """
        return self._log_stream_client is not None and self._log_stream_client.is_running()

    def close(self) -> None:
        """Close the client and stop the server if managed."""
        # Stop log streaming if active
        if self._log_stream_client:
            self.stop_log_streaming()

        if self._gql_client:
            self._gql_client = None

        if self._server_manager:
            self._server_manager.stop()

    def __enter__(self):
        """Context manager entry."""
        self._ensure_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
