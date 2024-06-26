from agency_swarm import Agency
from ResearchAgent import ResearchAgent
from ResearchCEO import ResearchCEO

from dotenv import load_dotenv
load_dotenv()

research_ceo = ResearchCEO()
research_agent = ResearchAgent()


agency = Agency([
    research_ceo, 
    research_agent, 
    [research_ceo, research_agent]
    ],
        shared_instructions='./agency_manifesto.md', # shared instructions for all agents
        max_prompt_tokens=25000, # default tokens in conversation for all agents
        temperature=0.3, # default temperature for all agents
        )
                
if __name__ == '__main__':
    # agency.demo_gradio(
    #     # height=900, 
    #     debug=True 
    # )
    agency.run_demo()    # Terminal version
    # completion_output = agency.get_completion("Please search company", abc)    # Terminal version
