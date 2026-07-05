from dataclasses import dataclass


@dataclass
class WorkflowStep:
    step_name: str
    assigned_agent: str
    status: str = "Pending"


class WorkflowEngine:
    def __init__(self) -> None:
        self.steps = [
            WorkflowStep(step_name="PM Review", assigned_agent="PM", status="Done"),
            WorkflowStep(step_name="Design", assigned_agent="Designer", status="Pending"),
            WorkflowStep(step_name="Development", assigned_agent="Developer", status="Pending"),
            WorkflowStep(step_name="QA", assigned_agent="QA", status="Pending"),
            WorkflowStep(step_name="PM Approval", assigned_agent="PM", status="Pending"),
        ]

    def get_status_lines(self) -> list[str]:
        return [f"{step.step_name}: {step.status}" for step in self.steps]

    def format_workflow(self) -> str:
        return "\n".join(["Mori Workflow", *self.get_status_lines()])
