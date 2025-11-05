"""Client-side log streaming functionality."""

import asyncio
import logging
from typing import Optional, Callable
import threading

from gql import gql, Client as GqlClient
from gql.transport.websockets import WebsocketsTransport

logger = logging.getLogger(__name__)


class LogStreamClient:
    """Client for receiving real-time log streams from the server."""

    def __init__(self, host: str, port: int, log_callback: Optional[Callable[[dict], None]] = None):
        """Initialize the log stream client.

        Args:
            host: Server host
            port: Server port
            log_callback: Optional callback function to handle log messages.
                         If None, logs will be printed to stdout.
        """
        self.host = host
        self.port = port
        self.log_callback = log_callback or self._default_log_handler
        self._ws_url = f"ws://{host}:{port}/graphql"
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def _default_log_handler(self, log_data: dict) -> None:
        """Default log handler that prints to stdout.

        Args:
            log_data: Log message data with keys: level, message, timestamp
        """
        level = log_data.get("level", "INFO")
        message = log_data.get("message", "")
        timestamp = log_data.get("timestamp", "")
        print(f"[{timestamp}] [{level}] {message}")

    async def _stream_logs(self) -> None:
        """Async function to stream logs from the server."""
        transport = WebsocketsTransport(url=self._ws_url)

        try:
            async with GqlClient(
                transport=transport,
                fetch_schema_from_transport=False,
            ) as session:
                subscription = gql("""
                    subscription {
                        log_stream {
                            level
                            message
                            timestamp
                        }
                    }
                """)

                logger.info("Log streaming started")

                try:
                    async for result in session.subscribe(subscription):
                        if not self._running:
                            break

                        log_data = result.get("log_stream", {})
                        if log_data:
                            # Call the callback in a thread-safe way
                            self.log_callback(log_data)
                except asyncio.CancelledError:
                    logger.info("Log streaming cancelled")
                    raise
                except Exception as e:
                    if self._running:  # Only log error if not intentionally stopped
                        logger.error(f"Error in log streaming: {e}")
        finally:
            logger.info("Log streaming stopped")

    def _run_in_thread(self) -> None:
        """Run the async log streaming in a separate event loop."""
        loop = asyncio.new_event_loop()
        self._loop = loop
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._stream_logs())
        finally:
            # Clean up the loop
            try:
                loop.close()
            except Exception:
                pass  # Ignore errors during cleanup
            self._loop = None

    def start(self) -> None:
        """Start the log streaming in a background thread."""
        if self._running:
            logger.warning("Log streaming already running")
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_in_thread, daemon=True)
        self._thread.start()
        logger.info("Log streaming thread started")

    def stop(self) -> None:
        """Stop the log streaming."""
        if not self._running:
            return

        logger.info("Stopping log streaming...")
        self._running = False

        # Wait for thread to finish gracefully
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
            self._thread = None

        self._loop = None
        logger.info("Log streaming stopped")

    def is_running(self) -> bool:
        """Check if log streaming is running.

        Returns:
            bool: True if streaming is active
        """
        return self._running

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
