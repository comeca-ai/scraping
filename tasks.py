from crewai import Task
from agents.researcher_agent import researcher_agent
from agents.data_analyst_agent import data_analyst_agent
from agents.visualizer_agent import visualizer_agent
from agents.developer_agent import developer_agent
from agents.validator_agent import validator_agent

research_task = Task(
    description='Research the web for the main strategic issues for Rafael Luchini at the Ultra Group in the Brazilian government.',
    expected_output='A detailed report on the main strategic issues, including key stakeholders and regulations.',
    agent=researcher_agent
)

analysis_task = Task(
    description='Analyze the research report to extract key insights, metrics, and patterns.',
    expected_output='A structured analysis of the data, including a summary of key findings and a list of relevant metrics.',
    agent=data_analyst_agent
)

visualization_task = Task(
    description='Design a dashboard layout and visualizations based on the analysis.',
    expected_output='A detailed specification of the dashboard, including chart types, layout, and color scheme.',
    agent=visualizer_agent
)

development_task = Task(
    description='Implement the dashboard design using HTML, CSS, and JavaScript.',
    expected_output='A fully functional and interactive dashboard as a single HTML file.',
    agent=developer_agent
)

validation_task = Task(
    description='Validate the dashboard for quality, performance, and compatibility.',
    expected_output='A validation report with a summary of findings and a list of any issues found.',
    agent=validator_agent
)
