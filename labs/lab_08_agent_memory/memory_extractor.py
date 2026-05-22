from labs.lab_08_agent_memory.llm_service import LLMService
from labs.lab_08_agent_memory.prompt import EXTRACT_SYSTEM_PROMPT

import json
import re

def extract_response(response: str):
    try: 
        json_response=json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                json_response = json.loads(match.group(0))
            except json.JSONDecodeError:
                json_response = {"source_query": "", "memories": []}
        else:
            json_response = {"source_query": "", "memories": []}
 
    return json_response
    
if __name__ == "__main__":
    query="Xin chào, tôi tên là Tuấn và tôi đang học AI và muốn tìm hiểu qdrant"
    response = LLMService().generate(query, EXTRACT_SYSTEM_PROMPT)
    print("raw output: ")
    print(response)
    print("\n")
    print("json output: ")
    print(json.dumps(extract_response(response), ensure_ascii=False, indent=2))
