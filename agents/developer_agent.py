from crewai import Agent

developer_agent = Agent(
    role='Developer Agent',
    goal='Implement the dashboard design using HTML, CSS, and JavaScript.',
    backstory='You are a skilled frontend developer, able to bring any design to life with code.',
    verbose=True,
)
