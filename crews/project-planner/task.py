from crewai import Task
from .agent import project_planning_agent, estimation_agent, resource_allocation_agent
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
