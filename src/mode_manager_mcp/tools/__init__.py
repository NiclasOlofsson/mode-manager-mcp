"""Tool registration modules for Mode Manager MCP Server."""

from .instruction_tools import register_instruction_tools
from .memory_tools import register_memory_tools
from .remember_tools import register_remember_tools

__all__ = [
    "register_instruction_tools",
    "register_memory_tools",
    "register_remember_tools",
]


def register_all_tools() -> None:
    """Register all tools with the server."""
    register_instruction_tools()
    register_memory_tools()
    register_remember_tools()
