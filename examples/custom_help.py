from flexcli import DynamicCLI

cli = DynamicCLI()

# Define a simple command
def greet(name: str = "world"):
    """Greets the user by name or defaults to 'world'."""
    print(f"Hello, {name}!")

# Register the command with documentation
cli.register_command("greet", greet, doc=greet.__doc__)

if __name__ == "__main__":
    cli.run()
