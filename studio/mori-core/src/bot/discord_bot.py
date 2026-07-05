import discord


class MoriClient(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self._register_commands()

    def _register_commands(self) -> None:
        @self.tree.command(name="ping", description="Respond with a pong")
        async def ping_command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message("🏓 Pong!")

        @self.tree.command(name="status", description="Show Mori Core status")
        async def status_command(interaction: discord.Interaction) -> None:
            message = (
                "Mori Core v0.3\n"
                "PM: Idle\n"
                "Developer: Idle\n"
                "Designer: Idle\n"
                "QA: Idle"
            )
            await interaction.response.send_message(message)

        @self.tree.command(name="help", description="Show available commands")
        async def help_command(interaction: discord.Interaction) -> None:
            message = (
                "Available commands:\n"
                "- /ping\n"
                "- /status\n"
                "- /help"
            )
            await interaction.response.send_message(message)

    async def setup_hook(self) -> None:
        await self.tree.sync()


def build_command_tree() -> discord.app_commands.CommandTree:
    intents = discord.Intents.default()
    client = MoriClient(intents=intents)
    return client.tree


def start_discord_bot(token: str) -> None:
    intents = discord.Intents.default()
    client = MoriClient(intents=intents)

    @client.event
    async def on_ready() -> None:
        print(f"Logged in as {client.user} (ID: {client.user.id})")

    client.run(token)
