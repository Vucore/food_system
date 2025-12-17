from app.bot.base.Agent.functions_router import function_router

class RAGAgentic:
    def __init__(self):

        self.functions_name = ["crawl_all_monngonmoingay_query", "crawl_monngonmoingay_url", "crawl_only_monngonmoingay_query"]

    def call(self, query: str = None, url: str = None, isBot: bool = True):
        if isBot:
            if query and not url: 
                function_name = self.functions_name[0]
                arguments = {"query": query}
                results = function_router(function_name, arguments)
                # print(f"Function '{function_name}' returned results: {results}")
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
            elif url and not query:
                function_name = self.functions_name[1]
                arguments = {"url": url}
                results = function_router(function_name, arguments)
                # print(f"Function '{function_name}' returned results: {results}")
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
            else:
                return {
                    "status": "error",
                    "message": "Không tìm thấy dữ liệu phù hợp.",
                }

        else:
            if query and not url: 
                function_name = self.functions_name[2]
                arguments = {"query": query}
                results = function_router(function_name, arguments)
                # print(f"Function '{function_name}' returned results: {results}")
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
                    return {
                    "status": "error",
                    "message": "Không tìm thấy dữ liệu phù hợp.",
                }
            else:
                return {
                    "status": "error",
                    "message": "Không tìm thấy dữ liệu phù hợp.",
                }
   