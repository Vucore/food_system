from app.bot.base.Agent.tools import search_monngonmoingay, scrape_monngonmoingay

def function_router(function_name, arguments):
    if function_name == "crawl_monngonmoingay_query":
        results = search_monngonmoingay.invoke(arguments["query"])
        scraped_recipes = []
        if len(results) < 1:
            return "Không tìm thấy công thức nào phù hợp."
        if len(results) == 1:
            try:
                recipe_details = scrape_monngonmoingay.invoke(results[0]['url'])
                metadata = {
                    "nums": "only",
                    "title": results[0].get("title", ""),
                    "url": results[0].get("url", ""),
                    "ingredients": recipe_details.get("nguyenlieu", ""),
                    "preparation": recipe_details.get("soche", ""),      
                    "cookingSteps": recipe_details.get("thuchien", ""),  
                    "howToServe": recipe_details.get("howtouse", ""),     
                    "tips": recipe_details.get("tips", "")             
                }
                scraped_recipes.append(metadata)
                print(f"Đã crawl chi tiết công thức cho: {results[0]['title']}")
            except Exception as e:
                print(f"Lỗi khi cạo chi tiết cho {results[0]['title']}: {e}")
        else:
            print(f"Tìm thấy {len(results)} kết quả cho '{arguments['query']}':")
            for result in results:
                metadata = {
                    "nums": "multiple",
                    "title": result.get("title", ""),
                    "url": result.get("url", "")
                }
                scraped_recipes.append(metadata)

        return scraped_recipes
    
    elif function_name == "crawl_monngonmoingay_url":
        try:
            recipe_details = scrape_monngonmoingay.invoke(arguments["url"])
            if not recipe_details:
                return {"status": "error", "message": "Không tìm thấy dữ liệu phù hợp."}
            metadata = {
                "title": arguments.get("title", ""),
                "url": arguments.get("url", ""),
                "ingredients": recipe_details.get("nguyenlieu", ""),
                "preparation": recipe_details.get("soche", ""),      
                "cookingSteps": recipe_details.get("thuchien", ""),  
                "howToServe": recipe_details.get("howtouse", ""),     
                "tips": recipe_details.get("tips", "")             
            }
            print(f"Đã crawl chi tiết công thức cho: {metadata['title']}")
            return metadata
        except Exception as e:
            return f"Lỗi khi cạo chi tiết cho {arguments.get('url', '')}: {e}"

# Khi LLM trả về function_call:
# function_name = "search_monngonmoingay"
# arguments = {"query": "gà"}
# result = function_router(function_name, arguments)