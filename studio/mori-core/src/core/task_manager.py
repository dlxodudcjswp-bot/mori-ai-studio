from dataclasses import dataclass

from src.core.agent_manager import AgentManager
from src.core.storage import Storage


@dataclass
class Task:
    id: str
    title: str
    status: str = "Todo"
    assignee: str = "Unassigned"
    priority: str = "Medium"


class TaskManager:
    def __init__(self, storage: Storage | None = None, agent_manager: AgentManager | None = None) -> None:
        self.storage = storage or Storage()
        self.agent_manager = agent_manager or AgentManager(storage=self.storage)
        self.tasks = self._load()

    def _load(self) -> list[Task]:
        data = self.storage.load_json("tasks.json")
        if isinstance(data, list) and data:
            return [Task(**task) for task in data]

        default_tasks = [
            Task(id="TASK-001", title="Task-008 Task Board", status="Todo", assignee="PM", priority="High"),
            Task(id="TASK-002", title="Issue Tracker", status="In Progress", assignee="Developer", priority="Medium"),
            Task(id="TASK-003", title="AI Workflow", status="Done", assignee="Designer", priority="Low"),
        ]
        self._save(default_tasks)
        return default_tasks

    def _save(self, tasks: list[Task]) -> None:
        payload = [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "assignee": task.assignee,
                "priority": task.priority,
            }
            for task in tasks
        ]
        self.storage.save_json("tasks.json", payload)

    def save(self) -> None:
        self._save(self.tasks)

    def refresh(self) -> None:
        self.tasks = self._load()

    def get_task(self, task_id: str) -> Task | None:
        return next((task for task in self.tasks if task.id == task_id), None)

    def update_task_status(self, task_id: str, status: str) -> Task | None:
        task = self.get_task(task_id)
        if task is None:
            return None

        task.status = status
        self.save()
        return task

    def create_task(self, title: str, assignee: str, priority: str) -> Task:
        next_number = len(self.tasks) + 1
        task_id = f"TASK-{next_number:03d}"
        task = Task(id=task_id, title=title, status="Todo", assignee=assignee, priority=priority)
        self.tasks.append(task)
        self.save()
        return task

    def assign_task(self, task_id: str, assignee: str) -> Task | None:
        task = self.get_task(task_id)
        if task is None:
            return None

        allowed_assignees = {"PM", "Designer", "Developer", "QA"}
        if assignee not in allowed_assignees:
            raise ValueError("Unknown assignee")

        task.assignee = assignee
        self.save()
        self.agent_manager.sync_task_assignment(task.id, assignee)
        return task

    def get_tasks_by_status(self, status: str) -> list[Task]:
        return [task for task in self.tasks if task.status == status]

    def get_status_groups(self) -> dict[str, list[Task]]:
        return {
            "Todo": self.get_tasks_by_status("Todo"),
            "In Progress": self.get_tasks_by_status("In Progress"),
            "Done": self.get_tasks_by_status("Done"),
        }

    def format_board(self) -> str:
        sections: list[str] = []
        for status in ["Todo", "In Progress", "Done"]:
            tasks = self.get_tasks_by_status(status)
            lines = [f"{status}:"]
            if tasks:
                lines.extend([f"- {task.title} ({task.id}) - {task.assignee} - {task.priority}" for task in tasks])
            else:
                lines.append("- None")
            sections.append("\n".join(lines))
        return "\n\n".join(sections)
