from pydantic import BaseModel, Field
from typing import List
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