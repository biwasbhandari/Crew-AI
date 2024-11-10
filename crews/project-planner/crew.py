from crewai import Agent, Task, Crew
import yaml
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from db.client import supabase

# LOAD DOTENV FILES
load_dotenv()

# FILE PATHS FOR YAML CONFIGURATIONS
files = {
    'agents': 'crews/project-planner/config/agents.yaml',
    'tasks': 'crews/project-planner/config/tasks.yaml'
}
print(files)

# LOAD CONFIGURATION FROM YAML FILES
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# ASSIGN LOADED CONFIGURATION TO SPECIFIC VARIABLES
agents_config = configs['agents']
tasks_config = configs['tasks']

# CREATE PYDANTIC MODELS FOR STRUCTURED OUTPUT
class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(..., description="Estimated time to complete the task")
    required_resources: List[str] = Field(..., description="List of resources")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description="name of the milestone")
    tasks: List[str] = Field(..., description="List of task IDs associated with this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description="List of project milestones")

# CREATE AGENTS
project_planning_agent = Agent(
    role=agents_config['project_planning_agent']['role'],
    goal=agents_config['project_planning_agent']['goal'],
    backstory=agents_config['project_planning_agent']['backstory']
)

estimation_agent = Agent(
    role=agents_config['estimation_agent']['role'],
    goal=agents_config['estimation_agent']['goal'],
    backstory=agents_config['estimation_agent']['backstory']
)

resource_allocation_agent = Agent(
    role=agents_config['resource_allocation_agent']['role'],
    goal=agents_config['resource_allocation_agent']['goal'],
    backstory=agents_config['resource_allocation_agent']['backstory']
)

# CREATE TASKS
task_breakdown = Task(
    description=tasks_config['task_breakdown']['description'],
    expected_output=tasks_config['task_breakdown']['expected_output'],
    agent=project_planning_agent
)

time_resource_estimation = Task(
    description=tasks_config['time_resource_estimation']['description'],
    expected_output=tasks_config['time_resource_estimation']['expected_output'],
    agent=estimation_agent
)

resource_allocation = Task(
    description=tasks_config['resource_allocation']['description'],
    expected_output=tasks_config['resource_allocation']['expected_output'],
    agent=resource_allocation_agent,
    output_pydantic=ProjectPlan
)

# CREATE CREW
crew = Crew(
    agents=[project_planning_agent, estimation_agent, resource_allocation_agent],
    tasks=[task_breakdown, time_resource_estimation, resource_allocation],
    verbose=True
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
print(result)
