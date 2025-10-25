from app.bot.model_setup import CustomViQwen2LLM
from app.bot.base.Agent.rag_agentic import RAGAgentic
class ChatbotBase:
    def __init__(self):
        self.llm = CustomViQwen2LLM()
        self.rag_agent = RAGAgentic(self.llm)
    def generate_response(self, query: str):
        response = self.rag_agent.call(query)
        return response
    
if __name__ == "__main__":
    bot = ChatbotBase()
    query = input("Nhập câu hỏi về món ăn: ")
    response = bot.generate_response(query)
    print("Trả lời từ chatbot:")
    print(response)

'''cd backend -> python -m app.bot.init'''