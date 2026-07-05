from dataclasses import dataclass

from src.core.storage import Storage


@dataclass
class Agent:
    name: str
    role: str
    status: str = "Idle"
    current_task: str = "None"


class AgentManager:
    def __init__(self, storage: Storage | None = None) -> None:
        self.storage = storage or Storage()
        self.agents = self._load()

    def _load(self) -> dict[str, Agent]:
        data = self.storage.load_json("agents.json")
        if not isinstance(data, dict):
            data = {}

        if data:
            return {
                key: Agent(
                    name=agent.get("name", "Agent"),
                    role=agent.get("role", "Agent"),
                    status=agent.get("status", "Idle"),
                    current_task=agent.get("current_task", "None"),
                )
                for key, agent in data.items()
            }

        default_agents = {
            "pm": Agent(name="PM", role="Project Manager", status="Idle", current_task="None"),
            "designer": Agent(name="Designer", role="Design", status="Idle", current_task="None"),
            "developer": Agent(name="Developer", role="Development", status="Idle", current_task="None"),
            "qa": Agent(name="QA", role="Quality Assurance", status="Idle", current_task="None"),
        }
        self._save(default_agents)
        return default_agents

    def _save(self, agents: dict[str, Agent]) -> None:
        payload = {
            key: {
                "name": agent.name,
                "role": agent.role,
                "status": agent.status,
                "current_task": agent.current_task,
            }
            for key, agent in agents.items()
        }
        self.storage.save_json("agents.json", payload)

    def save(self) -> None:
        self._save(self.agents)

    def get_agent(self, key: str) -> Agent | None:
        return self.agents.get(key)

    def get_all_agents(self) -> list[Agent]:
        return [self.agents[key] for key in ("pm", "designer", "developer", "qa")]

    def get_status_lines(self) -> list[str]:
        return [f"{agent.name}: {agent.status}" for agent in self.get_all_agents()]
