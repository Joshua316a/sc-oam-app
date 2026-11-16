# AI Agent Identification & Context

When working with AI coding agents on this project, please follow these guidelines to ensure effective collaboration.

## 🤖 Agent Types Supported

| Agent | Typical Trigger Phrase | Primary Strengths |
|-------|----------------------|-------------------|
| **OpenCode** | "skill", "tool", "codegraph", "gitnexus" | Multi-step workflow, codegraph integration, guardrails |
| **Claude Code** | "analyse", "debug", "implement" | Natural language, deep reasoning, large context |
| **GitHub Copilot** | inline suggestions | Real-time code completion, multi-language |
| **Cursor** | IDE-integrated | Full IDE experience, chat interface |
| **Custom/Local** | explicit specification | Pluggable, privacy-first |

## 🏗️ How to Identify the Agent

**For Human collaborators:** Assume standard developer knowledge, reference `docs/contributing/`.

**For AI agents:** Include the agent type in your initial prompt, e.g.:

> "I'm working with **OpenCode** on the sc-oam-app project. Please help me [task]. Here's the current state:..."

> "I'm working with **Claude** on the sc-oam-app project. Please analyze [issue] and provide a fix."

## 📋 Standard AI Agent Prompt Template

```
## Agent: <AGENT_TYPE>
## Platform: <OS>
## Project: sc-oam-app (v0.1.0)
## Task: <DESCRIPTION>

## Current Context
- Repository: /path/to/sc-oam-app
- Key files modified: <list>
- Recent commits: <list>
- Known issues: <list>

## Request
<task description>

## Constraints
- Follow Python/Ruf/Black style
- Maintain database pluggability (SQLite → PostgreSQL)
- Keep API consistency with existing endpoints
- Update documentation alongside code changes

## Deliverables
- Code changes with comments
- Updated tests (if applicable)
- Documentation updates (if applicable)
```

## 💡 Agent-Specific Recommendations

### OpenCode Users
```bash
# Preferred workflow
skill session-startup          # Health check first
skill codegraph_explore        # Code intelligence
skill gitnexus_impact          # Before edits
skill pre-release-validation   # Before release
```

### Claude Code Users
```
Please provide:
1. Full context (not just snippets)
2. Multiple approach options with trade-offs
3. Test considerations
4. Documentation impact
5. Platform-specific notes (macOS/Windows/Linux)
```

### Copilot/Cursor Users
```
Preferred interaction:
- Inline suggestions for boilerplate
- Chat for architecture/design questions
- Reference the .cursorrules if present
- Use /commands for common tasks
```
