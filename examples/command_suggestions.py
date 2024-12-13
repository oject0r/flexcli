from flexcli import DynamicCLI

cli = DynamicCLI()

# Define simple commands
def start():
    """Starts the process."""
    print("Process started.")

def stop():
    """Stops the process."""
    print("Process stopped.")

def restart():
    """Restarts the process."""
    print("Process restarted.")

# Register commands
cli.register_command("start", start, doc=start.__doc__)
cli.register_command("stop", stop, doc=stop.__doc__)
cli.register_command("restart", restart, doc=restart.__doc__)

if __name__ == "__main__":
    args = input("Enter command: ").split()
    command_name = args[0] if args else ""

    # Suggest commands if an invalid command is entered
    if command_name not in cli.list_commands():
        suggestions = cli.complete_command(command_name)
        if suggestions:
            print(f"Did you mean: {', '.join(suggestions)}?")
        else:
            print("Unknown command.")
    else:
        cli.run(args)
