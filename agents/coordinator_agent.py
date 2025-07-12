from crewai import Agent

coordinator_agent = Agent(
    role='Coordinator Agent',
    goal='Coordinate the workflow between all other agents.',
    backstory='You are a master of project management, able to orchestrate complex workflows with multiple agents.',
    verbose=True,
    allow_delegation=True
)
