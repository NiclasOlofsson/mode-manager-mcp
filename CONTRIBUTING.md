# Contributing to Mode Manager MCP

Thank you for your interest in contributing to the Mode Manager MCP Server!

## Development Setup

1. **Install uv:**
   ```bash
   # Windows (PowerShell)
   # See installation options: https://docs.astral.sh/uv/getting-started/installation/
   pip install uv  # or use the standalone installer
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/NiclasOlofsson/mode-manager-mcp.git
   cd mode-manager-mcp
   ```

3. **Run tests:**
```bash
uv sync --group dev
uv run pytest
```

## Development Workflow

### Environment Management

uv manages a project-local virtual environment for you:

- Run `uv sync` to create/sync the `.venv` with all dependencies.
- Use `uv run <command>` to execute tools inside that environment without manually activating it.
- Optional: activate `.venv` manually if you prefer a shell (`source .venv/bin/activate` on bash, `.venv\Scripts\Activate.ps1` on PowerShell).

### Running Tests

```bash
# Run all tests
uv sync --group dev
uv run pytest

# Run tests with coverage (pytest - add coverage plugin if needed)
uv run pytest --cov

# Run against multiple Python versions (use matrix in CI or uv python pin locally)
# e.g., uv run --python 3.10 pytest
```

### Code Quality

```bash
# Format code with Ruff (via uv format)
uv run pydocstringformatter src tests && uv format

# Check formatting without applying
uv format --check

# Run type checking
uv run mypy src tests

# Run all quality checks (pre-commit hooks)
uv run pre-commit run --all-files
```

**Note:** Type checking currently reports some annotation issues that need to be addressed in future contributions.

### Building the Project

```bash
# Build wheel and source distribution
uv build

# Build only wheel
uv build --only wheel

# Build only source distribution  
uv build --only sdist
```

### Working with Dependencies

```bash
# Install project dependencies
uv sync --group dev

# Enter a shell in the venv (optional)
source .venv/bin/activate  # bash
# On Windows PowerShell: .venv\Scripts\Activate.ps1
```

### Available Scripts

The project defines several convenient scripts in `pyproject.toml`:

- `uv run pytest` - Run pytest
- `uv format --check` - Check code formatting with Ruff (built-in)
- `uv run mypy src tests` - Run mypy type checking  
- `uv format` - Format code with Ruff (built-in)
- `uv run pre-commit run --all-files` - Run pre-commit hooks

### Running Individual Commands

```bash
# Run any Python command in the environment
uv run python -m src.mode_manager_mcp

# Run the server directly for testing
uv run python -m src.mode_manager_mcp --help

# Enter a shell in the development environment
source .venv/bin/activate  # or use uv run for commands
```

## Development Environment

uv creates and manages a virtual environment (`.venv`) in your project directory when you run `uv sync`. This environment:

- Is used automatically when you run commands via `uv run`
- Contains all project dependencies and development tools
- Can be recreated by re-running `uv sync` if dependencies change
- Can be entered manually if preferred (see Environment Management above)

## Quick Reference

| Command | Description |
|---------|-------------|
| `uv run pytest` | Run all tests with pytest |
| `uv format --check` | Check code formatting (Ruff) |
| `uv format` | Auto-format code with Ruff |
| `uv run mypy src tests` | Run mypy type checking |
| `uv build` | Build wheel and source distribution |
| `uv run` | Run commands in the project environment |
| `uv sync` | Sync dependencies (creates .venv) |
| `uv cache clean` | Clean cache (useful if needed) |

## Code Style

- Follow PEP 8 conventions
- Use type hints where appropriate
- Include docstrings for all public functions and classes
- Keep functions focused and small

## Testing

- Add tests for new functionality
- Ensure all existing tests pass
- Test both success and error cases

## Submitting Changes

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Run tests**
5. **Commit with clear messages:**
   ```bash
   git commit -m "Add feature: description of changes"
   ```
6. **Push and create a pull request**

## Areas for Contribution

- **Bug fixes** - Check the issue tracker
- **Documentation** - Improve existing docs or add new guides
- **Features** - New chatmode/instruction management features
- **Library expansion** - Add more chatmodes/instructions to the library
- **Testing** - Improve test coverage
- **Performance** - Optimize file operations or network requests

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Questions?

Feel free to open an issue for questions or discussions!
