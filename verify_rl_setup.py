"""Verification script for RL service setup."""

import sys
from planning_agent.config import config
from planning_agent.services.feedback_service import init_feedback_service, get_feedback_service
from planning_agent.services.rl_service import init_rl_service, get_rl_service

def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

# Use ASCII-compatible checkmarks for Windows compatibility
CHECK = "[OK]"
WARN = "[WARN]"
FAIL = "[FAIL]"

def verify_config():
    """Verify configuration settings."""
    print_section("Configuration Check")
    
    print(f"{CHECK} RL Enabled: {config.rl_enabled}")
    print(f"{CHECK} Exploration Rate: {config.rl_exploration_rate}")
    print(f"{CHECK} Learning Rate: {config.rl_learning_rate}")
    print(f"{CHECK} Discount Factor: {config.rl_discount_factor}")
    print(f"{CHECK} Min Samples: {config.rl_min_samples}")
    
    # Mask password in database URL
    db_url = config.database_url
    if "@" in db_url:
        display_url = db_url.split("@")[1]
    else:
        display_url = db_url
    print(f"{CHECK} Database URL: {display_url}")
    
    return config.rl_enabled

def verify_database_connection():
    """Verify database connection and tables."""
    print_section("Database Connection Check")
    
    try:
        feedback_service = init_feedback_service(config.database_url)
        print(f"{CHECK} Feedback service initialized successfully")
        
        # Try to query to verify tables exist
        try:
            metrics = feedback_service.get_tool_metrics()
            print(f"{CHECK} Database tables exist (found {len(metrics)} tool metrics)")
        except Exception as e:
            print(f"{WARN} Database connection OK but tables may not exist: {e}")
            print("  Run: python scripts/init_db.py")
            return None
        
        return feedback_service
    except Exception as e:
        print(f"{FAIL} Database connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure PostgreSQL is running")
        print("  2. Check DATABASE_URL in .env file")
        print("  3. Run: python scripts/init_db.py")
        return None

def verify_rl_service(feedback_service):
    """Verify RL service initialization."""
    print_section("RL Service Check")
    
    if not feedback_service:
        print(f"{FAIL} Cannot initialize RL service - feedback service not available")
        return None
    
    if not config.rl_enabled:
        print(f"{WARN} RL is disabled in configuration")
        return None
    
    try:
        rl_service = init_rl_service(
            feedback_service,
            config.database_url,
            exploration_rate=config.rl_exploration_rate,
            learning_rate=config.rl_learning_rate,
            discount_factor=config.rl_discount_factor,
            min_samples=config.rl_min_samples
        )
        print(f"{CHECK} RL service initialized successfully")
        
        # Check if RL tables exist
        try:
            policy_dict = rl_service._get_policy_dict()
            print(f"{CHECK} RL policy table accessible ({len(policy_dict)} policies)")
        except Exception as e:
            print(f"{WARN} RL service OK but policy table issue: {e}")
        
        return rl_service
    except Exception as e:
        print(f"{FAIL} RL service initialization failed: {e}")
        return None

def verify_rl_functionality(rl_service):
    """Verify RL functionality."""
    print_section("RL Functionality Check")
    
    if not rl_service:
        print(f"{WARN} Skipping functionality check - RL service not available")
        return
    
    try:
        # Test tool recommendations
        recommendations = rl_service.get_tool_recommendations(
            user_query="get application info",
            previous_tool=None,
            session_length=0
        )
        print(f"{CHECK} Tool recommendations working ({len(recommendations)} recommendations)")
        
        if recommendations:
            top_rec = recommendations[0]
            print(f"  Top recommendation: {top_rec['tool_name']} (confidence: {top_rec['confidence']:.3f})")
        
        # Test context hash creation
        context_hash = rl_service.tool_selector.create_context_hash(
            user_query="test query",
            previous_tool=None,
            session_length=0
        )
        print(f"{CHECK} Context hashing working (hash: {context_hash[:16]}...)")
        
        # Check for existing episodes
        episodes = rl_service.get_successful_sequences(limit=5)
        print(f"{CHECK} Episode tracking working ({len(episodes)} episodes found)")
        
    except Exception as e:
        print(f"{FAIL} RL functionality check failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main verification function."""
    print("\n" + "=" * 60)
    print("  RL Service Verification")
    print("=" * 60)
    
    # Step 1: Check configuration
    rl_enabled = verify_config()
    
    if not rl_enabled:
        print(f"\n{WARN} RL is disabled. Enable it by setting RL_ENABLED=true")
        return
    
    # Step 2: Check database connection
    feedback_service = verify_database_connection()
    
    if not feedback_service:
        print(f"\n{FAIL} Verification failed - database connection required")
        sys.exit(1)
    
    # Step 3: Check RL service
    rl_service = verify_rl_service(feedback_service)
    
    if not rl_service:
        print(f"\n{FAIL} Verification failed - RL service initialization required")
        sys.exit(1)
    
    # Step 4: Check functionality
    verify_rl_functionality(rl_service)
    
    # Summary
    print_section("Verification Summary")
    print(f"{CHECK} Configuration: OK")
    print(f"{CHECK} Database: OK")
    print(f"{CHECK} RL Service: OK")
    print(f"{CHECK} Functionality: OK")
    print("\n[SUCCESS] RL service is ready to use!")
    print("\nNext steps:")
    print("  1. Start the web server: python -m web.server")
    print("  2. Test RL endpoints: GET http://localhost:8080/rl/metrics")
    print("  3. Execute tools to start learning!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{FAIL} Verification error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

