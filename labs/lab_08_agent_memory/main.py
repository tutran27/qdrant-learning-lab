from labs.lab_08_agent_memory.llm_service import LLMService
from labs.lab_08_agent_memory.prompt import build_chat_prompt, EXTRACT_SYSTEM_PROMPT 
from labs.lab_08_agent_memory.memory_extractor import extract_response
from labs.lab_08_agent_memory.memory_service import MemoryService
from labs.lab_08_agent_memory.config import settings

from qdrant_client import QdrantClient
from common.embedding import load_dense_model

def main(user_id: str, client: QdrantClient):
    llm_service=LLMService()
    dense_model=load_dense_model()
    memory_service=MemoryService(user_id=user_id, client=client, dense_model=dense_model)
    memory_service.ensure_collection(settings.COLLECTION_NAME)
    memory_service.create_payload_index(settings.COLLECTION_NAME, settings.PAYLOAD_INDEX)

    history_memories=[]

    while True:
        query=str(input(f"User {user_id}: "))
        print(f"User: {query}")

        if query.lower()=="exit":
            break
        history_memories=memory_service.search_memory(query)

        system_prompt=build_chat_prompt(query,history_memories)
        response=llm_service.generate(query, system_prompt, 0.5)
        print(f"Response: {response}")

        memory=llm_service.generate(query,EXTRACT_SYSTEM_PROMPT, temperature=0)
        json_memory=extract_response(memory)
        print(f"json_memory: {json_memory}")

        memory_service.add_memory(json_memory)
        
if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    try:
        main("user_3", client)
    finally:
        client.close()
        print("client closed")
