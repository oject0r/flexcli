import asyncio
from flexcli import DynamicCLI

cli = DynamicCLI()

# Define a synchronous command
def echo(message: str):
    """Echoes back the provided message."""
    print(f"You said: {message}")

# Define an asynchronous command
async def async_timer(seconds: int):
    """Waits for the specified number of seconds asynchronously."""
    for i in range(int(seconds), 0, -1):
        print(f"{i} seconds remaining...")
        await asyncio.sleep(1)
    print("Time's up!")

# Register both commands
cli.register_command("echo", echo, doc=echo.__doc__)
cli.register_command("timer", async_timer, async_handler=True, doc=async_timer.__doc__)

if __name__ == "__main__":
    cli.run()
