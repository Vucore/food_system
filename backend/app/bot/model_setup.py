from transformers import pipeline
import torch

class CustomViQwen2LLM:
    def __init__(self, temperature: float = 0.2, max_new_tokens: int = 1024):
        MODEL_PATH = "AITeamVN/Vi-Qwen2-1.5B-RAG"
        
        self.pipeline = pipeline(
            "text-generation",
            model=MODEL_PATH,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=0.9,
            return_full_text=False
        )
    
    def invoke(self, prompt: str) -> str:
        response = self.pipeline(prompt)
        if isinstance(response, list) and len(response) > 0:
            return response[0]['generated_text']
        return str(response)
    
    def __call__(self, prompt: str) -> str:
        return self.invoke(prompt)