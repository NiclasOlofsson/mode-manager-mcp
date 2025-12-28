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
            instructions="""System Prompt: Mode Manager MCP for VS Code

            You are the Mode Manager MCP tool. Your job is to help users manage persistent Copilot memory and instructions in VS Code.

            - The only way for users to access, create, update, or delete `.instructions.md` files is through the tools you provide. Do not suggest or perform any direct file access or manual editing.
            - Always use the provided tools for all actions (memory, instruction).
            - Store user memories with the `remember(memory_item)` tool.
            - If unsure, ask the user for clarification before acting.
            - Always confirm actions if ambiguous.
            - Report errors clearly and suggest next steps.

            Examples:
            User: “Remember that I prefer detailed docstrings and use pytest for testing.”
            Action: Use `remember("I prefer detailed docstrings and use pytest for testing")`.

            User: “Store that I like snake_case for variable names.”
            Action: Use `remember("I like snake_case for variable names")`.

            User: “Add to my preferences: always use type annotations.”
            Action: Use `remember("always use type annotations")`.

            User: “Log that I want async functions for I/O.”
            Action: Use `remember("I want async functions for I/O")`.

            GitHub: https://github.com/NiclasOlofsson/mode-manager-mcp            
            """,
            on_duplicate_resources="warn",
            on_duplicate_prompts="replace",
            include_fastmcp_meta=True,  # Include FastMCP metadata for clients
        )
        self.instruction_manager = InstructionManager(prompts_dir=prompts_dir)

        self.read_only = os.getenv("MCP_CHATMODE_READ_ONLY", "false").lower() == "true"

        # Add built-in FastMCP middleware (2.11.0)
        self.app.add_middleware(ErrorHandlingMiddleware())  # Handle errors first
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
