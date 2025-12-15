from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "开源罗盘 - 贡献者导航系统"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # API配置
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # 数据库配置
    database_url: str = "sqlite:///./open_compass.db"
    
    # GitHub API配置
    github_token: Optional[str] = None
    github_api_base: str = "https://api.github.com"
    
    # 第三方服务配置
    openai_api_key: Optional[str] = None
    
    # 项目配置
    default_repos: list = [
        "apache/iotdb",
        "X-lab2017/open-digger",
        "easy-graph/Easy-Graph"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()