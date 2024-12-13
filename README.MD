# FlexCLI

**FlexCLI** is a lightweight, ultra-fast Python library for building command-line interfaces (CLIs) with minimal overhead and maximum flexibility. It supports both synchronous and asynchronous commands, detailed documentation for commands, aliases, and more.

---

## Features

- **Synchronous and Asynchronous Commands**: Supports both sync and async handlers.
- **Command Aliases**: Flexible invocation of commands using alternative names.
- **Detailed Help Documentation**: Provides per-command and global help output.
- **Command Suggestions**: Offers suggestions for similar commands when input is incorrect.
- **Minimal Overhead**: Lightweight and fast with no unnecessary dependencies.

---

## Installation

Simply include the `flexcli.py` file in your project folder:

```bash
# Clone the repository
git clone https://github.com/oject0r/flexcli.git

# Move flexcli.py into your project folder
```

---

## Basic Usage

### Example

```python
from flexcli import DynamicCLI
import asyncio

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
```

### Run the CLI

Save the above code in `example.py` and execute it with:

```bash
python example.py greet Alice
```

Output:

```
Hello, Alice!
```

---

## Advanced Features

### Command Aliases

Define aliases for commands to allow flexible invocation:

```python
cli.register_command("add", add_numbers, aliases={"sum", "plus"}, doc=add_numbers.__doc__)
```

### Detailed Command Documentation

FlexCLI provides detailed per-command help documentation:

```bash
python example.py greet --help
```

Output:

```
Help for command 'greet':
Greets the user with a customizable message.
```

### Error Handling

Commands can handle errors gracefully:

```python
def divide(a: str, b: str):
    try:
        result = float(a) / float(b)
        print(f"The result of {a} / {b} is {result}")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except ValueError:
        print("Error: Please provide valid numbers.")
```

### Command Suggestions

If a user inputs an incorrect or incomplete command, FlexCLI can suggest similar commands:

```python
suggestions = cli.complete_command("sta")
print(f"Did you mean: {', '.join(suggestions)}?")
```

---

## Examples

### Example Files

| **File Name**         | **Description**                                                                                     |
|------------------------|-----------------------------------------------------------------------------------------------------|
| `basic_usage.py`       | Introduces basic usage of synchronous and asynchronous commands.                                    |
| `command_aliases.py`   | Demonstrates command aliases for flexible invocation.                                              |
| `custom_help.py`       | Shows how to provide detailed documentation for commands.                                          |
| `error_handling.py`    | Includes error handling within commands for invalid arguments or runtime issues.                   |
| `command_suggestions.py` | Implements basic command suggestion functionality for incomplete or incorrect input.              |
| `sync_async_mix.py`    | Combines synchronous and asynchronous commands in a single CLI application.                        |

---

## API Documentation

### `DynamicCLI` Class

#### Methods

- **`register_command(name, handler, async_handler=False, aliases=None, doc=None)`**
  - Registers a new command.
  - **Parameters**:
    - `name`: Primary command name.
    - `handler`: Function or coroutine to execute the command.
    - `async_handler`: Set to `True` if the handler is asynchronous.
    - `aliases`: A set of alternative names for the command.
    - `doc`: Detailed documentation for the command.

- **`run(args=None)`**
  - Runs the CLI application synchronously.

- **`run_async(args)`**
  - Runs the CLI application asynchronously (useful for embedding).

- **`list_commands()`**
  - Lists all available commands.

- **`complete_command(prefix)`**
  - Suggests commands and aliases based on the provided prefix.

- **`show_help()`**
  - Displays a list of all available commands and aliases.

- **`show_command_help(command_name)`**
  - Displays detailed help for a specific command.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

