"""Test MongoDB connection for Planning project."""

from pymongo import MongoClient

try:
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/planning_agent", serverSelectionTimeoutMS=5000)
    
    # Test connection
    result = client.admin.command('ping')
    print("[OK] MongoDB connection successful!")
    print(f"   Ping result: {result}")
    
    # List databases
    print("\n[INFO] Available databases:")
    for db_name in client.list_database_names():
        print(f"   - {db_name}")
    
    # Test Planning database
    db = client.planning_agent
    collections = db.list_collection_names()
    print(f"\n[INFO] Collections in 'planning_agent' database: {collections if collections else '(none yet)'}")
    
    # Test write
    test_collection = db.test_connection
    test_collection.insert_one({"test": "connection", "timestamp": "now"})
    test_collection.delete_one({"test": "connection"})
    print("[OK] Write/Delete test successful!")
    
    client.close()
    print("\n[OK] All MongoDB tests passed! The Planning project is ready to use MongoDB.")
    
except Exception as e:
    print(f"[ERROR] MongoDB connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure MongoDB service is running: Get-Service MongoDB")
    print("2. Check if MongoDB is listening on port 27017")
    print("3. Verify connection string: mongodb://localhost:27017/planning_agent")

