from agency_swarm.agents import Agent


class ResearchCEO(Agent):
    def __init__(self):
        super().__init__(
            name="ResearchCEO",
            description="Oversee the operations, coordinate tasks, and ensure the information gathered meets the required standards.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
            model = "gpt-4o",
        )
        
    def response_validator(self, message):
        return message

    def curate_news(self, news_articles):
        # Implement logic to select the top 5 news articles from the 10 provided
        curated_news = sorted(news_articles, key=lambda x: x['relevance'], reverse=True)[:5]
        return curated_news