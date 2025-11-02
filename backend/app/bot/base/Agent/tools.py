from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
import re

from dotenv import load_dotenv
load_dotenv() 

# Viết mail
# def generate_email(username, address, date):
#     llm = load_model_Llama3(temperature=0.1)
#     prompt = PromptTemplate(
#         input_variables=["username", "address", "date"],
#         template=(
#             "Bạn là một trợ lý AI. Bạn sẽ đại diện cho `Hệ thống gửi mail tự động` để viết email chuyên nghiệp bằng tiếng Việt\n"
#             "Nội dung gmail là cảnh báo lũ lụt đến người nhận\n"
#             "Thông tin người nhận:\n"
#             "- Tên: {username}\n"
#             "- Địa chỉ: {address}\n"
#             "- Thời điểm hiện tại: {date}\n\n"
#             "Hãy viết một email hoàn chỉnh, nội dung rõ ràng, giọng văn phù hợp bằng tiếng Việt chỉ trả về nội dung email mà bạn viết, không thêm bất kỳ văn bản nào khác.\n\n"
#         )
#     )
#     chain: RunnableSequence = prompt | llm
#     return chain.invoke({
#         "username": username,
#         "address": address,
#         "date" : date
#     })

@tool
def search_all_monngonmoingay(query: str):
    """
    Tìm kiếm công thức món ăn trên monngonmoingay.com theo từ khóa.
    Trả về danh sách tiêu đề và URL công thức phù hợp.
    """
    search_url = f"https://monngonmoingay.com/?s={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MonNgonCrawler/1.0; +https://yourdomain.example)"
    }

    try:
        r = requests.get(search_url, headers=headers, timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Lỗi tìm kiếm: {e}")

    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    links = soup.find_all("a", href=True)

    recipe_url_pattern = re.compile(r"https://monngonmoingay.com/(?!tim-kiem-mon-ngon|thuc-don-dinh-duong|mach-nho|ke-hoach-nau-an|gia-vi-ban-can|lich-phat-song|tich-diem-doi-qua|lay-lai-mat-khau|category|tag|author|date|page|comment|feed)[^/]+/+$")


    for link in links:
        url = link.get("href")
        title = link.get_text(strip=True)

        if url and title: 
            if recipe_url_pattern.match(url):
                results.append({"title": title, "url": url})

    unique_results = []
    seen_urls = set()
    for result in results:
        if result['url'] not in seen_urls:
            unique_results.append(result)
            seen_urls.add(result['url'])
    
    return unique_results

@tool
def search_only_monngonmoingay(query: str):
    """
    Tìm kiếm công thức món ăn trên monngonmoingay.com theo từ khóa.
    Trả về tiêu đề và URL công thức đầu tiên phù hợp.
    """
    search_url = f"https://monngonmoingay.com/?s={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MonNgonCrawler/1.0; +https://yourdomain.example)"
    }

    try:
        r = requests.get(search_url, headers=headers, timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Lỗi tìm kiếm: {e}")

    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", href=True)

    recipe_url_pattern = re.compile(r"https://monngonmoingay.com/(?!tim-kiem-mon-ngon|thuc-don-dinh-duong|mach-nho|ke-hoach-nau-an|gia-vi-ban-can|lich-phat-song|tich-diem-doi-qua|lay-lai-mat-khau|category|tag|author|date|page|comment|feed)[^/]+/+$")

    for link in links:
        url = link.get("href")
        title = link.get_text(strip=True)

        if url and title and recipe_url_pattern.match(url):
            # Trả về link đầu tiên tìm được
            return {"title": title, "url": url}
    
    # Nếu không tìm thấy link nào
    return {"title": None, "url": None, "message": "Không tìm thấy công thức phù hợp"}


@tool
def scrape_monngonmoingay(url: str):
    """
    Cào chi tiết công thức món ăn từ một URL trên monngonmoingay.com.
    Trả về các section: nguyên liệu, sơ chế, thực hiện, cách dùng, mẹo hay.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MonNgonCrawler/1.0; +https://yourdomain.example)"
    }
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        raise Exception(f"Lỗi tải trang: {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")
    sections = ["nguyenlieu", "soche", "thuchien", "howtouse", "tips"]

    data = {"url": url}

    for sec in sections:
        div = soup.find("div", id=f"section-{sec}")
        if not div:
            continue
        # Ghép toàn bộ text trong div (bao gồm <li>, <p>, <span>...)
        parts = []
        for tag in div.find_all(["p", "li"]):
            txt = tag.get_text(" ", strip=True)
            if txt:
                parts.append(txt)
        data[sec] = parts

    return data