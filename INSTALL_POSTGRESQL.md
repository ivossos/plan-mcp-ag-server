# Installing PostgreSQL on Windows

## Quick Installation Guide

### Option 1: Official PostgreSQL Installer (Recommended)

1. **Download PostgreSQL:**
   - Visit: https://www.postgresql.org/download/windows/
   - Click "Download the installer"
   - Download the latest version (PostgreSQL 15 or 16)

2. **Run the Installer:**
   - Run the downloaded `.exe` file
   - Choose installation directory (default is fine)
   - Select components (default is fine - includes PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - Choose data directory (default is fine)
   - **IMPORTANT:** Set a password for the `postgres` superuser account
     - Remember this password - you'll need it for the connection string
   - Choose port (default 5432 is fine)
   - Choose locale (default is fine)
   - Complete the installation

3. **Verify Installation:**
   ```powershell
   psql --version
   ```
   Expected output: `psql (PostgreSQL) 15.x` or similar

4. **Check PostgreSQL Service:**
   ```powershell
   Get-Service postgresql*
   ```
   The service should be running automatically.

### Option 2: Using Chocolatey (Faster)

If you have Chocolatey package manager installed:

```powershell
# Install PostgreSQL
choco install postgresql -y

# Note: You may need to set the postgres password manually after installation
# The default password might be 'postgres' or you may need to set it via pgAdmin
```

### Option 3: Using Docker (Alternative)

If you have Docker Desktop installed:

```powershell
# Pull PostgreSQL image
docker pull postgres:15

# Run PostgreSQL container
docker run -d `
  --name postgres-planning `
  -e POSTGRES_PASSWORD=password `
  -e POSTGRES_DB=planning_agent `
  -p 5432:5432 `
  postgres:15

# Note: Update DATABASE_URL in .env to:
# DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/planning_agent
```

## Configuration

### Default Connection Settings

After installation, PostgreSQL will be available at:
- **Host:** localhost
- **Port:** 5432
- **Username:** postgres
- **Password:** (the password you set during installation)
- **Database:** planning_agent (will be created by init script)

### Update Your .env File

Edit your `.env` file and set:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/planning_agent
```

Replace `YOUR_PASSWORD` with the password you set during PostgreSQL installation.

## Initialize Database

After installing PostgreSQL and updating your `.env` file:

```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Initialize database
python scripts\init_db.py
```

This will:
1. Create the `planning_agent` database if it doesn't exist
2. Create all required tables (tool_executions, tool_metrics, rl_policy, rl_episodes)

## Test Connection

```powershell
python test_postgresql_connection.py
```

## Troubleshooting

### PostgreSQL Service Not Running

```powershell
# Check service status
Get-Service postgresql*

# Start the service (replace version number if different)
Start-Service postgresql-x64-15
```

### Connection Refused

1. Check if PostgreSQL is listening on port 5432:
   ```powershell
   netstat -ano | findstr :5432
   ```

2. Verify PostgreSQL service is running:
   ```powershell
   Get-Service postgresql*
   ```

3. Check firewall settings (PostgreSQL should allow local connections)

### Authentication Failed

1. Verify the password in your `.env` file matches the postgres user password
2. Try connecting manually:
   ```powershell
   psql -U postgres -h localhost
   ```
   (Enter password when prompted)

### Database Already Exists Error

If you see "database already exists", that's fine - the init script will skip creation and just initialize the schema.

## Using pgAdmin (GUI Tool)

PostgreSQL installation includes pgAdmin 4, a graphical tool for managing PostgreSQL:

1. Open pgAdmin 4 from Start Menu
2. Connect to localhost server (password is the one you set during installation)
3. You can browse databases, tables, and run SQL queries

## Alternative: Use SQLite for Development

If you want to skip PostgreSQL installation for now, you can use SQLite (included with Python):

Update your `.env` file:
```env
DATABASE_URL=sqlite:///planning_agent.db
```

**Note:** SQLite is fine for development, but PostgreSQL is recommended for production and better performance with concurrent access.








