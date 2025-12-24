"""Test PostgreSQL connection for Planning project."""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from planning_agent.config import PlanningConfig

try:
    # Load configuration
    config = PlanningConfig()
    db_url = config.database_url
    
    print(f"[INFO] Testing PostgreSQL connection...")
    print(f"   Database URL: {db_url.split('@')[1] if '@' in db_url else '***'}")
    
    # Create engine
    engine = create_engine(db_url)
    
    # Test connection
    with engine.connect() as conn:
        # Test basic query
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"[OK] PostgreSQL connection successful!")
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        # Test database name
        result = conn.execute(text("SELECT current_database()"))
        db_name = result.fetchone()[0]
        print(f"   Current database: {db_name}")
        
        # Check if tables exist
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            print(f"\n[INFO] Existing tables in database:")
            for table in tables:
                print(f"   - {table}")
        else:
            print(f"\n[INFO] No tables found. Run 'python scripts/init_db.py' to initialize schema.")
    
    engine.dispose()
    print("\n[OK] All PostgreSQL tests passed! The Planning project is ready to use PostgreSQL.")
    
except OperationalError as e:
    print(f"[ERROR] PostgreSQL connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure PostgreSQL service is running")
    print("2. Check if PostgreSQL is listening on port 5432")
    print("3. Verify connection string in .env file:")
    print("   DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/planning_agent")
    print("4. Ensure the database exists (run 'python scripts/init_db.py')")
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    import traceback
    traceback.print_exc()








