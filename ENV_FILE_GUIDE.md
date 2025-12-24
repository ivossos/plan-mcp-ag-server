# .env File Configuration Guide

The `.env` file has been created in the project root. Here's what each setting does:

## Configuration Options

### Planning Connection
```bash
PLANNING_URL=                    # Your Oracle Planning instance URL
PLANNING_USERNAME=               # Your Planning username
PLANNING_PASSWORD=               # Your Planning password
PLANNING_API_VERSION=v3         # API version (default: v3)
PLANNING_MOCK_MODE=true          # Set to false for real connection
```

**Note:** When `PLANNING_MOCK_MODE=true`, the Planning URL, username, and password are not required. The agent will use mock data.

### Database (MongoDB)
```bash
DATABASE_URL=mongodb://localhost:27017/planning_agent
```

**Connection String Format:**
- Local: `mongodb://localhost:27017/planning_agent`
- With authentication: `mongodb://username:password@localhost:27017/planning_agent`
- Remote: `mongodb://user:pass@mongodb.example.com:27017/planning_agent`

### Server Configuration
```bash
PORT=8080                        # Web server port
```

### Gemini Model (Optional)
```bash
GOOGLE_API_KEY=                  # For future ADK integration
MODEL_ID=gemini-2.0-flash        # Model identifier
```

### Reinforcement Learning
```bash
RL_ENABLED=true                  # Enable/disable RL features
RL_EXPLORATION_RATE=0.1          # Exploration vs exploitation (0.0-1.0)
RL_LEARNING_RATE=0.1             # How fast RL learns (0.0-1.0)
RL_DISCOUNT_FACTOR=0.9           # Future reward discount (0.0-1.0)
RL_MIN_SAMPLES=5                 # Minimum samples before using RL
```

## Quick Setup

### For Development (Mock Mode)
```bash
PLANNING_MOCK_MODE=true
DATABASE_URL=mongodb://localhost:27017/planning_agent
```

### For Production (Real Planning Connection)
```bash
PLANNING_MOCK_MODE=false
PLANNING_URL=https://your-instance.epm.us-frankfurt-1.ocs.oc-test.com
PLANNING_USERNAME=your_username
PLANNING_PASSWORD=your_password
DATABASE_URL=mongodb://localhost:27017/planning_agent
```

## Verification

After configuring `.env`, test the setup:

```powershell
# Test MongoDB connection
python test_mongodb_connection.py

# Test Planning agent initialization
python -c "from planning_agent.agent import initialize_agent; import asyncio; print(asyncio.run(initialize_agent()))"
```

## Security Notes

⚠️ **Important:**
- Never commit `.env` to version control (it's in `.gitignore`)
- Keep your Planning credentials secure
- Use environment variables in production instead of `.env` file
- MongoDB connection strings with passwords should be kept secret













