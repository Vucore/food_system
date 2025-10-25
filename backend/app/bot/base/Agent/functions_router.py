from app.bot.base.Agent.tools import search_monngonmoingay, scrape_monngonmoingay

def function_router(function_name, arguments):
    if function_name == "crawl_monngonmoingay":
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
                print(f"Đã cạo chi tiết công thức cho: {results[0]['title']}")
            except Exception as e:
                print(f"Lỗi khi cạo chi tiết cho {results[0]['title']}: {e}")
        else:
            for result in results:
                print(f"Tìm thấy {len(results)} kết quả cho '{arguments['query']}':")
                metadata = {
                    "nums": "multiple",
                    "title": result.get("title", ""),
                    "url": result.get("url", "")
                }
                scraped_recipes.append(metadata)

        return scraped_recipes
    
    # ... các function khác

# Khi LLM trả về function_call:
# function_name = "search_monngonmoingay"
# arguments = {"query": "gà"}
# result = function_router(function_name, arguments)