import json
import os
import requests
from langchain.tools import tool
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
class SearchTools():

    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet
        about a a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # check if there is an organic key
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with you serper api key."
        else:
            results = response.json()['organic']
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next

        return '\n'.join(string)

def website_search_tool(website: str = 'https://toyota.com'):
    return WebsiteSearchTool(website=website, 
                    config=dict(llm=dict(
                        provider="groq", # or google, openai, anthropic, llama2, ...
                        config=dict(
                            model="llama-3.3-70b-versatile",
                            # temperature=0.5,
                            # top_p=1,
                            # stream=true,
                        ),
                        ),
                        embedder = dict(
                            provider = "huggingface",        # local sentence-transformers
                            config = dict(
                                model = "sentence-transformers/all-MiniLM-L6-v2",
                                # task_type = "retrieval_document",
                            ),
                        ),
                    )
                )