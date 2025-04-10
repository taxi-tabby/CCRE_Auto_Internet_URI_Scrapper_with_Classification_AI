from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.validation import Validator
from prompt_toolkit.history import InMemoryHistory  # Import history feature


class CommandHandler:

    def __init__(self):
        self.running = True
        self.commands = {}
        self.word_completer = WordCompleter([])
        self.validator = Validator.from_callable(
            self.is_exists_command,
            error_message='It is not a valid command',
            move_cursor_to_end=True
        )
        
        self.history = InMemoryHistory()

    def _command_exit(self):
        """Exit this program"""
        self.running = False
        

    def _command_test(self, option_name1: str = 'empty', option_name2: str = 'empty'):
        """
        Example command that takes a command and an option.
        """
        print(f"option_name1: {option_name1} / option_name1: {option_name2}")

    def is_exists_command(self, txt):
        """
        Check if the command exists.
        """
        if any(txt.lstrip().startswith(cmd) for cmd in self.commands.keys()):
            return True
        return False

    def add_command(self, command: str, func: any):
        """
        Add a new command and its corresponding function to the handler.
        """
        self.commands[command] = func

        # Update the word completer with the updated list of commands
        self.word_completer = WordCompleter(list(self.commands.keys()), ignore_case=True, match_middle=True)

    def handle_input(self, user_input):
        """
        Process the user input and call the correct command function.
        """
        # Empty command input doesn't do anything
        if user_input.strip() == '':
            return True

        # Parse the command and execute
        self.execute_command(user_input)

        return True

    def execute_command(self, user_input):
        """
        Parse the command and options, and execute the corresponding function.
        """
        try:
            # Split user input into command and arguments (space-separated)
            parts = user_input.strip().split()
            command_name = parts[0]  # The first part is the command
            args = parts[1:]  # Remaining parts are arguments/options

            if command_name in self.commands:
                # Manually handle options if there are any
                if command_name == "test" and len(args) >= 1:
                    # Parse options in the form of '--option_name value'
                    options = self._parse_options(args)  # Parse options after the command
                    self.commands[command_name](**options)  # Call the command function with options
                else:
                    # If no options, just call the function directly
                    self.commands[command_name](*args)
            else:
                print(f"Unknown command: {command_name}")
        except Exception as e:
            print(f"Error executing command: {e}")

    def _parse_options(self, args):
        """
        Parse options in the form of '--option_name value'
        """
        options = {}
        i = 0
        while i < len(args):
            if args[i].startswith('--'):
                # Option name is the part after '--'
                option_name = args[i][2:]  # Get option name (remove '--')
                # Check if the next argument is the option value
                if i + 1 < len(args):
                    options[option_name] = args[i + 1]  # Store the option and its value
                    i += 1
                else:
                    print(f"Option {option_name} expects a value")
            i += 1
        return options

    def start_input_loop(self):
        """
        Loop to handle user input continuously.
        """
        with patch_stdout():
            while self.running:
                # Use history in the prompt
                user_input = prompt('> ', 
                                    auto_suggest=AutoSuggestFromHistory(),
                                    complete_while_typing=False, 
                                    completer=self.word_completer, 
                                    validator=self.validator,
                                    history=self.history)  
                
                # Add the user input to history manually
                if user_input.strip():
                    self.history.append_string(user_input.strip()) 

                if not self.handle_input(user_input):
                    break

    def start(self):
        """
        Main function to start the console application.
        """
        # Add default commands
        self.add_command('exit', self._command_exit)
        self.add_command('test', self._command_test)

        # Start input loop
        self.start_input_loop()

