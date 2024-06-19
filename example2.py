from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import os
import json

class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.name = "NewsAPI Pipeline"

    async def on_startup(self):
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")
        pass

def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
    # This is where you can add your custom pipelines like RAG.
    print(f"pipe:{__name__}")
    
    if body.get("title", False):
        print("Title Generation")
        return "NewsAPI Pipeline"
    else:
        articles = []  # Initialize the list before the loop
        for query in [user_message]:
            url = f"https://newsapi.org/v2/everything?q={query}&pageSize=5&apiKey={os.getenv('NEWS_API_KEY', '')}"
            
            r = requests.get(url)
            
            response = json.loads(r.text)
            articles = articles + response['articles'][:5]  # get first 5 articles
            print(articles)
        
        content = []
        for article in articles:
            if 'content' not in article:
                content.append(article['description'])
            else:
                content.append(article['content'])
            
        return '\n'.join(content)
