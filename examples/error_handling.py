from flexcli import DynamicCLI

cli = DynamicCLI()

# Command with error handling
def divide(a: str, b: str):
    """Divides two numbers and prints the result."""
    try:
        result = float(a) / float(b)
        print(f"The result of {a} / {b} is {result}")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except ValueError:
        print("Error: Please provide valid numbers.")

# Register command
cli.register_command("divide", divide, doc=divide.__doc__)

if __name__ == "__main__":
    cli.run()
