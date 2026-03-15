import os
from datetime import datetime

from langchain_neo4j import Neo4jVector
from utils.config_handler import neo4j_config
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex


class VectorStoreService:
    def __init__(self):
        self.vector_store = Neo4jVector(
            embedding=embedding_model,
            url=neo4j_config["neo4j_url"],
            username=neo4j_config["neo4j_username"],
            password=neo4j_config["neo4j_password"],
            index_name="test",  # 连接已存在的索引
            node_label="Chunk"
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=neo4j_config["chunk_size"],
            chunk_overlap=neo4j_config["chunk_overlap"],
            separators=neo4j_config["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": neo4j_config["k"]})

    def load_document(self):
        """
        读取数据文件存入向量库
        :return:
        """
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(neo4j_config["md5_path"])):
                open(get_abs_path(neo4j_config["md5_path"]), "w", encoding="utf-8")
                return False

            with open(get_abs_path(neo4j_config["md5_path"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(neo4j_config["md5_path"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            elif read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(neo4j_config["data_path"]),
            tuple(neo4j_config["allowed_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}已经存在于知识库中")
                continue
            try:
                documents = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容")
                    continue
                split_documents: list[documents] = self.splitter.split_documents(documents)
                if not split_documents:
                    logger.warning(f"[加载知识库]分片后{path}内没有有效文本内容")
                    continue

                # metadata = {
                #     "source": path,
                #     "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #     "operator": "cc"
                # }

                #入库
                self.vector_store.add_documents(split_documents)
                # self.vector_store.add_documents(split_documents, metadatas = [metadata for _ in split_documents])

                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]{path}内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{path}知识库加载失败：{str(e)}", exc_info=True)
                continue

if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("机器人充不了电")
    for chunk in res:
        print(chunk.page_content)
        print("="*20)