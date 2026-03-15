import time
import os

import streamlit as st
from streamlit import spinner
from agent.react_agent import ReactAgent
from rag.vector_store import VectorStoreService
from utils.path_tool import get_abs_path
from utils.config_handler import neo4j_config


#标题
st.title('智扫通扫地机器人客服')
st.divider()

# 侧边栏 - 知识库管理
with st.sidebar:
    st.header("知识库管理")

    # 显示知识库文件列表
    knowledge_path = get_abs_path(neo4j_config["data_path"])
    allowed_types = tuple(neo4j_config["allowed_knowledge_file_type"])

    st.subheader("知识文件列表")
    if os.path.exists(knowledge_path):
        knowledge_files = [f for f in os.listdir(knowledge_path) if f.endswith(allowed_types)]
        if knowledge_files:
            for f in knowledge_files:
                st.text(f"  {f}")
        else:
            st.warning("暂无知识文件")
    else:
        st.error(f"知识库路径不存在：{knowledge_path}")

    st.divider()

    # 知识库统计
    st.subheader("知识库状态")
    md5_path = get_abs_path(neo4j_config["md5_path"])
    if os.path.exists(md5_path):
        with open(md5_path, "r", encoding="utf-8") as f:
            loaded_count = len([line for line in f.readlines() if line.strip()])
        st.info(f"已加载 {loaded_count} 个文件")
    else:
        st.info("暂无加载记录")

    st.divider()

    # 手动加载知识库按钮
    if st.button("重新加载知识库", use_container_width=True):
        with st.spinner("正在加载知识库，请稍候..."):
            try:
                vs = VectorStoreService()
                vs.load_document()
                st.success("知识库加载完成！")
            except Exception as e:
                st.error(f"加载失败：{str(e)}")

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent(max_context_turns=10)  # 保留最近 10 条消息作为上下文

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with spinner("智能客服思考中..."):
        # 传递聊天历史作为上下文
        chat_history = st.session_state["message"]
        res_stream = st.session_state["agent"].execute_stream(prompt, chat_history=chat_history)
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char


        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()
