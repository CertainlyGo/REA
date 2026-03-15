from utils.config_handler import prompts_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_config['main_prompt_path'])
    except KeyError as e:
        logger.error(f"main_prompt_path不存在")
        raise e

    try:
        return open(system_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"解析系统提示词出错，{str(e)}")
        raise e

def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_config['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"rag_summarize_prompt_path不存在")
        raise e

    try:
        return open(rag_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"解析rag提示词出错，{str(e)}")
        raise e

def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_config['report_prompt_path'])
    except KeyError as e:
        logger.error(f"report_prompt_path不存在")
        raise e

    try:
        return open(report_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"解析报告提示词出错，{str(e)}")
        raise e