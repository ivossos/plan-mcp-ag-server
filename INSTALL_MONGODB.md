# Installing MongoDB on Windows

## Option 1: MongoDB Community Server (Recommended)

### Download and Install

1. **Download MongoDB Community Server:**
   - Visit: https://www.mongodb.com/try/download/community
   - Select:
     - Version: Latest (7.0+)
     - Platform: Windows
     - Package: MSI
   - Click "Download"

2. **Run the Installer:**
   - Run the downloaded `.msi` file
   - Choose "Complete" installation
   - **Important:** Check "Install MongoDB as a Service"
   - Check "Install MongoDB Compass" (GUI tool)
   - Click "Install"

3. **Verify Installation:**
   ```powershell
   mongod --version
   mongo --version
   ```

### Start MongoDB Service

MongoDB should start automatically as a Windows service. To verify:

```powershell
# Check if MongoDB service is running
Get-Service MongoDB

# If not running, start it
Start-Service MongoDB
```

### Connect to MongoDB

```powershell
# Connect using MongoDB shell
mongosh

# Or using legacy mongo client
mongo
```

## Option 2: Using Chocolatey (Faster)

If you have Chocolatey installed:

```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install MongoDB
choco install mongodb -y

# Start MongoDB service
Start-Service MongoDB
```

## Option 3: Using Docker (Alternative)

If you have Docker Desktop installed:

```powershell
# Pull MongoDB image
docker pull mongo:latest

# Run MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Connect to MongoDB
docker exec -it mongodb mongosh
```

## Configuration

### Default Connection String

After installation, MongoDB will be available at:
```
mongodb://localhost:27017
```

### Create a Database

```javascript
// In mongosh
use planning_agent
db.createCollection("tool_executions")
```

## Note About This Project

**Important:** This Planning MCP Agent project is currently configured to use **PostgreSQL**, not MongoDB. The database URL in `config.py` is:

```python
database_url: str = "postgresql+psycopg://postgres:password@localhost:5432/planning_agent"
```

If you want to switch to MongoDB, you would need to:
1. Install a MongoDB adapter for SQLAlchemy (like `pymongo` or `mongoengine`)
2. Update the database URL format
3. Modify the service files to work with MongoDB instead of PostgreSQL

Would you like me to help you switch the project to use MongoDB instead of PostgreSQL?














