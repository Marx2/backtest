# Agent Configuration

This file contains configuration and instructions for AI agents working in this project.

## Project Context

Python application which is doing backtests.

## Documentation (context7 MCP)

Use the context7 MCP server to fetch up-to-date documentation.
Always prefer context7 docs over web search or training data for these libraries.

## Agent Behaviors

Do not make any changes until you have 95% confidence in what you need to build. Ask me
follow-up questions until you reach that confidence.

## Code Style

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure credentials (required before first run)
cp .env.example .env
# Edit .env to add some credentials
```

### Running the App
```bash
python main.py -config=config/backtest.yaml -strategy=strategies/basic.py
```

## Project Structure Conventions

**Main folder** - Keep clean, only essential files:
- Entry points: `main.py`
- Configuration: `requirements.txt`, `.env`
- Documentation: `README.md`

**Organized subdirectories**:
- `tests/` - All test files (unit, integration, e2e)
- `docs/` - Documentation (guides, reports, specifications)
- `config/` - Configuration files
- `strategies/` - Strategies folder

**Important conventions**:
- Never add new files to the root directory unless absolutely necessary
- Tests belong in `tests/` even if they're integration tests
- Documentation belongs in `docs/` even if it's temporary
- When extending functionality, add to existing modules rather than creating new root-level files

## Applied Learning

When something fails repeatedly, when I has to re-explain, or when a workaround is found for a
platform/tool limitation, add a one-line bullet here. Keep each bullet under 15 words. No
explanations. Only add things that will save time in future.