from langchain.agents import create_agent

from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import *
from agent.tools.middleware import *


class ReactAgent:
    def __init__(self, max_context_turns: int = 10):
        """
        初始化 ReactAgent

        Args:
            max_context_turns: 保留的最大对话轮数（默认 10 轮，即最近 5 轮完整的问答）
        """
        self.agent = create_agent(
            model=chat_model,
            tools=[rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, fetch_external_data, fill_context_for_report],
            system_prompt=load_system_prompts(),
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )
        self.max_context_turns = max_context_turns

    def _build_context(self, chat_history: list) -> list:
        """
        构建上下文消息列表，自动截取最近的对话历史

        Args:
            chat_history: 完整的聊天历史记录

        Returns:
            截取后的上下文消息列表
        """
        if not chat_history:
            return []

        # 只保留最近的对话（每轮对话包含 user 和 assistant 各一条消息）
        # 保留最后 max_context_turns 条消息
        recent_history = chat_history[-self.max_context_turns:]

        messages = []
        for msg in recent_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        return messages

    def execute_stream(self, query: str, chat_history: list = None):
        """
        执行流式响应，自动管理上下文

        Args:
            query: 用户当前输入
            chat_history: 完整的聊天历史记录
        """
        # 如果没有传入聊天历史，初始化为空列表
        if chat_history is None:
            chat_history = []

        # 构建包含上下文的完整消息列表
        messages = self._build_context(chat_history)

        # 添加当前用户消息
        messages.append({"role": "user", "content": query})

        input_dict = {
            "messages": messages
        }
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)