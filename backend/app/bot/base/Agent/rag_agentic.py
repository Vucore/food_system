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
    def __init__(self):
        # Load model và tokenizer từ Hugging Face
        # self.llm = llm
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

        self.functions_name = ["crawl_monngonmoingay_query", "crawl_monngonmoingay_url"]

    # def call(self, query: str):
    #     function_name = self.functions_name[0]
    #     arguments = {"query": query}
    #     results = function_router(function_name, arguments)
    #     print(f"Function '{function_name}' returned results: {results}")
    #     # Nếu chỉ có 1 kết quả
    #     if isinstance(results, list) and results and results[0].get("nums") == "only":
    #         metadata = results[0]
    #         prompt = self.prompt_template.format(
    #             title=metadata.get("title", ""),
    #             ingredients=metadata.get("ingredients", ""),
    #             preparation=metadata.get("preparation", ""),
    #             cookingSteps=metadata.get("cookingSteps", ""),
    #             howToServe=metadata.get("howToServe", ""),
    #             tips=metadata.get("tips", ""),
    #             query=query
    #         )

    #         response = self.llm.invoke(prompt)
    #         return response

    #     # Nếu nhiều món
    #     elif isinstance(results, list) and results and results[0].get("nums") == "multiple":
    #         return "Tìm thấy nhiều món:\n" + "\n".join(
    #             f"- {item['title']}: {item['url']}" for item in results
    #         )

    #     else:
    #         return results
    def call(self, query: str = None, url: str = None):
        if url and not query:
            function_name = self.functions_name[1]
            arguments = {"url": url}
            results = function_router(function_name, arguments)
            print(f"Function '{function_name}' returned results: {results}")
            if isinstance(results, dict) and results:
                metadata = results
                return {
                    "status": "only",
                    "message": f"Tìm thấy món: {metadata.get('title', 'Không rõ tên')}",
                    "data": {
                        "title": metadata.get("title", ""),
                        "ingredients": metadata.get("ingredients", []),
                        "preparation": metadata.get("preparation", []),
                        "cookingSteps": metadata.get("cookingSteps", []),
                        "howToServe": metadata.get("howToServe", []),
                        "tips": metadata.get("tips", []),
                    },
                }

            # ---- Nếu không có kết quả hoặc sai định dạng ----
            return {
                "status": "error",
                "message": "Không tìm thấy dữ liệu phù hợp.",
            }
        elif query and not url: 
            function_name = self.functions_name[0]
            arguments = {"query": query}
            results = function_router(function_name, arguments)
            print(f"Function '{function_name}' returned results: {results}")
            if isinstance(results, list) and results:
                first = results[0]
                nums_type = first.get("nums", "")

                # ---- Nếu chỉ có 1 món ----
                if nums_type == "only":
                    metadata = first
                    return {
                        "status": "only",
                        "message": f"Tìm thấy 1 món: {metadata.get('title', 'Không rõ tên')}",
                        "data": {
                            "title": metadata.get("title", ""),
                            "ingredients": metadata.get("ingredients", []),
                            "preparation": metadata.get("preparation", []),
                            "cookingSteps": metadata.get("cookingSteps", []),
                            "howToServe": metadata.get("howToServe", []),
                            "tips": metadata.get("tips", []),
                        },
                    }

                # ---- Nếu có nhiều món ----
                elif nums_type == "multiple":
                    return {
                        "status": "multiple",
                        "message": f"Tìm thấy {len(results)} món tương tự.",
                        "options": [
                            {
                                "title": item.get("title", "Không rõ tên"),
                                "url": item.get("url", "#")
                            }
                            for item in results
                        ],
                    }

            # ---- Nếu không có kết quả hoặc sai định dạng ----
            return {
                "status": "error",
                "message": "Không tìm thấy dữ liệu phù hợp.",
            }
        else:
            return {
                "status": "error",
                "message": "Không tìm thấy dữ liệu phù hợp.",
            }