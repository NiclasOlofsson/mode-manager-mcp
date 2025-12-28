<picture>
  <source media="(prefers-color-scheme: dark)" srcset="remember-new-logo-complete-white.svg">
  <source media="(prefers-color-scheme: light)" srcset="remember-new-logo-complete-black.svg">
  <img alt="GitHub Copilot Memory Tool" src="https://raw.githubusercontent.com/NiclasOlofsson/mode-manager-mcp/refs/heads/main/remember-new-logo-complete-black.svg" width="800">
</picture>


# Meet #remember -- Real Memory for You, Your Team, and Your AI

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=modemanager&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mode-manager-mcp%22%5D%7D)
[![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=modemanager&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mode-manager-mcp%22%5D%7D&quality=insiders)
&nbsp;&nbsp;&nbsp;&nbsp;[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Mode Manager MCP is an AI-powered memory and context system for developers and teams. It lets you and your team “remember” important facts, preferences, and best practices—so your AI assistant always has the right context, and your team’s knowledge is never lost.

With Mode Manager MCP, you can:
- Instantly store and retrieve personal, team, and language-specific knowledge.
- Share onboarding notes, coding conventions, and project wisdom—right where you work.
- Make your AI assistant smarter, more helpful, and always in sync with your workflow.

## Why “Remember”? (Features & Benefits)

- **Personal AI Memory:** Instantly store preferences, facts, and reminders for yourself—your AI assistant will always know your context.
- **Workspace (Team) Memory:** Share best practices, onboarding notes, and team knowledge directly in the repo. New team members ramp up faster, and everyone stays on the same page.
- **Language-Specific Memory:** Save and retrieve language-specific tips and conventions. Your assistant adapts to each language’s best practices automatically.
- **Natural Language Simplicity:** Just say “remember…”—no config files, no YAML, no technical hurdles.
- **Smarter Coding, Fewer Repeated Questions:** Your team’s memory grows over time, reducing repeated questions and ensuring consistent practices.- **AI-Powered Memory Optimization:** Automatically consolidate and organize your memories to keep them clean and efficient.
&nbsp;  
>&nbsp;  
> **Before this tool**  
> *"Hey Copilot, write me a Python function..."*  
> Copilot: *Gives generic Python code*
>
> **After using `remember`**  
> You: *"Remember I'm a senior data architect at Oatly, prefer type hints, and use Black formatting"*  
> Next conversation: *"Write me a Python function..."*  
> Copilot: *Generates perfectly styled code with type hints, following your exact preferences*  
>&nbsp;  

**Ready to have Copilot that actually remembers you? [Get started now!](#get-it-running-2-minutes)**

## Real-World Examples: Just Say It!

You don’t need special syntax—just talk to Copilot naturally. Mode Manager MCP is extremely relaxed about how you phrase things. 
If it sounds like something you want remembered, it will be!

>&nbsp;  
>**Personal memory**  
> You: *I like detailed docstrings and use pytest for testing.
> (Copilot, keep that in mind.)*  
>
> ---  
>**Team memory**  
> You: *We alw&nbsp;ays use the Oatly data pipeline template and follow our naming conventions.
> (Let’s make sure everyone remembers that.)*
>
> ---  
>**Language-specific memory**
> You: *For Python, use type hints and Black formatting.
> In C#, always use nullable reference types.*  
>&nbsp;  

## Get It Running (2 Minutes)

If you don't have Python installed, get it at [python.org/downloads](https://www.python.org/downloads/) - you'll need Python 3.10 or higher.

Don't have `uv` yet? Install it with: `pip install uv` or see [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/)

### Option 1: One-Click Install (Easiest)

Click the badge for your VS Code version:

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=modemanager&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mode-manager-mcp%22%5D%7D)
[![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=modemanager&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mode-manager-mcp%22%5D%7D&quality=insiders)

That's it! The server will automatically start when you open VS Code.

### Option 2: Manual Configuration

Add this to your `.vscode/mcp.json` or global `mcp.json` file:

```json
{
  "servers": {
    "mode-manager": {
      "command": "uvx",
      "args": ["mode-manager-mcp"]
    }
  }
}
```

Or if you prefer `pipx`:

```json
{
  "servers": {
    "mode-manager": {
      "command": "pipx",
      "args": ["run", "mode-manager-mcp"]
    }
  }
}
```

### Option 3: Development / Testing (Latest from GitHub)

For the impatient who want the latest features immediately:

With `uvx`:

```json
{
  "servers": {
    "mode-manager": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/NiclasOlofsson/mode-manager-mcp.git",
        "mode-manager-mcp"
      ]
    }
  }
}
```

With `pipx`:

```json
{
  "servers": {
    "mode-manager": {
      "command": "pipx",
      "args": [
        "run",
        "--no-cache",
        "--spec",
        "git+https://github.com/NiclasOlofsson/mode-manager-mcp.git",
        "mode-manager-mcp"
      ]
    }
  }
}
```

This downloads and installs directly from GitHub every time - always bleeding edge!

### Bonus: Interactive Onboarding

As a convenience, you can run the following prompt in VS Code to get started:

>&nbsp;  
>You: */mcp.mode-manager.onboarding*  
>&nbsp;  

This will guide you through the onboarding process, set up your persistent memory, and ensure Copilot knows your preferences from the start.

### For Development / Testing Latest from GitHub

To run the latest code directly from GitHub:

```json
{
  "servers": {
    "mode-manager": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "git+https://github.com/NiclasOlofsson/mode-manager-mcp.git",
        "mode-manager-mcp"
      ],
      "env": {
        "_RESTART": "1"
      }
    }
  }
}
```


## Under the Hood: How Memory Magic Happens

Mode Manager MCP is designed to make memory persistent, context-aware, and 
easy to manage—without you having to think about the details. Here’s how 
it works under the hood:

### Memory Scopes

- **Personal Memory:**  
  Stored in a user-specific file (`memory.instructions.md`) in your VS Code prompts directory. This is your private memory—preferences, habits, and facts that follow you across all projects.

- **Workspace (Team) Memory:**  
  Stored in a workspace-level file (also `memory.instructions.md`, but in the workspace’s `.github/instructions` directory). This is shared with everyone working in the same repo, so team conventions and onboarding notes are always available.

- **Language-Specific Memory:**  
  Stored in files like `memory-python.instructions.md`, `memory-csharp.instructions.md`, etc. These are automatically loaded when you’re working in a particular language, so language tips and conventions are always at hand.

### How Memory is Stored

All memory is saved as Markdown files with a YAML frontmatter header, 
making it both human- and machine-readable. Each entry is timestamped and 
neatly organized, so you can always see when and what was remembered. You 
never have to manage these files yourself—Mode Manager MCP automatically 
creates and updates them as you add new memories.

### How Memory is Loaded

Here’s the magic: Mode Manager MCP writes and manages all your memory files, 
but it’s actually the new VS Code Copilot Chat that automatically loads 
them—every single turn. This deep integration means that, every time you send 
a message or ask Copilot for help, your user, workspace, and language memories 
are instantly available to the AI.

Language-specific memory is even smarter: it’s tied to file types using 
the `applyTo` property in the YAML frontmatter (for example, `**/*.py` for Python 
or `**/*.cs` for C#). This means you get the right tips, conventions, and 
reminders only when you’re working in the relevant language or file type—no clutter, 
just the context you need, exactly when you need it.

You never have to worry about context being lost between messages or sessions; your 
memory is always active and available. We’re simply leveraging this new, amazing 
VS Code feature to make your Copilot (and your team) smarter than ever.

### No Special Syntax Needed

There’s no need to remember special commands or keywords—just talk naturally. Mode Manager 
MCP is flexible and understands a wide range of phrasing. You don’t have to say 
“workspace” to store team memory; it recognizes common alternatives like “project,” 
“repo,” or even just describing something as a team convention. Whether you’re 
making a personal note, a team guideline, or a language-specific tip, just say it 
in your own words—Mode Manager MCP figures out what you want to remember and where it belongs.

## Contributing

Want to help make this better? The best contribution you can make is actually using it - your feedback and bug reports are what really drive improvements.

Of course, code contributions are welcome too! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines. But seriously, just using it and telling us what works (or doesn't) is incredibly valuable.

## License

MIT License - see [LICENSE](LICENSE) for details.
