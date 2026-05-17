from langchain_community.document_loaders import PyPDFLoader


def load_document(path: str):
    loader=PyPDFLoader(path)
    pages=loader.load()
    return pages

if __name__=="__main__":
    path=r"/mnt/d/qdrant-learning-lab/data/raw/sample_docs/MemoryAgent.pdf"
    pages=load_document(path)
    for p in pages:
        print(p)
        break