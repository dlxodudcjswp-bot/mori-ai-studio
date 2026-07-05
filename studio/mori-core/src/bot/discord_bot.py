import os

import discord


async def sync_commands(tree: discord.app_commands.CommandTree, *, guild_id: str | None = None) -> int:
    resolved_guild_id = guild_id if guild_id is not None else os.getenv("DISCORD_GUILD_ID", "").strip()
    guild = None
    use_guild_sync = bool(resolved_guild_id)

    if use_guild_sync:
        try:
            guild = discord.Object(id=int(resolved_guild_id))
        except ValueError:
            print(f"Invalid DISCORD_GUILD_ID value: {resolved_guild_id}")
            use_guild_sync = False

    print("Sync starting...")
    print(f"Guild Sync: {'Yes' if use_guild_sync else 'No'}")

    try:
        if use_guild_sync:
            synced = await tree.sync(guild=guild)
        else:
            synced = await tree.sync()
    except Exception as exc:  # pragma: no cover - runtime safety path
        print(f"Slash command sync failed: {exc}")
        raise

    count = len(synced)
    print(f"Registered Slash Commands: {count}")
    return count


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
                "Mori Core v0.4\n"
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
                "- /help\n"
                "- /pm\n"
                "- /designer\n"
                "- /developer\n"
                "- /qa"
            )
            await interaction.response.send_message(message)

        @self.tree.command(name="pm", description="Notify the PM agent")
        async def pm_command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message("💼 PM Agent is ready.")

        @self.tree.command(name="designer", description="Notify the Designer agent")
        async def designer_command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message("🎨 Designer Agent is ready.")

        @self.tree.command(name="developer", description="Notify the Developer agent")
        async def developer_command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message("💻 Developer Agent is ready.")

        @self.tree.command(name="qa", description="Notify the QA agent")
        async def qa_command(interaction: discord.Interaction) -> None:
            await interaction.response.send_message("🧪 QA Agent is ready.")

    async def setup_hook(self) -> None:
        guild_id = os.getenv("DISCORD_GUILD_ID", "").strip()
        await sync_commands(self.tree, guild_id=guild_id or None)


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
        guild_id = os.getenv("DISCORD_GUILD_ID", "").strip()
        await sync_commands(client.tree, guild_id=guild_id or None)

    client.run(token)
