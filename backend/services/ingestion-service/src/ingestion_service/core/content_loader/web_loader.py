from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
from typing import List


class WebLoader:
    """ to load the web pages in given urls """

    def __init__(self):
        print(f"web loader initiated")
        
    def load_docs(self, urls = list[str]):
        """
        web scraping using WebBaseLoader
        Returns: List of Document objects
        """
        final_documents = []
        for url in urls:
            loader = WebBaseLoader(
                        url,
                        bs_get_text_kwargs={'separator': ' ', 'strip': True},
                        bs_kwargs={},
                        header_template={'User-Agent': 'Mozilla/5.0'}
                    )
            documents = loader.load()
            
            for doc in documents:
                doc.page_content = self._cleanup_html(doc.page_content)
                print(f"Content: {doc.page_content[:50]}...")
                print(f"Metadata: {doc.metadata}")
            final_documents.extend(documents)

        print('all the documents loaded')
        return final_documents 

    def load_doc(self, url: str):
        """load single url at a time"""
        loader = WebBaseLoader(
                url,
                bs_get_text_kwargs={'separator': ' ', 'strip': True},
                bs_kwargs={},
                header_template={'User-Agent': 'Mozilla/5.0'}
            )
        documents = loader.load()
    
        for doc in documents:
            doc.page_content = self._cleanup_html(doc.page_content)
            print(f"Content: {doc.page_content[:50]}...")
            print(f"Metadata: {doc.metadata}")
        
        return documents

    def _cleanup_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text