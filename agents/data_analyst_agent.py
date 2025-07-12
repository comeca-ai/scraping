from crewai import Agent

data_analyst_agent = Agent(
    role='Data Analyst Agent',
    goal='Process and analyze data to extract insights and metrics.',
    backstory='You are a data wizard, able to find patterns and meaning in any dataset.',
    verbose=True,
)
