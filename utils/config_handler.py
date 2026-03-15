"""
配置文件
"""

import yaml
from utils.path_tool import get_abs_path

def load_rag_config(config_path: str=get_abs_path("config/rag.yaml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_config

def load_neo4j_config(config_path: str=get_abs_path("config/neo4j.yaml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_config

def load_prompts_config(config_path: str=get_abs_path("config/prompts.yaml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_config

def load_agent_config(config_path: str=get_abs_path("config/agent.yaml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_config

rag_config = load_rag_config()
neo4j_config = load_neo4j_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()

