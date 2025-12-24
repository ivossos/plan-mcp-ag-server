# MongoDB Migration Complete

The Planning MCP Agent project has been successfully migrated from PostgreSQL to MongoDB.

## Changes Made

### 1. Configuration (`planning_agent/config.py`)
- Changed default database URL from PostgreSQL to MongoDB:
  - **Before:** `postgresql+psycopg://postgres:password@localhost:5432/planning_agent`
  - **After:** `mongodb://localhost:27017/planning_agent`

### 2. Dependencies (`pyproject.toml`)
- **Removed:** `sqlalchemy>=2.0.0`, `psycopg[binary]>=3.1.0`
- **Added:** `pymongo>=4.6.0`, `motor>=3.3.0` (async MongoDB driver)

### 3. Feedback Service (`planning_agent/services/feedback_service.py`)
- Completely rewritten to use MongoDB instead of SQLAlchemy
- Uses `pymongo` for database operations
- Collections: `tool_executions`, `tool_metrics`
- Returns string IDs (MongoDB ObjectIds) instead of integers

### 4. RL Service (`planning_agent/services/rl_service.py`)
- Updated to use MongoDB collections: `rl_policy`, `rl_episodes`
- Removed SQLAlchemy dependencies
- Uses MongoDB indexes for performance

## Installation

1. **Install MongoDB:**
   ```powershell
   # Using Chocolatey
   choco install mongodb -y
   
   # Or download from: https://www.mongodb.com/try/download/community
   ```

2. **Start MongoDB Service:**
   ```powershell
   Start-Service MongoDB
   ```

3. **Install Python Dependencies:**
   ```powershell
   pip install -e .
   ```

4. **Configure Environment:**
   Create `.env` file with:
   ```
   DATABASE_URL=mongodb://localhost:27017/planning_agent
   PLANNING_MOCK_MODE=true
   ```

## Database Structure

### Collections

1. **tool_executions**
   - Stores individual tool execution records
   - Indexes: `session_id`, `tool_name`, `created_at`

2. **tool_metrics**
   - Aggregated metrics per tool
   - Index: `tool_name` (unique)

3. **rl_policy**
   - RL policy values (Q-values)
   - Indexes: `tool_name`, `context_hash` (unique compound)

4. **rl_episodes**
   - Complete session episodes
   - Indexes: `session_id`, `created_at`

## Connection String Format

```
mongodb://[username:password@]host[:port][/database][?options]
```

Examples:
- Local: `mongodb://localhost:27017/planning_agent`
- With auth: `mongodb://user:pass@localhost:27017/planning_agent`
- Remote: `mongodb://user:pass@mongodb.example.com:27017/planning_agent`

## Testing

After installation, test the connection:

```python
from planning_agent.services.feedback_service import init_feedback_service

service = init_feedback_service("mongodb://localhost:27017/planning_agent")
print("MongoDB connection successful!")
```

## Notes

- Execution IDs are now strings (MongoDB ObjectIds) instead of integers
- All database operations are synchronous (pymongo) - async support can be added with motor if needed
- The feedback service automatically creates indexes on first use
- MongoDB collections are created automatically when first document is inserted














