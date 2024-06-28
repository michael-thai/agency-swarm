from agency_swarm import Agent
from .tools.DuckDuckGoSearchTools import DuckDuckGoSearchTools
from .tools.YFinanceTools import YFinanceTools

class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Retrieve information from the web and financial APIs.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[DuckDuckGoSearchTools, YFinanceTools],

            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            model = "gpt-3.5-turbo",
        )
        
    def response_validator(self, message):
        return message

    def gather_news(self, company_name):
        # Implement logic to retrieve 10 news articles about the company
        news_articles = DuckDuckGoSearchTools.search(company_name, num_results=10, filter='past 6 months')
        return news_articles