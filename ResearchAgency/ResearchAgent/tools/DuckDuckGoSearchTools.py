from agency_swarm.tools import BaseTool
from pydantic import Field
from duckduckgo_search import DDGS
import datetime

class DuckDuckGoSearchTools(BaseTool):
    """
    A tool to perform web searches using DuckDuckGo, specifically retrieving general information or news articles within the last 6 months.
    """
    query: str = Field(..., description="The search query to be sent to DuckDuckGo.")
    search_type: str = Field(..., description="Type of search: 'info' for general information or 'news' for news articles.")
    date_range: int = Field(6, description="The number of months to look back for news articles (only relevant for news search).")

    def run(self):
        """
        Executes the search query using DuckDuckGo's search API and returns the results.
        """
        ddg = DDGS()
        
        if self.search_type == 'news':
            # Calculate the start date for the search range (6 months ago)
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=self.date_range * 30)
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # Perform the search for news
            search_query = f"{self.query} business news"
            results = ddg.news(search_query)
            news_results = []

            # Keywords to filter out stock-related articles
            exclude_keywords = ['stock', 'share', 'valuation', 'earnings', 'dividend']

            for result in results:
                pub_date = datetime.datetime.strptime(result['date'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)

                if start_date <= pub_date <= end_date:
                    if not any(keyword in result['title'].lower() for keyword in exclude_keywords):
                        news_results.append({
                            "date": result.get('date', 'N/A'),
                            "headline": result.get('title', 'N/A'),
                            "summary": result.get('body', 'N/A'),
                            "link": result.get('url', 'N/A')
                        })

            return news_results if news_results else "No recent business news articles found within the specified date range."

        elif self.search_type == 'info':
            # Perform the search for general information
            search_query = self.query
            results = ddg.text(search_query)
            info_results = []

            for result in results:
                info_results.append({
                    "title": result.get('title', 'N/A'),
                    "summary": result.get('body', 'N/A'),
                    "link": result.get('url', 'N/A')
                })

            return info_results if info_results else "No information found for the query."

        else:
            return "Invalid search type. Please specify 'info' for general information or 'news' for news articles."

# Simple test
# if __name__ == '__main__':
#     # Test for news search
    # tool_news = DuckDuckGoSearchTools(query="Palantir", search_type="news")
    # news_results = tool_news.run()

    # if isinstance(news_results, list):
    #     for news in news_results:
    #         print(f"Date: {news['date']}")
    #         print(f"Headline: {news['headline']}")
    #         print(f"Summary: {news['summary']}")
    #         print(f"Link: {news['link']}\n")
    # else:
    #     print(news_results)


    # # Test for information search
    # tool_info = DuckDuckGoSearchTools(query="Palantir", search_type="info")
    # info_results = tool_info.run()

    # if isinstance(info_results, list):
    #     for info in info_results:
    #         print(f"Title: {info['title']}")
    #         print(f"Summary: {info['summary']}")
    #         print(f"Link: {info['link']}\n")
    # else:
    #     print(info_results)

# class DuckDuckGoSearchTools(BaseTool):
#     """
#     A tool to perform web searches using DuckDuckGo.
#     """
#     query: str = Field(..., description="The search query to be sent to DuckDuckGo.")

#     def run(self):
#         """
#         Executes the search query using DuckDuckGo's search API and returns the results.
#         """
#         ddg = DDGS()
#         results = ddg.text(self.query)
#         if results:
#             return results[0]['body']
#         else:
#             return "No results found"
