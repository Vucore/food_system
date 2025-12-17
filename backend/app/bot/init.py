from app.bot.base.Agent.rag_agentic import RAGAgentic
class ChatbotBase:
    def __init__(self):

        self.rag_agent = RAGAgentic()
    def generate_response(self, query: str, url: str, isBot: bool = True):
        response = self.rag_agent.call(query=query, url=url, isBot=isBot)
        return response

'''cd backend -> python -m app.bot.init'''