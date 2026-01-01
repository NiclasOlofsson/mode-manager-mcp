"""
Memory Optimization Implementation with Full Backward Compatibility.

This implementation gracefully handles existing memory files without metadata
and gradually migrates them to the new enhanced format.
"""

import datetime
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import tiktoken
from fastmcp import Context

from .simple_file_ops import (
    is_in_git_repository,
    parse_frontmatter,
    parse_frontmatter_file,
    write_frontmatter_file,
)

logger = logging.getLogger(__name__)


class MemoryOptimizer:
    """Handles memory file optimization with full backward compatibility."""

    def __init__(self, instruction_manager: Any) -> None:
        self.instruction_manager = instruction_manager

    def _get_memory_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract or initialize metadata for a memory file.

        Handles backward compatibility by providing defaults for missing metadata.
        """
        try:
            frontmatter, _ = parse_frontmatter_file(file_path)

            # Provide backward-compatible defaults for missing metadata
            metadata = {
                "lastOptimized": frontmatter.get("lastOptimized"),
                "entryCount": frontmatter.get("entryCount", 0),
                "optimizationVersion": frontmatter.get("optimizationVersion", 0),
                "autoOptimize": frontmatter.get("autoOptimize", True),  # Default to enabled
                "lastOptimizedTokenCount": frontmatter.get("lastOptimizedTokenCount", 0),  # Critical for token growth check
                "tokenGrowthThreshold": frontmatter.get("tokenGrowthThreshold", 1.20),  # Default 20% growth
            }

            return metadata

        except Exception as e:
            logger.warning(f"Could not read metadata from {file_path}: {e}")
            # Return safe defaults for corrupted files
            return {
                "lastOptimized": None,
                "entryCount": 0,
                "optimizationVersion": 0,
                "autoOptimize": True,
                "lastOptimizedTokenCount": 0,
                "tokenGrowthThreshold": 1.20,
            }

    def _count_memory_entries(self, content: str) -> int:
        """
        Count memory entries in the content.

        Handles various formats:
        - **timestamp:** content
        - - timestamp: content
        - timestamp: content (without dashes)
        """
        patterns = [
            r"^\s*-\s*\*\*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\*\*:.*$",  # - **2025-08-09 10:30:** content
            r"^\s*-\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:.*$",  # - 2025-08-09 10:30: content
            r"^\s*\*\*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\*\*:.*$",  # **2025-08-09 10:30:** content (no dash)
            r"^\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:.*$",  # 2025-08-09 10:30: content (no formatting)
        ]

        total_count = 0
        lines = content.split("\n")

        for pattern in patterns:
            count = len([line for line in lines if re.match(pattern, line, re.MULTILINE)])
            total_count = max(total_count, count)  # Use the highest count found

        # Fallback: count lines starting with "- **" (most common format)
        if total_count == 0:
            fallback_count = len([line for line in lines if line.strip().startswith("- **")])
            total_count = fallback_count

        return total_count

    def _count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken (cl100k_base encoding).

        This provides accurate token counts for Claude and GPT models.
        """
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"Token counting failed, falling back to character estimate: {e}")
            # Rough fallback: ~4 chars per token
            return len(text) // 4

    def _should_optimize_memory(self, file_path: Path, metadata: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Determine if memory file should be optimized.

        Returns (should_optimize, reason)
        """
        # Check if auto-optimization is disabled
        if not metadata.get("autoOptimize", True):
            return False, "Auto-optimization disabled"

        # Token growth check
        try:
            frontmatter, content = parse_frontmatter_file(file_path)
            # Count tokens in the full file (frontmatter + content)
            full_content = "---\n"
            for key, value in frontmatter.items():
                if isinstance(value, str) and ('"' in value or "'" in value):
                    full_content += f'{key}: "{value}"\n'
                else:
                    full_content += f"{key}: {value}\n"
            full_content += f"---\n{content}"
            current_tokens = self._count_tokens(full_content)

            # Get last optimization token count
            last_optimized_tokens = metadata.get("lastOptimizedTokenCount", 0)

            if last_optimized_tokens == 0:
                # No previous optimization - this is a legacy file
                return True, f"No previous optimization recorded (current: {current_tokens} tokens)"

            # Check token growth threshold (default 20%)
            token_growth_threshold = metadata.get("tokenGrowthThreshold", 1.20)
            threshold_tokens = int(last_optimized_tokens * token_growth_threshold)

            if current_tokens > threshold_tokens:
                growth_percent = ((current_tokens - last_optimized_tokens) / last_optimized_tokens) * 100
                return True, f"Token count ({current_tokens}) exceeds threshold ({threshold_tokens}), {growth_percent:.1f}% growth"

        except Exception as e:
            logger.warning(f"Could not count tokens: {e}")
            return True, "Token counting failed, triggering optimization"

        return False, "Token growth below threshold"

    def _update_metadata(self, file_path: Path, content: Optional[str] = None) -> bool:
        """
        Update metadata in a memory file's frontmatter.

        Gracefully handles files with or without existing metadata.
        """
        try:
            frontmatter, body_content = parse_frontmatter_file(file_path)

            # Count current entries and tokens
            entry_count = self._count_memory_entries(body_content)

            # Count tokens in full content
            full_content = "---\n"
            for key, value in frontmatter.items():
                if isinstance(value, str) and ('"' in value or "'" in value):
                    full_content += f'{key}: "{value}"\n'
                else:
                    full_content += f"{key}: {value}\n"
            full_content += f"---\n{body_content}"
            current_tokens = self._count_tokens(full_content)

            # Update metadata while preserving existing frontmatter
            frontmatter.update(
                {
                    "lastOptimized": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "entryCount": entry_count,
                    "optimizationVersion": frontmatter.get("optimizationVersion", 0) + 1,
                    "lastOptimizedTokenCount": current_tokens,
                }
            )

            # Set defaults for new metadata fields if they don't exist
            if "autoOptimize" not in frontmatter:
                frontmatter["autoOptimize"] = True
            if "tokenGrowthThreshold" not in frontmatter:
                frontmatter["tokenGrowthThreshold"] = 1.20  # 20% growth

            # Migrate old fields: remove deprecated byte/entry/time thresholds
            for old_field in ["sizeThreshold", "entryThreshold", "timeThreshold"]:
                frontmatter.pop(old_field, None)

            # Use provided content or keep existing body
            final_content = content if content else body_content

            return write_frontmatter_file(file_path, frontmatter, final_content, create_backup=True)

        except Exception as e:
            logger.error(f"Failed to update metadata for {file_path}: {e}")
            return False

    async def _optimize_memory_with_ai(self, ctx: Context, content: str) -> Optional[str]:
        """Safely optimize memory content using AI sampling with comprehensive error handling."""
        try:
            response = await ctx.sample(
                f"""Please optimize this AI memory file by following these guidelines:

**CRITICAL RULES:**
1. **Preserve ALL information** - Never delete memories, facts, or important details
2. **Maintain all timestamps** - Keep original dates for traceability (format: **YYYY-MM-DD HH:MM**)
3. **Preserve frontmatter** - Keep the YAML header intact with all metadata

**ORGANIZATION (use this exact order):**
1. ## Universal Laws - Immutable procedural rules (numbered):
   - Multi-step workflows and protocols (e.g., "Before X, always do Y")
   - Mandatory execution sequences (e.g., "run format, typecheck, test in order")
   - Complex behavioral requirements with conditions
   - Error prevention mechanisms and safety checks
   - Cross-cutting requirements that affect multiple areas

2. ## Policies - Standards, constraints, and guidelines:
   - Tool and technology choices (e.g., "Use X for Y")
   - File organization and placement rules
   - Code style and formatting requirements
   - Simple prohibitions (e.g., "Never commit X")
   - Best practices and conventions

3. ## Personal Context - Name, location, role, background
4. ## Professional Context - Company, team, tools, methodology, focus areas
5. ## Technical Preferences - Languages, stack, IDEs, coding style, problem-solving approach
6. ## Communication Preferences - Style, information needs, feedback preferences
7. ## Suggestions/Hints - Recommendations and tips (optional section)
8. ## Memories/Facts - Organize into logical subsections by topic (e.g., "### Python Standards", "### KQL Guidelines", "### Project-Specific Patterns")

**CONSOLIDATION RULES:**
- Merge identical or nearly identical entries (preserve newest timestamp)
- Group related memories under descriptive subsections (### Topic Name)
- Keep distinct facts separate even if related
- Consolidate scattered information about the same topic

**FORMATTING STANDARDS:**
- Use `code blocks` for commands, paths, and technical terms
- Use **bold** for emphasis on key terms
- Use bullet points (-) for lists under each section
- Preserve code blocks in memories (```language ... ```)
- Ensure consistent indentation and spacing

Return ONLY the optimized content (including frontmatter), nothing else:

{content}""",
                temperature=0.1,  # Very low for consistency
                max_tokens=4000,
                model_preferences=["gpt-4", "claude-3-sonnet"],  # Prefer more reliable models
            )

            if response and hasattr(response, "text"):
                text_attr = getattr(response, "text", None)
                optimized_content = str(text_attr).strip() if text_attr else None

                # Basic validation - ensure we still have a memories section
                if optimized_content and ("## Memories" in optimized_content or "# Personal" in optimized_content):
                    return optimized_content
                else:
                    logger.warning("AI optimization removed essential sections, reverting to original")
                    return None
            else:
                logger.warning(f"AI optimization returned unexpected type or no text: {type(response)}")
                return None

        except Exception as e:
            logger.info(f"AI optimization failed: {e}")
            return None

    async def optimize_memory_if_needed(self, file_path: Path, ctx: Context, force: bool = False) -> Dict[str, Any]:
        """
        Main optimization method with full backward compatibility.

        Args:
            file_path: Path to memory file
            ctx: FastMCP context for AI sampling
            force: Force optimization regardless of criteria

        Returns:
            Dict with optimization results
        """
        try:
            # Get metadata (with backward compatibility)
            metadata = self._get_memory_metadata(file_path)

            # Check if optimization is needed
            if not force:
                should_optimize, reason = self._should_optimize_memory(file_path, metadata)
                if not should_optimize:
                    return {"status": "skipped", "reason": reason, "metadata": metadata}
            else:
                reason = "Forced optimization"

            # Read current content
            frontmatter, content = parse_frontmatter_file(file_path)
            full_content = "---\n"
            for key, value in frontmatter.items():
                if isinstance(value, str) and ('"' in value or "'" in value):
                    full_content += f'{key}: "{value}"\n'
                else:
                    full_content += f"{key}: {value}\n"
            full_content += f"---\n{content}"

            logger.info(f"Starting memory optimization: {reason}")

            # Try AI optimization
            optimized_content = await self._optimize_memory_with_ai(ctx, full_content)

            if optimized_content:
                # Parse optimized content directly from string
                optimized_frontmatter, optimized_body = parse_frontmatter(optimized_content)

                # Update metadata in the optimized frontmatter
                entry_count = self._count_memory_entries(optimized_body)

                # Count tokens in optimized content
                full_optimized = "---\n"
                for key, value in optimized_frontmatter.items():
                    if isinstance(value, str) and ('"' in value or "'" in value):
                        full_optimized += f'{key}: "{value}"\n'
                    else:
                        full_optimized += f"{key}: {value}\n"
                full_optimized += f"---\n{optimized_body}"
                optimized_tokens = self._count_tokens(full_optimized)

                optimized_frontmatter.update(
                    {
                        "lastOptimized": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "entryCount": entry_count,
                        "optimizationVersion": frontmatter.get("optimizationVersion", 0) + 1,
                        "lastOptimizedTokenCount": optimized_tokens,
                    }
                )

                # Preserve user preferences from original frontmatter
                if "autoOptimize" in frontmatter:
                    optimized_frontmatter["autoOptimize"] = frontmatter["autoOptimize"]
                elif "autoOptimize" not in optimized_frontmatter:
                    optimized_frontmatter["autoOptimize"] = True

                if "tokenGrowthThreshold" in frontmatter:
                    optimized_frontmatter["tokenGrowthThreshold"] = frontmatter["tokenGrowthThreshold"]
                elif "tokenGrowthThreshold" not in optimized_frontmatter:
                    optimized_frontmatter["tokenGrowthThreshold"] = 1.20

                # Remove deprecated fields
                for old_field in ["sizeThreshold", "entryThreshold", "timeThreshold"]:
                    optimized_frontmatter.pop(old_field, None)

                # Write optimized content
                success = write_frontmatter_file(file_path, optimized_frontmatter, optimized_body, create_backup=True)

                # Determine if backup was actually created (skipped for git repos)
                backup_created = False if is_in_git_repository(file_path) else success

                if success:
                    logger.info("Memory optimization completed successfully")
                    return {"status": "optimized", "reason": reason, "method": "ai", "entries_before": metadata.get("entryCount", 0), "entries_after": entry_count, "backup_created": backup_created}
                else:
                    return {"status": "error", "reason": "Failed to write optimized content"}
            else:
                # AI optimization failed, just update metadata
                logger.info("AI optimization unavailable, updating metadata only")
                success = self._update_metadata(file_path, content)

                # Determine if backup was actually created (skipped for git repos)
                backup_created = False if is_in_git_repository(file_path) else success

                return {"status": "metadata_updated", "reason": reason, "method": "metadata_only", "ai_available": False, "backup_created": backup_created}

        except Exception as e:
            logger.error(f"Memory optimization failed: {e}")
            return {"status": "error", "reason": str(e)}

    def get_memory_stats(self, file_path: Path) -> Dict[str, Any]:
        """
        Get statistics about a memory file.

        Returns metadata and file information for user inspection.
        """
        try:
            metadata = self._get_memory_metadata(file_path)
            frontmatter, content = parse_frontmatter_file(file_path)

            current_entries = self._count_memory_entries(content)
            file_size = file_path.stat().st_size

            # Count current tokens
            full_content = "---\n"
            for key, value in frontmatter.items():
                if isinstance(value, str) and ('"' in value or "'" in value):
                    full_content += f'{key}: "{value}"\n'
                else:
                    full_content += f"{key}: {value}\n"
            full_content += f"---\n{content}"
            current_tokens = self._count_tokens(full_content)

            # Calculate optimization eligibility
            should_optimize, reason = self._should_optimize_memory(file_path, metadata)

            # Calculate token growth
            last_optimized_tokens = metadata.get("lastOptimizedTokenCount", 0)
            token_growth = 0.0
            if last_optimized_tokens > 0:
                token_growth = ((current_tokens - last_optimized_tokens) / last_optimized_tokens) * 100

            return {
                "file_path": str(file_path),
                "file_size_bytes": file_size,
                "current_entries": current_entries,
                "current_tokens": current_tokens,
                "last_optimized": metadata.get("lastOptimized"),
                "last_optimized_tokens": last_optimized_tokens,
                "token_growth_percent": round(token_growth, 1),
                "optimization_version": metadata.get("optimizationVersion", 0),
                "auto_optimize_enabled": metadata.get("autoOptimize", True),
                "token_growth_threshold": metadata.get("tokenGrowthThreshold", 1.20),
                "optimization_eligible": should_optimize,
                "optimization_reason": reason,
                "entries_since_last_optimization": current_entries - metadata.get("entryCount", 0),
            }

        except Exception as e:
            return {"error": f"Could not read memory file stats: {e}"}
