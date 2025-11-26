"""
Configuration for Oracle Log Analyzer AI Agents

Handles environment variables and application settings
for the multi-agent log analysis system.

Supports multiple LLM providers:
- OpenAI (GPT-4, GPT-3.5-turbo)
- Anthropic (Claude)
- Meta (LLaMA via various providers)
- Google (Gemini)
"""

import os
from typing import Optional, Literal
from pydantic_settings import BaseSettings
from pydantic import Field

class LLMConfig(BaseSettings):
    """LLM Configuration - Using Databricks Claude Sonnet 4 Endpoint"""
    
    # Databricks Claude Endpoint
    # NOTE: Do NOT include /invocations - LangChain adds it automatically
    databricks_base_url: str = Field(
        default="https://dbc-4ee5e339-1e79.cloud.databricks.com/serving-endpoints/databricks-claude-sonnet-4",
        env="DATABRICKS_BASE_URL"
    )
    databricks_token: str = Field(env="DATABRICKS_TOKEN")
    
    # Claude Settings
    claude_model: str = Field(default="claude-sonnet-4", env="CLAUDE_MODEL")
    
    # Generation Settings
    max_tokens: int = Field(default=4096, env="LLM_MAX_TOKENS")
    temperature: float = Field(default=0.1, env="LLM_TEMPERATURE")

class AppConfig(BaseSettings):
    """Application Configuration"""
    
    # Application Info
    app_name: str = Field(default="Oracle Log Analyzer", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database API Settings
    database_api_url: str = Field(default="http://localhost:8001", env="DATABASE_API_URL")
    database_api_key: Optional[str] = Field(default=None, env="DATABASE_API_KEY")
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    
    # Plan Storage Settings
    plan_cache_ttl_seconds: int = Field(default=3600, env="PLAN_CACHE_TTL_SECONDS")
    max_plan_versions: int = Field(default=5, env="MAX_PLAN_VERSIONS")
    plan_success_threshold: float = Field(default=0.7, env="PLAN_SUCCESS_THRESHOLD")
    
    # Vector Search (Optional - requires Databricks Vector Search)
    # ⚠️  Querying vector search is cheap (~$0.0001/query)
    # ⚠️  Generating embeddings is expensive (~$0.01) and requires user approval
    enable_vector_search: bool = Field(default=False, env="ENABLE_VECTOR_SEARCH")
    
    # GitLab Integration (Optional)
    enable_gitlab: bool = Field(default=False, env="ENABLE_GITLAB")
    gitlab_url: Optional[str] = Field(default=None, env="GITLAB_URL")
    gitlab_token: Optional[str] = Field(default=None, env="GITLAB_TOKEN")
    gitlab_project_id: Optional[str] = Field(default=None, env="GITLAB_PROJECT_ID")
    gitlab_api_timeout: int = Field(default=30, env="GITLAB_API_TIMEOUT")
    gitlab_max_file_size: int = Field(default=1048576, env="GITLAB_MAX_FILE_SIZE")
    
    # LangSmith Configuration (Optional)
    langchain_tracing_v2: bool = Field(default=False, env="LANGCHAIN_TRACING_V2")
    langchain_api_key: Optional[str] = Field(default=None, env="LANGCHAIN_API_KEY")
    langchain_project: str = Field(default="oracle-log-analyzer", env="LANGCHAIN_PROJECT")
    
    # Monitoring & Performance
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=8080, env="METRICS_PORT")
    health_check_interval: int = Field(default=60, env="HEALTH_CHECK_INTERVAL")

class Config:
    """Main configuration combining all settings"""
    
    def __init__(self):
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        self.llm = LLMConfig()
        self.app = AppConfig()
    
    def is_ready(self) -> bool:
        """Check if configuration is ready"""
        # Check required Databricks token
        if not self.llm.databricks_token or self.llm.databricks_token == "your-databricks-token":
            return False
        
        # Check database API URL
        if not self.app.database_api_url:
            return False
        
        return True
    
    def has_gitlab(self) -> bool:
        """Check if GitLab integration is enabled and configured"""
        if not self.app.enable_gitlab:
            return False
        return all([
            self.app.gitlab_url,
            self.app.gitlab_token,
            self.app.gitlab_project_id
        ])
    
    def has_langsmith(self) -> bool:
        """Check if LangSmith monitoring is configured"""
        return self.app.langchain_tracing_v2 and self.app.langchain_api_key

# Global configuration instance
config = Config()
