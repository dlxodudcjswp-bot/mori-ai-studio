from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    title: str
    status: str = "Todo"
    assignee: str = "Unassigned"
    priority: str = "Medium"


class TaskManager:
    def __init__(self) -> None:
        self.tasks: list[Task] = [
            Task(id="TASK-001", title="Task-008 Task Board", status="Todo", assignee="PM", priority="High"),
            Task(id="TASK-002", title="Issue Tracker", status="In Progress", assignee="Developer", priority="Medium"),
            Task(id="TASK-003", title="AI Workflow", status="Done", assignee="Designer", priority="Low"),
        ]

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
