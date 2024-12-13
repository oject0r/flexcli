import asyncio
from flexcli import DynamicCLI

cli = DynamicCLI()

# Define a synchronous command
def greet(name: str = "world"):
    """Greets the user with a customizable message."""
    print(f"Hello, {name}!")

# Define an asynchronous command
async def countdown(start: int = 5):
    """Counts down from a specified number asynchronously."""
    for i in range(int(start), 0, -1):
        print(i)
        await asyncio.sleep(1)
    print("Countdown complete!")

# Register commands
cli.register_command("greet", greet, doc=greet.__doc__)
cli.register_command("countdown", countdown, async_handler=True, doc=countdown.__doc__)

if __name__ == "__main__":
    cli.run()
