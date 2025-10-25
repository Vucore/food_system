# from langchain.prompts import PromptTemplate
# from fastapi.responses import StreamingResponse
# from app.bot.base.Agent.functions_router import function_router
# from langchain_core.messages import HumanMessage
# class RAGAgentic():
#     def __init__(self, llm):
#         self.llm = llm
#         self.prompt_template = PromptTemplate(
#             input_variables=["title", "ingredients", "preparation", "cookingSteps", "howToServe", "tips", "query"],
#             template="""
#                 Bạn là một trợ lý đầu bếp AI chuyên trả lời công thức món ăn và hướng dẫn nấu ăn chuyên nghiệp, luôn trả lời bằng tiếng Việt, chỉ sử dụng những dữ liệu được cung cấp, không thêm bất kỳ thông tin nào khác.

#                 Dưới đây là thông tin chi tiết về món ăn mà bạn cần sử dụng để trả lời câu hỏi của người dùng. Hãy trả lời thật tự nhiên, đầy đủ, dễ hiểu bằng tiếng Việt, sử dụng đúng các trường thông tin đã cho.

#                 Thông tin món ăn:
#                     - Tên món: {title}
#                     - Nguyên liệu: {ingredients}
#                     - Sơ chế: {preparation}
#                     - Các bước thực hiện: {cookingSteps}
#                     - Cách dùng: {howToServe}
#                     - Mẹo hay: {tips}

#                 Câu hỏi của người dùng: {query}

#                 Hãy trả lời dựa trên các thông tin trên. Nếu người dùng hỏi về nguyên liệu, chỉ trả lời phần nguyên liệu. Nếu hỏi về cách làm, hãy trả lời chi tiết các bước thực hiện. Nếu hỏi về mẹo hay hoặc cách dùng, hãy trả lời đúng phần đó. Nếu người dùng hỏi tổng quát, hãy trình bày đầy đủ các phần trên.
#             """
#         )
#         self.functions_name = [ "crawl_monngonmoingay" ]

#     def call(self, query: str):
#         function_name = self.functions_name[0]
#         arguments = {"query": query}
#         results = function_router(function_name, arguments)
        
#         # Nếu chỉ có 1 kết quả, lấy phần tử đầu tiên
#         if isinstance(results, list) and results and results[0].get("nums") == "only":
#             metadata = results[0]
#             prompt = self.prompt_template.format(
#                 title=metadata.get("title", ""),
#                 ingredients=metadata.get("ingredients", ""),
#                 preparation=metadata.get("preparation", ""),
#                 cookingSteps=metadata.get("cookingSteps", ""),
#                 howToServe=metadata.get("howToServe", ""),
#                 tips=metadata.get("tips", ""),
#                 query=query
#             )
#             answer = self.llm(prompt)
#             return answer
#         # Nếu nhiều kết quả, trả về danh sách món
#         elif isinstance(results, list) and results and results[0].get("nums") == "multiple":
#             return "Tìm thấy nhiều món:\n" + "\n".join(
#                 f"- {item['title']}: {item['url']}" for item in results
#             )
#         else:
#             return results 

 




# from langchain.prompts import PromptTemplate
# from fastapi.responses import StreamingResponse
# from app.bot.base.Agent.functions_router import function_router
# import asyncio
# from transformers import AutoTokenizer


# class RAGAgentic:
#     def __init__(self, llm):
#         self.llm = llm
#         self.tokenizer = AutoTokenizer.from_pretrained("AITeamVN/Vi-Qwen2-1.5B-RAG")

#         # Prompt tổng hợp dạng context (như trong RAG)
#         self.custom_prompt = PromptTemplate(
#             input_variables=["context", "query"],
#             template="""
#             Bạn là một đầu bếp AI chuyên nghiệp, luôn trả lời bằng **tiếng Việt**, 
#             và chỉ sử dụng thông tin được cung cấp dưới đây. Không tự bịa hoặc thêm thông tin khác.

#             -----
#             THÔNG TIN MÓN ĂN:
#             {context}
#             -----

#             CÂU HỎI CỦA NGƯỜI DÙNG:
#             {query}

#             Hãy trả lời dựa trên các thông tin trên bằng ngôn ngữ giao tiếp tự nhiên nhất có thể. 
#             Nếu người dùng chỉ nhập tên món (ví dụ: “phở gà”), hãy tóm tắt ngắn gọn món ăn, không liệt kê toàn bộ chi tiết.
#             Nếu người dùng hỏi về nguyên liệu, chỉ trả lời phần nguyên liệu. 
#             Nếu hỏi về cách làm, hãy mô tả chi tiết các bước.
#             Nếu hỏi về mẹo hay hoặc cách dùng, chỉ trả lời đúng phần đó.
#             Nếu hỏi tổng quát khác, hãy trình bày đầy đủ các phần trên.
#         """
#         )
#         self.functions_name = ["crawl_monngonmoingay"]

