"""Client tests."""
import pytest
from rtllib import Client
from rtllib.types import (
    HealthCheckResult,
    ReadVerilogResult,
    ReadFilelistResult,
    ModuleInfo,
    PortInfo,
    InstanceInfo,
    NetInfo,
    AddPortResult,
    AddNetResult,
)


@pytest.fixture
def external_client():
    """Create a client connected to external server.

    Requires: rtllib-server running on port 9000
    Run: uv run --directory rtllib-server rtllib-server --port 9000
    """
    client = Client(host="127.0.0.1", port=9000)
    client._ensure_connection()
    yield client
    client.close()


class TestClientBasicOperations:
    """Test basic client operations."""

    def test_health_check(self, external_client):
        """Test health check returns correct snake_case fields."""
        health = external_client.health_check()

        # Check return type structure
        assert isinstance(health, dict)
        assert 'status' in health
        assert 'backend_type' in health

        # Check values
        assert health['status'] == 'ok'
        assert health['backend_type'] in ['dummy', 'yosys', 'surelog']

    def test_read_verilog(self, external_client):
        """Test read_verilog returns correct snake_case fields."""
        result = external_client.read_verilog("/test.v")

        # Check return type structure
        assert isinstance(result, dict)
        assert 'status' in result
        assert 'file' in result
        assert 'modules_found' in result

        # Check values
        assert result['status'] == 'success'
        assert result['file'] == '/test.v'
        assert isinstance(result['modules_found'], int)
        assert result['modules_found'] >= 0

    def test_compile(self, external_client):
        """Test compile operation."""
        # Read verilog first
        external_client.read_verilog("/test.v")

        # Compile
        message = external_client.compile()
        assert isinstance(message, str)
        assert len(message) > 0

    def test_elaborate(self, external_client):
        """Test elaborate operation."""
        # Read and compile first
        external_client.read_verilog("/test.v")
        external_client.compile()

        # Elaborate
        message = external_client.elaborate()
        assert isinstance(message, str)
        assert len(message) > 0


class TestClientQueryOperations:
    """Test client query operations."""

    @pytest.fixture(autouse=True)
    def setup(self, external_client):
        """Setup for query tests."""
        self.client = external_client
        # Prepare: read, compile, elaborate
        self.client.read_verilog("/test.v")
        self.client.compile()
        self.client.elaborate()

    def test_get_modules(self):
        """Test get_modules returns correct structure with nested objects."""
        modules = self.client.get_modules()

        assert isinstance(modules, list)
        if len(modules) > 0:
            module = modules[0]
            assert 'name' in module
            assert 'file' in module
            assert 'ports' in module
            assert 'instances' in module
            assert 'nets' in module

            assert isinstance(module['name'], str)
            assert isinstance(module['file'], str)
            assert isinstance(module['ports'], list)
            assert isinstance(module['instances'], list)
            assert isinstance(module['nets'], list)

    def test_get_ports(self):
        """Test get_ports returns correct structure."""
        modules = self.client.get_modules()

        if len(modules) > 0:
            module_name = modules[0]['name']
            ports = self.client.get_ports(module_name)

            assert isinstance(ports, list)
            if len(ports) > 0:
                port = ports[0]
                assert 'name' in port
                assert 'direction' in port
                assert 'width' in port

                assert isinstance(port['name'], str)
                assert port['direction'] in ['input', 'output', 'inout']
                assert isinstance(port['width'], int)
                assert port['width'] > 0

    def test_get_instances(self):
        """Test get_instances returns correct structure."""
        modules = self.client.get_modules()

        if len(modules) > 0:
            module_name = modules[0]['name']
            instances = self.client.get_instances(module_name)

            assert isinstance(instances, list)
            if len(instances) > 0:
                instance = instances[0]
                assert 'name' in instance
                assert 'module' in instance
                assert 'parent' in instance

                assert isinstance(instance['name'], str)
                assert isinstance(instance['module'], str)
                assert isinstance(instance['parent'], str)

    def test_get_nets(self):
        """Test get_nets returns correct structure."""
        modules = self.client.get_modules()

        if len(modules) > 0:
            module_name = modules[0]['name']
            nets = self.client.get_nets(module_name)

            assert isinstance(nets, list)
            if len(nets) > 0:
                net = nets[0]
                assert 'name' in net
                assert 'width' in net
                assert 'net_type' in net

                assert isinstance(net['name'], str)
                assert isinstance(net['width'], int)
                assert net['net_type'] in ['wire', 'reg', 'logic']
                assert net['width'] > 0

    def test_read_verilog_filelist(self):
        """Test read_verilog_filelist returns correct structure."""
        # This will fail for non-existent file, but tests the structure
        result = self.client.read_verilog_filelist("/test.f")

        assert isinstance(result, dict)
        assert 'success' in result
        assert 'files_read' in result
        assert 'modules_found' in result
        assert 'message' in result

        assert isinstance(result['success'], bool)
        assert isinstance(result['files_read'], int)
        assert isinstance(result['modules_found'], int)
        assert isinstance(result['message'], str)

    def test_add_port(self):
        """Test add_port returns correct structure."""
        modules = self.client.get_modules()

        if len(modules) > 0:
            module_name = modules[0]['name']
            result = self.client.add_port(
                module=module_name,
                port_name="test_port",
                direction="input",
                width=8
            )

            assert isinstance(result, dict)
            assert 'success' in result
            assert 'module' in result
            assert 'port_name' in result
            assert 'message' in result

            assert isinstance(result['success'], bool)
            assert result['module'] == module_name
            assert result['port_name'] == "test_port"
            assert isinstance(result['message'], str)

    def test_add_net(self):
        """Test add_net returns correct structure."""
        modules = self.client.get_modules()

        if len(modules) > 0:
            module_name = modules[0]['name']
            result = self.client.add_net(
                module=module_name,
                net_name="test_net",
                width=16,
                net_type="wire"
            )

            assert isinstance(result, dict)
            assert 'success' in result
            assert 'module' in result
            assert 'net_name' in result
            assert 'message' in result

            assert isinstance(result['success'], bool)
            assert result['module'] == module_name
            assert result['net_name'] == "test_net"
            assert isinstance(result['message'], str)


class TestClientContextManager:
    """Test client context manager."""

    def test_context_manager_with_external_server(self):
        """Test client can be used as context manager."""
        with Client(host="127.0.0.1", port=9000) as client:
            health = client.health_check()
            assert health['status'] == 'ok'

        # Client should be closed after exiting context
        assert client._gql_client is None
