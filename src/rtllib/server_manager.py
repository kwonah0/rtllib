"""Server process management."""

import socket
import subprocess
import time
import logging
from pathlib import Path
from typing import Optional
import httpx

from rtllib.config import settings

logger = logging.getLogger(__name__)


class ServerManager:
    """Manages the RTL library server process."""

    def __init__(
        self,
        server_mode: Optional[str] = None,
        binary_path: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ):
        """Initialize server manager.

        Args:
            server_mode: "python" or "binary" (defaults to config)
            binary_path: Path to server binary (defaults to config)
            host: Host to bind server to (defaults to config)
            port: Port to bind server to, None for auto-assign (defaults to config)
        """
        self.server_mode = server_mode or settings.server_mode
        self.binary_path = binary_path or settings.binary_path
        self.host = host or settings.server.host
        self.port = port if port is not None else getattr(settings.server, "port", None)

        self.process: Optional[subprocess.Popen] = None
        self._started = False

    def find_free_port(self) -> int:
        """Find a free port on localhost.

        Returns:
            int: Available port number
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.listen(1)
            port = s.getsockname()[1]
        logger.info(f"Found free port: {port}")
        return port

    def start(self) -> tuple[str, int]:
        """Start the server process.

        Returns:
            tuple: (host, port) where the server is running

        Raises:
            RuntimeError: If server fails to start
        """
        if self._started:
            logger.warning("Server already started")
            return self.host, self.port

        # Auto-assign port if not specified
        if self.port is None:
            self.port = self.find_free_port()

        # Build command based on mode
        if self.server_mode == "python":
            # Find rtllib-server package
            # In development, we assume it's in a sibling directory
            server_path = Path(__file__).parent.parent.parent.parent / "rtllib-server"
            if server_path.exists():
                cmd = [
                    "uv",
                    "run",
                    "--directory",
                    str(server_path),
                    "rtllib-server",
                    "--host",
                    self.host,
                    "--port",
                    str(self.port),
                ]
            else:
                # Try installed package
                cmd = [
                    "rtllib-server",
                    "--host",
                    self.host,
                    "--port",
                    str(self.port),
                ]
        elif self.server_mode == "binary":
            cmd = [
                self.binary_path,
                "--host",
                self.host,
                "--port",
                str(self.port),
            ]
        else:
            raise ValueError(f"Unknown server mode: {self.server_mode}")

        logger.info(f"Starting server: {' '.join(cmd)}")

        try:
            # Create log files for debugging
            import tempfile
            self._stdout_file = tempfile.NamedTemporaryFile(
                mode='w+',
                prefix='rtllib_server_stdout_',
                suffix='.log',
                delete=False
            )
            self._stderr_file = tempfile.NamedTemporaryFile(
                mode='w+',
                prefix='rtllib_server_stderr_',
                suffix='.log',
                delete=False
            )

            logger.info(f"Server stdout: {self._stdout_file.name}")
            logger.info(f"Server stderr: {self._stderr_file.name}")

            self.process = subprocess.Popen(
                cmd,
                stdout=self._stdout_file,
                stderr=self._stderr_file,
            )
            self._started = True
            logger.info(f"Server process started with PID: {self.process.pid}")

            # Wait for server to be ready
            if not self._wait_for_ready():
                self.stop()
                raise RuntimeError("Server failed to become ready")

            logger.info(f"Server ready at {self.host}:{self.port}")
            return self.host, self.port

        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise RuntimeError(f"Failed to start server: {e}") from e

    def _wait_for_ready(self) -> bool:
        """Wait for server to be ready.

        Returns:
            bool: True if server is ready, False otherwise
        """
        timeout = settings.timeouts.startup
        start_time = time.time()
        url = f"http://{self.host}:{self.port}/health"

        logger.info(f"Waiting for server to be ready at {url}")

        # Give server time to initialize before first check
        logger.info("Initial wait for server initialization (3 seconds)...")
        time.sleep(3)

        attempt = 0
        while time.time() - start_time < timeout:
            attempt += 1

            # Check if process is still running
            if self.process and self.process.poll() is not None:
                logger.error("Server process terminated unexpectedly")
                logger.error(f"Check logs: {getattr(self, '_stderr_file', None)}")
                return False

            try:
                logger.debug(f"Health check attempt {attempt}")
                response = httpx.get(url, timeout=2.0)
                if response.status_code == 200:
                    logger.info(f"Server is ready (after {attempt} attempts)")
                    return True
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                logger.debug(f"Attempt {attempt} failed: {e}")
                pass

            time.sleep(1.0)  # Increased from 0.5s to 1.0s

        logger.error(f"Server did not become ready within {timeout} seconds")
        return False

    def stop(self) -> None:
        """Stop the server process."""
        if not self._started or not self.process:
            return

        logger.info(f"Stopping server (PID: {self.process.pid})")

        try:
            self.process.terminate()
            self.process.wait(timeout=5)
            logger.info("Server stopped gracefully")
        except subprocess.TimeoutExpired:
            logger.warning("Server did not stop gracefully, killing...")
            self.process.kill()
            self.process.wait()
            logger.info("Server killed")
        finally:
            self.process = None
            self._started = False

            # Clean up log files
            if hasattr(self, '_stdout_file'):
                try:
                    self._stdout_file.close()
                    import os
                    os.unlink(self._stdout_file.name)
                except Exception:
                    pass

            if hasattr(self, '_stderr_file'):
                try:
                    self._stderr_file.close()
                    import os
                    os.unlink(self._stderr_file.name)
                except Exception:
                    pass

    def is_running(self) -> bool:
        """Check if server is running.

        Returns:
            bool: True if server is running
        """
        return self._started and self.process and self.process.poll() is None

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