#     async def stream_answer(self, llm, prompt: str):
#         """Stream output từ LLM"""
#         for chunk in llm.stream(prompt):
#             if hasattr(chunk, "content"):
#                 for token in chunk.content:
#                     yield token
#                     await asyncio.sleep(0.002)

#     def build_context(self, metadata: dict) -> str:
#         """Ghép dữ liệu crawl thành 1 đoạn context duy nhất"""
#         parts = []
#         if metadata.get("title"):
#             parts.append(f"• Tên món: {metadata['title']}")
#         if metadata.get("ingredients"):
#             parts.append(f"• Nguyên liệu:\n{metadata['ingredients']}")
#         if metadata.get("preparation"):
#             parts.append(f"• Sơ chế:\n{metadata['preparation']}")
#         if metadata.get("cookingSteps"):
#             parts.append(f"• Cách nấu:\n{metadata['cookingSteps']}")
#         if metadata.get("howToServe"):
#             parts.append(f"• Cách dùng:\n{metadata['howToServe']}")
#         if metadata.get("tips"):
#             parts.append(f"• Mẹo:\n{metadata['tips']}")

#         return "\n".join(parts)

#     def call(self, query: str):
#         """Gọi mô hình trả lời theo context từ crawl"""
#         function_name = self.functions_name[0]
#         arguments = {"query": query}
#         results = function_router(function_name, arguments)

#         if isinstance(results, list) and results and results[0].get("nums") == "only":
#             metadata = results[0]
#             context = self.build_context(metadata)
#             prompt = self.custom_prompt.format(context=context, query=query)

#             # Tạo định dạng chat phù hợp với Vi-Qwen2
#             messages = [
#                 {"role": "system", "content": "Bạn là đầu bếp AI chuyên trả lời món ăn Việt Nam."},
#                 {"role": "user", "content": prompt}
#             ]
#             formatted_prompt = self.tokenizer.apply_chat_template(
#                 messages, tokenize=False, add_generation_prompt=True
#             )

#             # Gọi LLM (non-stream)
#             answer = self.llm.invoke(formatted_prompt)
#             return answer

#         elif isinstance(results, list) and results and results[0].get("nums") == "multiple":
#             return "Tìm thấy nhiều món:\n" + "\n".join(
#                 f"- {item['title']}: {item['url']}" for item in results
#             )

#         else:
#             return "Không tìm thấy món phù hợp hoặc dữ liệu rỗng."




from langchain.prompts import PromptTemplate
from app.bot.base.Agent.functions_router import function_router
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class RAGAgentic:
    def __init__(self, llm):
        # Load model và tokenizer từ Hugging Face
        self.llm = llm
        # Prompt cơ bản
        self.prompt_template = PromptTemplate(
            input_variables=["title", "ingredients", "preparation", "cookingSteps", "howToServe", "tips", "query"],
            template="""
                Bạn là một đầu bếp AI chuyên nghiệp, luôn trả lời bằng **tiếng Việt**, 
                và chỉ sử dụng thông tin được cung cấp dưới đây. Không tự bịa hoặc thêm thông tin khác.

                -----
                THÔNG TIN MÓN ĂN:
                • Tên món: {title}
                • Nguyên liệu: {ingredients}
                • Sơ chế: {preparation}
                • Cách nấu: {cookingSteps}
                • Cách dùng: {howToServe}
                • Mẹo: {tips}
                -----

                CÂU HỎI CỦA NGƯỜI DÙNG:
                {query}

                Hãy trả lời ngắn gọn, rõ ràng, đúng với câu hỏi với ngôn ngữ giao tiếp tự nhiên nhất có thể, KHÔNG thêm hashtag hoặc ký tự đặc biệt.
                Nếu người dùng chỉ nhập tên món (ví dụ: “phở gà”), hãy tóm tắt ngắn gọn món ăn, không liệt kê toàn bộ chi tiết.
                Nếu người dùng hỏi về nguyên liệu, chỉ nêu phần nguyên liệu.
                Nếu hỏi về cách làm, hãy mô tả chi tiết các bước.
                Nếu hỏi tổng quát, hãy trình bày đầy đủ gồm nguyên liệu, sơ chế, nấu, mẹo, cách dùng.
            """
        )

        self.functions_name = ["crawl_monngonmoingay"]

    def call(self, query: str):
        function_name = self.functions_name[0]
        arguments = {"query": query}
        results = function_router(function_name, arguments)
        print(f"Function '{function_name}' returned results: {results}")
        # Nếu chỉ có 1 kết quả
        if isinstance(results, list) and results and results[0].get("nums") == "only":
            metadata = results[0]
            prompt = self.prompt_template.format(
                title=metadata.get("title", ""),
                ingredients=metadata.get("ingredients", ""),
                preparation=metadata.get("preparation", ""),
                cookingSteps=metadata.get("cookingSteps", ""),
                howToServe=metadata.get("howToServe", ""),
                tips=metadata.get("tips", ""),
                query=query
            )

            response = self.llm.invoke(prompt)
            return response

        # Nếu nhiều món
        elif isinstance(results, list) and results and results[0].get("nums") == "multiple":
            return "Tìm thấy nhiều món:\n" + "\n".join(
                f"- {item['title']}: {item['url']}" for item in results
            )

        else:
            return results





