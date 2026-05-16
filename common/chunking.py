from langchain_text_splitters import RecursiveCharacterTextSplitter

from common.config import settings

def text_split(document) -> list[str]:
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", "."," ", ""]
    )
    chunks=splitter.split_documents(document)
    return chunks

if __name__=="__main__":
    from common.document_loader import load_document
    
    path=r"/mnt/d/qdrant-learning-lab/data/raw/sample_docs/MemoryAgent.pdf"
    pages=load_document(path)
    splitted_text=text_split(pages)
    print(splitted_text[10])

    title=splitted_text[0].metadata["title"]
    print(title)
    page=splitted_text[0].metadata["page"]
    total_pages=splitted_text[0].metadata["total_pages"]
    print(f"page {page}/{total_pages}")