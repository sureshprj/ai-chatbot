from langchain_huggingface import HuggingFaceEmbeddings
from shared_service.config.settings import settings

class HuggingFaceEmbedding:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def embed(self, text: str):
        """ 
        Embeds a text string into a vector space.
        """
        return self.model.embed_query(text)

    def embed_documents(self, documents: list[str]):
        """ 
        Embeds a list of text strings into a vector space.
        """
        return self.model.embed_documents(documents)