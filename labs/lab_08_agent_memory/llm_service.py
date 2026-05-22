from dotenv import load_dotenv

from groq import Groq

from common.config import settings

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def generate(self, query: str, system_prompt: str, temperature: float = 0.7):      
        completion = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role":"system",
                    "content": system_prompt    
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
        temperature=temperature,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None
        )
        # for chunk in completion:
        #     print(chunk.choices[0].delta.content or "", end="")
        return completion.choices[0].message.content

if __name__=="__main__":
    llm=LLMService()
    llm.generate("Hello", "You are a helpful assistant.")
    
