from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool

researcher_agent = Agent(
    role='Researcher Agent',
    goal='Collect and extract relevant data from the web.',
    backstory='You are an expert in finding and extracting information from various web sources.',
    verbose=True,
    tools=[
        SerperDevTool(),
        WebsiteSearchTool()
    ]
)
