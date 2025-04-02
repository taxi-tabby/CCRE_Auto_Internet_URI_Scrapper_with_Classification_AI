#https://i.ytimg.com/vi/HbvjfRPFjyg/hqdefault.jpg

import sys
import os


# 테스트용 루트 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Source start line

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.crawing import fetch_with_redirects
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.mime import get_mime_type_from_binary

import asyncio

async def test_fetch_with_redirects():
    data = await fetch_with_redirects(
        url="https://i.ytimg.com/vi/HbvjfRPFjyg/hqdefault.jpg",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    )
    content_type = data['content_type']
    http_body = data['body']
    

    print(f"HTTP Status Code: {data['status_code']}")
    # Ensure the binary data is passed correctly
    if isinstance(http_body, bytes):
        mime = get_mime_type_from_binary(http_body)
        print(f"{http_body}")
    else:
        mime = get_mime_type_from_binary(http_body.encode())
        print(f"{http_body.encode()}")
    

    if mime == "application/octet-stream" and content_type != mime:
        mime = content_type

    
    # Debugging: Print the first few bytes of the binary data
    print(f"First 20 bytes of the binary data: {http_body[:20] if isinstance(http_body, bytes) else http_body.encode()[:20]}")
    
    print(f"Detected MIME type: {mime}")
    

if __name__ == "__main__":
    asyncio.run(test_fetch_with_redirects())
#-------------------------------------------------------------------------------
