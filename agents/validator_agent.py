from crewai import Agent

validator_agent = Agent(
    role='Validator Agent',
    goal='Test and validate the dashboard for quality, performance, and compatibility.',
    backstory='You are a meticulous QA engineer, dedicated to ensuring the highest quality standards.',
    verbose=True,
)
