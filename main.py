from crewai import Crew, Process
from agents.coordinator_agent import coordinator_agent
from agents.researcher_agent import researcher_agent
from agents.data_analyst_agent import data_analyst_agent
from agents.visualizer_agent import visualizer_agent
from agents.developer_agent import developer_agent
from agents.validator_agent import validator_agent
from tasks import research_task, analysis_task, visualization_task, development_task, validation_task

# Form the crew
crew = Crew(
    agents=[coordinator_agent, researcher_agent, data_analyst_agent, visualizer_agent, developer_agent, validator_agent],
    tasks=[research_task, analysis_task, visualization_task, development_task, validation_task],
    process=Process.sequential,
    full_output=True,
    verbose=True,
)

if __name__ == '__main__':
    # Start the crew's work
    result = crew.kickoff()
    print("######################")
    print("## Here is the result")
    print("######################")
    print(result)
