from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    role: str
    status: str = "Idle"
    current_task: str = "None"


class AgentManager:
    def __init__(self) -> None:
        self.agents = {
            "pm": Agent(name="PM", role="Project Manager", status="Idle", current_task="None"),
            "designer": Agent(name="Designer", role="Design", status="Idle", current_task="None"),
            "developer": Agent(name="Developer", role="Development", status="Idle", current_task="None"),
            "qa": Agent(name="QA", role="Quality Assurance", status="Idle", current_task="None"),
        }

    def get_agent(self, key: str) -> Agent | None:
        return self.agents.get(key)

    def get_all_agents(self) -> list[Agent]:
        return [self.agents[key] for key in ("pm", "designer", "developer", "qa")]

    def get_status_lines(self) -> list[str]:
        return [f"{agent.name}: {agent.status}" for agent in self.get_all_agents()]
