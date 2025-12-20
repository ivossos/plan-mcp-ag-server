# Planning MCP Agentic Server

Oracle EPM Cloud Planning agentic server using Google ADK with MCP support.

## Features

- **25+ Planning Tools**: Full coverage of Oracle Planning REST API
- **Dual Mode**: MCP server (Claude Desktop) + Web API (FastAPI)
- **Memory & Feedback**: PostgreSQL persistence with RL tracking
- **Mock Mode**: Development without real Planning connection
- **Bilingual**: English and Portuguese support

## Quick Start

### Windows (Recommended)

**Automated Setup:**
```powershell
.\setup-windows.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create `.env` file from template
- Guide you through configuration

**Manual Setup:**
1. Create virtual environment: `python -m venv venv`
2. Activate: `.\venv\Scripts\Activate.ps1`
3. Install: `pip install -e .`
4. Configure: Copy `.env.example` to `.env` and edit
5. Initialize database: `python scripts\init_db.py` (if using PostgreSQL)

**Quick Commands:**
- Start web server: `.\start-server.bat`
- Start MCP server: `.\start-mcp-server.bat`
- Install dependencies: `.\install-dependencies.bat`
- Initialize database: `.\init-database.bat`

See [WINDOWS_DEPLOYMENT.md](WINDOWS_DEPLOYMENT.md) for detailed Windows setup guide.

### Linux/Mac

**1. Install Dependencies:**
```bash
pip install -e .
```

**2. Configure Environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

**3. Run:**

**MCP Server (for Claude Desktop):**
```bash
python -m cli.mcp_server
```

**Web Server (for API access):**
```bash
python -m web.server
```

**Interactive CLI:**
```bash
python -m cli.main
```

## Claude Desktop Configuration

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "planning-agent": {
      "command": "python",
      "args": ["-m", "cli.mcp_server"],
      "cwd": "C:\\path\\to\\plan-mcp-ag-server",
      "env": {
        "PLANNING_MOCK_MODE": "true"
      }
    }
  }
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/tools` | GET | List available tools |
| `/execute` | POST | Execute a tool |
| `/tools/{name}` | POST | Call specific tool |
| `/feedback` | POST | Submit user feedback |
| `/metrics` | GET | Get tool metrics |

## Available Tools

### Application
- `get_application_info` - Planning application details
- `get_rest_api_version` - API version info

### Jobs
- `list_jobs` - List recent jobs
- `get_job_status` - Job status by ID
- `execute_job` - Execute business rules, export metadata, etc.

### Dimensions
- `get_dimensions` - List all dimensions
- `get_members` - Get dimension members
- `get_member` - Get specific member with hierarchy

### Data
- `export_data_slice` - Export grid data
- `smart_retrieve` - Smart data retrieval
- `copy_data` / `clear_data`

### Reports
- `generate_report` - Generate Planning reports
- `get_report_job_status` - Async report status

### Variables
- `get_substitution_variables` - Get substitution variables
- `set_substitution_variable` - Set substitution variable

### Documents
- `get_documents` - List library documents

### Snapshots
- `get_snapshots` - List application snapshots

## Architecture

```
plan-mcp-ag-server/
├── planning_agent/      # Main package
│   ├── agent.py         # Agent orchestration
│   ├── config.py        # Configuration
│   ├── client/         # Planning HTTP client
│   ├── tools/          # 25+ tool modules
│   └── services/       # Feedback service
├── cli/                 # CLI & MCP server
│   ├── main.py         # Interactive CLI
│   └── mcp_server.py   # MCP stdio server
└── web/                 # FastAPI server
    └── server.py
```

## Deployment

### Windows

See [WINDOWS_DEPLOYMENT.md](WINDOWS_DEPLOYMENT.md) for complete Windows deployment guide including:
- Prerequisites installation
- Automated setup scripts
- Windows Service configuration
- Troubleshooting

### Docker

```bash
docker build -t planning-agent .
docker run -p 8080:8080 --env-file .env planning-agent
```

### Google Cloud Run

```bash
gcloud run deploy planning-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PLANNING_MOCK_MODE=true
```

## Feedback System

The agent tracks tool executions for reinforcement learning:

- **Automatic**: Execution time, success/failure, errors
- **User Feedback**: 1-5 rating via `/feedback` endpoint
- **Metrics**: Aggregated stats via `/metrics` endpoint

## Documentation

- [Windows Deployment Guide](WINDOWS_DEPLOYMENT.md) - Complete Windows setup
- [GitHub Setup Guide](GITHUB_SETUP.md) - Repository setup and configuration
- [Quick Deploy](QUICK_DEPLOY.md) - Google Cloud Run deployment
- [ChatGPT Quick Start](CHATGPT_QUICK_START.md) - ChatGPT integration
- [Dashboard Quick Start](DASHBOARD_QUICKSTART.md) - Performance dashboard

## License

MIT
