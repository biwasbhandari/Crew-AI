from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from db.client import supabase

# LOAD DOTENV FILES
load_dotenv()

# FILE PATHS FOR YAML CONFIGURATIONS
# files = {
#     'agents': 'crews/project-planner/config/agents.yaml',
#     'tasks': 'crews/project-planner/config/tasks.yaml'
# }
# print(files)

# # LOAD CONFIGURATION FROM YAML FILES
# configs = {}
# for config_type, file_path in files.items():
#     with open(file_path, 'r') as file:
#         configs[config_type] = yaml.safe_load(file)

# # ASSIGN LOADED CONFIGURATION TO SPECIFIC VARIABLES
# agents_config = configs['agents']
# tasks_config = configs['tasks']

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
    role="The Ultimate Project Planner",
    goal="To breakdown the {project_type} into actionable tasks, ensuring no detail is overlooked, and setting precise timelines that aligns with {project_objective}",
    backstory="As a veteran project planner you've succesfully led multiple projects, particularly in {industry}. Your keen eye for detail and strategic thinking have always ensured that projects are delivered on time and within scope. Now you're tasked with planning next groundbreaking {project_type} project.",
    allow_delegation=False,
    verbose=False
)

estimation_agent = Agent(
    role="Expert Estimation Analyst",
    goal="Provide highly accurate time, resource, and effort estimations for each task in the {project_type} project to ensure it is delivered efficently and on budget.",
    backstory=" You are the go-to expert for project estimation in {industry}. With a wealth of expereience and access to vast historical data, you can predict the resources required for any task with remarkable accuracy.Your precision ensures that the {project_type} remains feasible and avoids unnecessary delays or budget overruns.",
    allow_delegation=False,
    verbose=False
)

resource_allocation_agent = Agent(
    role="Strategic Resource Allocation Specialist",
    goal=" Develop a resource allocation plan that precisely identifies and assigns resources to each task in the {project_type} project. Ensure optimal resource use to meet {project_objective} while maintaining efficiency and cost-effectiveness.",
    backstory="With extensive experience in {industry} and a track record in managing resource-heavy projects, you are adept at orchestrating the assignment of people, budget, and equipment to align with project requirements. Your goal is to balance the resource demands for the {project_type} to avoid bottlenecks and ensure seamless project progress. You work closely with the planning and estimation teams to confirm that all resource allocations are practical, feasible, and support the project's strategic objectives.",
    allow_delegation=False,
    verbose=False
)

# CREATE TASKS
task_breakdown = Task(
    description="Carefully analyze the following project requiements:\n {project_requirements} for the {project_type} project and break them into individual tasks. Define each task's scope indetail, set achievable timelines, and ensuer that all dependencies are accounted for:\n{project_requirements}Team members:{team_members}",
    expected_output="A comprehensive list of tasks with detailed descriptions, timelines, dependencies, and deliverables. Your final output MUST include a Gantt chart or similar timeline visualization specific to the {project_type} project.",
    agent=project_planning_agent
)

time_resource_estimation = Task(
    description="Thoroughly evaluate each task in the {project_type} project to estimate the time, resources and effort required. Use historical data, task complexity, and available resources to provide a realistic estimation of each tasks.",
    expected_output="A detailed estimation report outlining the time, resources, and effort required for each task in the {project_type} project. Your final report MUST include a summary of any risks or uncertainties associated with the estimations.",
    agent=estimation_agent
)

resource_allocation = Task(
    description="Analyze the detailed task breakdown and time/resource estimations for the {project_type} project. Develop a strategic resource allocation plan by assigning \n{team_members}, and equipment to each task. Ensure the allocation is balanced to avoid bottlenecks, addresses all dependencies, and maximizes efficiency to meet \n{project_objective} while staying within budget. Factor in skill levels, availability of resources, and any constraints from \n {project_requirements} to optimize the allocation.",
    expected_output="A complete resource allocation report, detailing the assignment of team members, budget, and equipment for each task in the {project_type} project. The final report MUST include an overview of resource distribution, a chart visualizing allocation across the project timeline, and an identification of potential resource conflicts or shortages, with proposed resolutions.",
    agent=resource_allocation_agent,
    output_pydantic=ProjectPlan
)

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