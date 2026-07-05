from dataclasses import dataclass

from src.core.storage import Storage


@dataclass
class WorkflowStep:
    step_name: str
    assigned_agent: str
    status: str = "Pending"


class WorkflowEngine:
    def __init__(self, storage: Storage | None = None) -> None:
        self.storage = storage or Storage()
        self.steps = self._load()

    def _load(self) -> list[WorkflowStep]:
        data = self.storage.load_json("workflow.json")
        if isinstance(data, list) and data:
            return [WorkflowStep(**step) for step in data]

        default_steps = [
            WorkflowStep(step_name="PM Review", assigned_agent="PM", status="Done"),
            WorkflowStep(step_name="Design", assigned_agent="Designer", status="Pending"),
            WorkflowStep(step_name="Development", assigned_agent="Developer", status="Pending"),
            WorkflowStep(step_name="QA", assigned_agent="QA", status="Pending"),
            WorkflowStep(step_name="PM Approval", assigned_agent="PM", status="Pending"),
        ]
        self._save(default_steps)
        return default_steps

    def _save(self, steps: list[WorkflowStep]) -> None:
        payload = [
            {
                "step_name": step.step_name,
                "assigned_agent": step.assigned_agent,
                "status": step.status,
            }
            for step in steps
        ]
        self.storage.save_json("workflow.json", payload)

    def save(self) -> None:
        self._save(self.steps)

    def get_status_lines(self) -> list[str]:
        return [f"{step.step_name}: {step.status}" for step in self.steps]

    def format_workflow(self) -> str:
        return "\n".join(["Mori Workflow", *self.get_status_lines()])
