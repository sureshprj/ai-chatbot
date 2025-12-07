from langchain_core.documents import Document
from langchain_groq import ChatGroq
from typing import List
from pydantic import BaseModel, Field
from ingestion_service.config.settings import settings


class ChunkResponse(BaseModel):
    chunks: List[str] = Field(description="List of semantic chunks")


class SemanticChunker:
    """
    Uses an LLM to split text into meaningful sections.
    """

    def __init__(self, model_name: str = settings.CHUNKER_MODEL):
        chunk_tool = {
            "name": "return_chunks",
            "description": "Return a list of semantic chunks extracted from text.",
            "input_schema": ChunkResponse.model_json_schema(),
        }

        self.llm = ChatGroq(
            model_name=model_name,
            tools=[chunk_tool],
            tool_choice="auto",
            temperature=0,
            api_key= settings.GROQ_API_KEY).with_structured_output(ChunkResponse)

        self.chunking_prompt = """ 
                You are a text segmentation engine.
                Goal:
                Split the input text into meaningful, coherent sections based on topics, ideas, or natural transitions.

                Rules:
                - Output each chunk as a separate string.
                - Preserve the original text exactly; do not summarize, rewrite, or change wording.
                - Remove unnecessary whitespace and redundant special characters.
                - Only split at natural boundaries (e.g., paragraph breaks, sentence ends).
                - Maintain logical flow; do not break sentences in half.
                - Aim for chunks that are roughly coherent; avoid overly long or overly short chunks.

                TEXT:
                {input}

            """
    
    def chunk(self, docs: List[Document]) -> List[Document]:

        final_chunks: List[Document] = []
        for doc in docs:
            resp:ChunkResponse = self.llm.invoke(
                self.chunking_prompt.format(input=doc.page_content)
            )
            # Convert to Document objects
            for chunk in resp.chunks:
                final_chunks.append(
                    Document(page_content=chunk.strip(), metadata=doc.metadata)
                )

        return final_chunks
