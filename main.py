"""
EOC Log Analyzer - Main Entry Point

AI-powered log analysis system using Claude AI agents to automatically
troubleshoot orders by analyzing database logs.
"""

import sys
from loguru import logger
from config import config

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    level=config.app.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

def check_configuration():
    """Verify configuration is ready"""
    logger.info("Checking configuration...")
    
    if not config.is_ready():
        logger.error("❌ Configuration not ready!")
        logger.error("   Missing required settings:")
        logger.error("   - DATABRICKS_TOKEN (Databricks access token)")
        logger.error("   - DATABASE_API_URL (eoc-database-api endpoint)")
        logger.error("")
        logger.error("   Please update your .env file with:")
        logger.error("   DATABRICKS_TOKEN=your-token-here")
        logger.error("   DATABASE_API_URL=http://localhost:8001")
        return False
    
    logger.info("✅ Configuration ready")
    logger.info(f"   LLM: {config.llm.claude_model}")
    logger.info(f"   Database API: {config.app.database_api_url}")
    logger.info(f"   Environment: {config.app.environment}")
    
    if config.has_gitlab():
        logger.info("✅ GitLab integration configured (code-aware analysis enabled)")
    else:
        logger.info("⚠️  GitLab not configured (code-aware analysis disabled)")
    
    if config.has_langsmith():
        logger.info("✅ LangSmith monitoring enabled")
    else:
        logger.info("⚠️  LangSmith monitoring disabled")
    
    return True




def test_llm_connection():
    """Test LLM connection"""
    logger.info("Testing LLM connection...")
    
    try:
        from langchain_databricks import ChatDatabricks
        
        # Extract endpoint name and host from URL
        endpoint_name = config.llm.databricks_base_url.split("/")[-1]
        host = config.llm.databricks_base_url.rsplit("/serving-endpoints/", 1)[0]
        
        llm = ChatDatabricks(
            endpoint=endpoint_name,
            host=host,
            api_token=config.llm.databricks_token,
            max_tokens=100,
            temperature=0.1
        )
        
        response = llm.invoke("Say 'LLM connection successful'")
        logger.info(f"✅ LLM connection successful: {response.content}")
        return True
    except Exception as e:
        logger.error(f"❌ LLM connection failed: {e}")
        logger.error("   Check your DATABRICKS_TOKEN in .env")
        return False


def run_example_analysis():
    """Run an example order analysis"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Running Example Analysis")
    logger.info("=" * 60)
    
    try:
        from agents import coordinator
        
        # Example order analysis
        user_data1 = "082869064"
        goal = "Find why message processing failed"
        
        logger.info(f"Analyzing logs for user_data1: {user_data1}")
        logger.info(f"Goal: {goal}")
        logger.info("")
        
        result = coordinator.analyze_order(
            user_data1=user_data1,
            goal=goal
        )
        
        logger.info("=" * 60)
        logger.info("Analysis Complete")
        logger.info("=" * 60)
        logger.info(f"Success: {result.get('success')}")
        logger.info(f"Goal Type: {result.get('goal_type')}")
        
        if result.get('success'):
            plan_info = result.get('plan_info', {})
            logger.info(f"Plan ID: {plan_info.get('plan_id')}")
            logger.info(f"Plan Created: {plan_info.get('plan_created')}")
            logger.info(f"Success Rate: {plan_info.get('success_rate', 0):.2f}")
            
            execution_info = result.get('execution_info', {})
            logger.info(f"Execution Time: {execution_info.get('execution_time_ms', 0):.0f}ms")
            
            logger.info("")
            logger.info("Agent Response:")
            logger.info("-" * 60)
            logger.info(execution_info.get('agent_response', 'No response'))
        else:
            logger.error(f"Analysis failed: {result.get('error')}")
        
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        logger.error(traceback.format_exc())


def interactive_mode():
    """Run in interactive mode"""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Interactive Mode")
    logger.info("=" * 60)
    logger.info("Type 'help' for commands, 'quit' to exit")
    logger.info("")
    
    from agents import coordinator
    
    while True:
        try:
            logger.info("")
            command = input("eoc-log-analyzer> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                logger.info("Goodbye!")
                break
            
            if command.lower() == 'help':
                print("")
                print("Commands:")
                print("  analyze <user_data1> <goal>  - Analyze logs by user_data1")
                print("  help                         - Show this help")
                print("  quit                         - Exit")
                print("")
                print("Example:")
                print("  analyze 082869064 Find payment failure")
                continue
            
            if command.lower().startswith('analyze '):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    logger.error("Usage: analyze <order_id> <goal>")
                    continue
                
                _, user_data1, goal = parts
                
                logger.info(f"Analyzing logs for user_data1: {user_data1}")
                logger.info(f"Goal: {goal}")
                
                result = coordinator.analyze_order(
                    user_data1=user_data1,
                    goal=goal
                )
                
                logger.info("")
                logger.info(f"✅ Analysis complete: Success={result.get('success')}")
                
                if result.get('success'):
                    execution_info = result.get('execution_info', {})
                    logger.info("")
                    logger.info("Response:")
                    logger.info("-" * 60)
                    logger.info(execution_info.get('agent_response', 'No response'))
                    logger.info("-" * 60)
                else:
                    logger.error(f"Error: {result.get('error')}")
            else:
                logger.warning(f"Unknown command: {command}")
                logger.info("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            logger.info("")
            logger.info("Interrupted. Type 'quit' to exit.")
        except Exception as e:
            logger.error(f"Error: {e}")


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info(f"{config.app.app_name} v{config.app.app_version}")
    logger.info("=" * 60)
    logger.info("")
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    logger.info("")
    
    # Test LLM connection
    if not test_llm_connection():
        logger.error("")
        logger.error("❌ LLM connection test failed. Please fix the issues above.")
        sys.exit(1)
    
    logger.info("")
    logger.info("✅ All systems ready!")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'ui':
            # Launch Streamlit UI
            logger.info("Launching Web UI...")
            logger.info("Opening browser at http://localhost:8501")
            import subprocess
            subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
        elif command == 'example':
            run_example_analysis()
        elif command == 'interactive':
            interactive_mode()
        elif command == 'analyze' and len(sys.argv) >= 4:
            user_data1 = sys.argv[2]
            goal = ' '.join(sys.argv[3:])
            
            from agents import coordinator
            result = coordinator.analyze_order(user_data1=user_data1, goal=goal)
            
            if result.get('success'):
                logger.info("✅ Analysis successful")
                execution_info = result.get('execution_info', {})
                print(execution_info.get('agent_response', 'No response'))
            else:
                logger.error(f"❌ Analysis failed: {result.get('error')}")
                sys.exit(1)
        else:
            print("")
            print("Usage:")
            print("  python main.py                                    # Launch Web UI (default)")
            print("  python main.py ui                                 # Launch Web UI")
            print("  python main.py interactive                        # Interactive CLI mode")
            print("  python main.py example                            # Run example analysis")
            print("  python main.py analyze <user_data1> <goal>        # Analyze specific logs")
            print("")
            print("Examples:")
            print("  python main.py ui")
            print("  python main.py example")
            print("  python main.py analyze 082869064 Find payment failure")
            sys.exit(1)
    else:
        # Default to Web UI
        logger.info("Launching Web UI (use 'python main.py interactive' for CLI mode)...")
        logger.info("Opening browser at http://localhost:8501")
        import subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    