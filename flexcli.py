import asyncio
import sys
from typing import Callable, Dict, List, Union, Optional, Set

class DynamicCLI:
    """
    Ultra-fast CLI framework with support for:
    - Command aliases
    - Detailed per-command documentation
    - Asynchronous and synchronous command handlers

    Features:
    - Minimal overhead for argument parsing
    - Command aliasing for flexible invocation
    - Clear, extensible design
    """

    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self.async_commands: Dict[str, Callable] = {}
        self.alias_map: Dict[str, str] = {}
        self.docs: Dict[str, str] = {}
        self._all_commands_cached: Optional[List[str]] = None

    def register_command(
        self,
        name: str,
        handler: Callable,
        async_handler: bool = False,
        aliases: Optional[Set[str]] = None,
        doc: Optional[str] = None,
    ):
        """
        Registers a new command.

        Args:
            name (str): Primary command name.
            handler (Callable): The function or coroutine to handle this command.
            async_handler (bool): True if handler is async, False if sync.
            aliases (Optional[Set[str]]): Alternative command names that map to 'name'.
            doc (Optional[str]): A documentation string describing the command.
        """
        if (name in self.commands) or (name in self.async_commands) or (name in self.alias_map):
            raise ValueError(f"Command or alias '{name}' is already registered.")

        if async_handler:
            self.async_commands[name] = handler
        else:
            self.commands[name] = handler

        self.docs[name] = doc or "No description provided."

        if aliases:
            for alias in aliases:
                if (alias in self.commands) or (alias in self.async_commands) or (alias in self.alias_map):
                    raise ValueError(f"Alias '{alias}' conflicts with an existing command or alias.")
                self.alias_map[alias] = name

        # Invalidate command cache whenever we add a command
        self._all_commands_cached = None

    def _resolve_command(self, command_name: str) -> Optional[str]:
        """
        Resolves a command name or alias to a primary command.

        Args:
            command_name (str): The user-entered command name.

        Returns:
            Optional[str]: The resolved primary command name, or None if not found.
        """
        if command_name in self.commands or command_name in self.async_commands:
            return command_name
        return self.alias_map.get(command_name)

    def _execute_sync(self, handler: Callable, args: List[str]):
        """Executes a synchronous command handler."""
        handler(*args)

    async def _execute_async(self, handler: Callable, args: List[str]):
        """Executes an asynchronous command handler."""
        await handler(*args)

    def list_commands(self) -> List[str]:
        """
        Lists all primary command names (excluding aliases).

        Returns:
            List[str]: Sorted list of all primary commands.
        """
        if self._all_commands_cached is None:
            all_primary_commands = list(self.commands.keys()) + list(self.async_commands.keys())
            self._all_commands_cached = sorted(all_primary_commands)
        return self._all_commands_cached

    def get_command_aliases(self, command_name: str) -> List[str]:
        """
        Get a list of aliases for a given command.

        Args:
            command_name (str): The primary command name.

        Returns:
            List[str]: Aliases associated with this command.
        """
        return [alias for alias, target in self.alias_map.items() if target == command_name]

    def complete_command(self, prefix: str) -> List[str]:
        """
        Provides basic command completion suggestions for a given prefix.

        Args:
            prefix (str): The start of a command the user has typed.

        Returns:
            List[str]: Commands and aliases starting with the given prefix.
        """
        all_cmds = self.list_commands()
        suggestions = [cmd for cmd in all_cmds if cmd.startswith(prefix)]
        # Include aliases
        suggestions += [alias for alias in self.alias_map if alias.startswith(prefix)]
        return sorted(suggestions)

    def show_help(self):
        """Displays a list of available commands and their aliases."""
        print("Available commands:")
        for cmd in self.list_commands():
            alias_text = self._format_aliases(cmd)
            ctype = "(async)" if cmd in self.async_commands else "(sync)"
            print(f"  {cmd} {ctype}{alias_text}")
        print("\nUse '<command> --help' for details about a specific command.")

    def show_command_help(self, command_name: str):
        """Displays detailed help for a specific command."""
        doc = self.docs.get(command_name, "No description available.")
        print(f"Help for command '{command_name}':\n{doc}")

    def _format_aliases(self, command_name: str) -> str:
        aliases = self.get_command_aliases(command_name)
        if aliases:
            return f" (aliases: {', '.join(aliases)})"
        return ""

    def run(self, args: Optional[List[str]] = None):
        """
        Runs the CLI application synchronously. Exits the process on error.

        Args:
            args (Optional[List[str]]): Arguments. Defaults to sys.argv[1:].
        """
        if args is None:
            args = sys.argv[1:]
        exit_code = asyncio.run(self.run_async(args))
        sys.exit(exit_code)

    async def run_async(self, args: List[str]) -> int:
        """
        Runs the CLI application in an async context. Does not exit the process.

        Args:
            args (List[str]): Arguments.

        Returns:
            int: Exit code (0 on success, non-zero on error).
        """
        if not args:
            print("No command provided.\n")
            self.show_help()
            return 1

        command_name = args[0]
        if command_name == "--help":
            self.show_help()
            return 0

        resolved_command = self._resolve_command(command_name)
        if not resolved_command:
            print(f"Unknown command or alias: '{command_name}'\n")
            self.show_help()
            return 1

        # Show command-specific help if requested
        if len(args) > 1 and args[1] == "--help":
            self.show_command_help(resolved_command)
            return 0

        command_args = args[1:]
        # Execute the command
        try:
            if resolved_command in self.commands:
                self._execute_sync(self.commands[resolved_command], command_args)
            elif resolved_command in self.async_commands:
                await self._execute_async(self.async_commands[resolved_command], command_args)
            else:
                print(f"Error: command '{resolved_command}' not found.")
                self.show_help()
                return 1
        except Exception as e:
            print(f"Command '{resolved_command}' failed with error: {e}")
            return 1

        return 0
