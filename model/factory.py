from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from utils.config_handler import agent_config

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)-> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatOllama(model=agent_config["chat_model"])

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return OllamaEmbeddings(model=agent_config["embedding_model"])

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()