# from langchain.prompts import PromptTemplate
# from fastapi.responses import StreamingResponse
# from ..RAG.file_loader import DocumentLoader
# from ..RAG.setup_spilitter import TextSplitter
# from ..RAG.vectorstore import VectorDB
# from ..RAG.setup_retriever import Retriever
# import asyncio

# class RAGAgent():
#     def __init__(self, llm):
#         self.llm = llm
#         self.document_loader = DocumentLoader()
#         self.splitter_class = TextSplitter()
#         self.vectorstore = None
#         self.retriever_class = Retriever()
#         self.retriever = None
#         self.ensemble_retriever = None
#         self.process_documents()
#         self.build_ensemble_retriever()

#     def process_documents(self):
#         # documents = self.pdf_loader.load_pdf_docs()
#         documents = self.document_loader.load_markdown_docs()
#         docs = self.splitter_class.split_documents(documents=documents)
#         self.vectorstore = VectorDB(docs=docs,
#                                           embedding=self.embedding
#                                         ).get_vectorstore()
#         self.retriever = self.retriever_class.build_retriever(docs=docs, k=3)

#     def build_ensemble_retriever(self):
#         self.ensemble_retriever = self.retriever_class.get_ensemble_retriever(vectorstore=self.vectorstore, retriever=self.retriever)

#         self.custom_prompt = PromptTemplate(
#             input_variables=["context", "question"],
#             template="""
#                     Bạn là một trợ lý AI chuyên về cảnh báo lũ lụt, mực nước và lượng mưa hoặc các chỉ số thời tiết được cung cấp tài liệu.
#                     Chỉ dựa vào thông tin tìm được từ công cụ và kiến thức nội tại của bạn về chủ đề này để trả lời.
#                     Nếu không tìm thấy thông tin trong tài liệu, hãy nói rằng bạn không có thông tin đó trong tài liệu được cung cấp.
#                     Luôn trả lời bằng tiếng Việt một cách rõ ràng và chi tiết nhất có thể dựa trên thông tin có được, không thêm bất kỳ văn bản nào khác.
                    
#                     Thông tin:
#                     {context}

#                     Câu hỏi:
#                     {question}
#                     Hãy trả lời bằng tiếng Việt!
#                     """,
#                     )

#     def run_rag(self, query: str):
#         async def stream_answer(llm, prompt: str):
#             for chunk in llm.stream(prompt):
#                 if hasattr(chunk, "content"):
#                     for token in chunk.content:
#                         yield token
#                         await asyncio.sleep(0.002)

#         async def generate_response():
#             '''Retrieval'''
#             docs = self.ensemble_retriever.invoke(query)  
#             # In thông tin chi tiết về từng document
#             print("\n=== Retrieved Documents ===")
#             for i, doc in enumerate(docs, 1):
#                 print(f"\nDocument {i}:")
#                 print(f"Content: {doc.page_content}")
#                 print(f"Metadata: {doc.metadata}")
#             print("=" * 50)

#             '''Context'''
#             context = "\n".join([doc.page_content for doc in docs])
#             max_context_length = 10000  
#             if len(context) > max_context_length:
#                 context = context[:max_context_length]

#             '''Prompt'''
#             prompt = self.custom_prompt.format(context=context, question=query)

#             response_text = ""
#             async for token in stream_answer(self.llm, prompt):
#                 response_text += token
#                 yield token

#         return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")

#     def run_llm(self, query: str):
#         async def stream_answer(llm, prompt: str):
#             for chunk in llm.stream(prompt):
#                 if hasattr(chunk, "content"):
#                     for token in chunk.content:
#                         yield token
#                         await asyncio.sleep(0.002)
#         prompt = "Hãy trả lời bằng tiếng Việt cho câu hỏi {}".format(query)
        
#         async def generate_response():
#             response_text = ""
#             async for token in stream_answer(self.llm, prompt):
#                 response_text += token
#                 yield token

#             # Log the conversation after response is complete
#             self.conversation_logger.log_conversation(
#                 question=query,
#                 answer=response_text,
#                 rag_used=False,
#                 response_type="chat"
#             )

#         return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")
