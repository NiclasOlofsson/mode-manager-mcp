"""
Mode Manager MCP Server Implementation.

This server provides tools for managing VS Code .instructions.md files
which define custom instructions for GitHub Copilot.
"""

import logging
import os
from typing import Optional

from fastmcp import FastMCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware

from .instruction_manager import InstructionManager
from .server_registry import ServerRegistry
from .tools import register_all_tools

logger = logging.getLogger(__name__)


class ModeManagerServer:
    """
    Mode Manager MCP Server.

    Provides tools for managing VS Code .instructions.md files.
    """

    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize the server.

        Args:
            prompts_dir: Custom prompts directory for all managers (optional)
        """
        # FastMCP initialization with recommended arguments
        from . import __version__

        self.app = FastMCP(
            version=__version__,
            name="Mode Manager MCP",
            instructions="""Persistent Copilot Memory for VS Code (2025+).

            GitHub Repository: https://github.com/NiclasOlofsson/mode-manager-mcp

            Game-Changer for 2025:
            - Copilot now loads instructions with every chat message, not just at session start.
            - Your memories and preferences are ALWAYS active in every conversation, across sessions, topics, and projects.

            Main Feature:
            - Store your work context, coding preferences, and workflow details using the remember(memory_item) tool.

            How It Works:
            - Auto-setup: Creates memory.instructions.md in your VS Code prompts directory on first use.
            - Smart storage: Each memory is timestamped and organized for easy retrieval.
            - Always loaded: VS Code includes your memories in every chat request.

            Additional Capabilities:
            - Manage and organize .instructions.md files.
            - AI-powered memory optimization to consolidate and organize your memories.

            Usage Example:
            - Ask Copilot: "Remember that I prefer detailed docstrings and use pytest for testing"
            - Copilot will remember this across all future conversations.
            """,
            on_duplicate_resources="warn",
            on_duplicate_prompts="replace",
            include_fastmcp_meta=True,  # Include FastMCP metadata for clients
        )
        self.instruction_manager = InstructionManager(prompts_dir=prompts_dir)

        self.read_only = os.getenv("MCP_CHATMODE_READ_ONLY", "false").lower() == "true"

        # Add built-in FastMCP middleware (2.11.0)
        self.app.add_middleware(ErrorHandlingMiddleware())  # Handle errors first
        self.app.add_middleware(RateLimitingMiddleware(max_requests_per_second=50))
        self.app.add_middleware(TimingMiddleware())  # Time actual execution
        self.app.add_middleware(LoggingMiddleware(include_payloads=True, max_payload_length=1000))

        # Initialize the singleton server registry
        registry = ServerRegistry.get_instance()
        registry.initialize(
            app=self.app,
            instruction_manager=self.instruction_manager,
            read_only=self.read_only,
        )

        # Register all tools from separate modules
        register_all_tools()

        logger.info("Mode Manager MCP Server initialized")
        if self.read_only:
            logger.info("Running in READ-ONLY mode")

    def run(self) -> None:
        self.app.run()


def create_server() -> ModeManagerServer:
    return ModeManagerServer()
