# Installation

## Requirements

- **Python**: 3.10 (3.11 not currently supported)
- **Operating System**: Linux, macOS, or Windows with WSL
- **rtllib-server**: GraphQL server (Python or binary)

## Install Client SDK

### Using pip

```bash
pip install rtllib
```

### Using uv (Recommended)

```bash
uv pip install rtllib
```

### From Source

```bash
git clone https://github.com/kwonah0/rtllib.git
cd rtllib
uv sync
```

## Install Server

The rtllib client requires an rtllib-server to connect to.

### Option 1: Auto-start Python Server (Easiest)

The client can automatically start the server if you have rtllib-server installed:

```bash
# Install server package
pip install rtllib-server

# Client will auto-start it
from rtllib import Client
client = Client(auto_start=True)  # default
```

### Option 2: Use Pre-built Binary

Download the rtllib-server binary and specify the path:

```python
client = Client(
    server_mode="binary",
    binary_path="/path/to/rtllib-server"
)
```

### Option 3: External Server

Start the server manually and connect to it:

```bash
# Terminal 1: Start server
rtllib-server --port 8000

# Terminal 2: Connect from Python
client = Client(host="127.0.0.1", port=8000, auto_start=False)
```

## Verify Installation

```python
from rtllib import Client

# Test connection
with Client() as client:
    health = client.health_check()
    print(health)
    # {'status': 'ok', 'backend_type': 'dummy'}
```

## Configuration

Default configuration file: `~/.rtllib/settings.toml` or project root

```toml
[default]
server_mode = "python"  # or "binary"
auto_start = true

[default.server]
host = "127.0.0.1"
port = 5000  # auto-assigned if not specified

[default.timeouts]
startup = 20
health_check = 10
request = 30
```

## Environment Variables

Override settings with environment variables:

```bash
export RTLLIB_SERVER_MODE=binary
export RTLLIB_BINARY_PATH=/path/to/rtllib-server
export RTLLIB_AUTO_START=true
```

## Troubleshooting

### Import Error

```python
ModuleNotFoundError: No module named 'rtllib'
```

**Solution**: Ensure rtllib is installed in your current Python environment:
```bash
pip list | grep rtllib
```

### Server Connection Error

```
ConnectionError: Failed to connect to server
```

**Solutions**:
- Check if server is running: `ps aux | grep rtllib-server`
- Try manual server start: `rtllib-server --port 8000`
- Check port availability: `lsof -i :5000`

### Port Already in Use

```
OSError: [Errno 98] Address already in use
```

**Solution**: Let the client auto-assign a free port:
```python
client = Client(port=None)  # auto-assign
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [Command Reference](commands/queries.md) - Learn all available commands
