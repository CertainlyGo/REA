import hashlib
import os.path
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"File {filepath} does not exist")
        return

    if not os.path.isfile(filepath):
        logger.error(f"File {filepath} is not a file")
        return

    md5 = hashlib.md5()

    chunk_size = 4096
    try:
        with open(filepath, 'rb') as f: #二进制读取
            while chunk := f.read(chunk_size): #分片读取
                md5.update(chunk)
            md5_hex = md5.hexdigest() #生成
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}的md5失败，异常为{str(e)}")

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):  #返回文件夹的文件列表（允许的后缀）
    files = []
    if not os.path.isdir(path):
        logger.error(f"路径{path}无效，不是文件夹")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return tuple(files)

def pdf_loader(filepath: str, password=None)-> list[Document]:
    return PyPDFLoader(filepath, password=password).load()

def txt_loader(filepath: str)-> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()