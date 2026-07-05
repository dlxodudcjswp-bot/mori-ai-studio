import discord


def start_discord_bot(token: str) -> None:
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        print(f"Logged in as {client.user} (ID: {client.user.id})")

    client.run(token)
