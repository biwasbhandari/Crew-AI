from crewai import Crew
from dotenv import load_dotenv
from db.client import supabase
from crews.project_planner.agent import project_planning_agent, estimation_agent, resource_allocation_agent
from crews.project_planner.task import task_breakdown, time_resource_estimation, resource_allocation
# LOAD DOTENV FILES
load_dotenv()

# CREATE CREW
crew = Crew(
    agents=[project_planning_agent, estimation_agent, resource_allocation_agent],
    tasks=[task_breakdown, time_resource_estimation, resource_allocation],
    # verbose=False
)

# ADD INPUTS FROM SUPABASE
data = supabase.table('test').select("*").eq('id', 1).execute().data[0]
project = data['project']
industry = data['industry']
project_objective = data['project_objective']
team_members = data['team_members']
project_requirements = data['project_requirements']

# print(project, industry, project_objective, team_members, project_requirements)

inputs = {
    'project_type': project,
    'industry':industry,
    'project_objective': project_objective,
    'team_members': team_members,
    'project_requirements': project_requirements
}

# KICK OFF THE CREW
result = crew.kickoff(inputs=inputs)
print(task_breakdown.output)
print(time_resource_estimation.output)
print(resource_allocation.output)