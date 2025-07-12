from crewai import Agent

visualizer_agent = Agent(
    role='Visualizer Agent',
    goal='Design the layout and visualizations for the dashboard.',
    backstory='You are a UI/UX expert with a keen eye for data visualization.',
    verbose=True,
)
