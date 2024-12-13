from flexcli import DynamicCLI

cli = DynamicCLI()

# Define a command with aliases
def add_numbers(a: str, b: str):
    """Adds two numbers and prints the result."""
    result = float(a) + float(b)
    print(f"The result of {a} + {b} is {result}")

# Register command with aliases
cli.register_command("add", add_numbers, aliases={"sum", "plus"}, doc=add_numbers.__doc__)

if __name__ == "__main__":
    cli.run()
