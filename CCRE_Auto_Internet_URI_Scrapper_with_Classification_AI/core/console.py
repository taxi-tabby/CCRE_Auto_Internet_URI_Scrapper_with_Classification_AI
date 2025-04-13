from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.validation import Validator
import inspect
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory  # Import history feature


class MissingParameterError(Exception):
    """Exception raised when required parameters are missing."""
    
    def __init__(self, command_name, missing_params):
        self.command_name = command_name
        self.missing_params = missing_params
        message = f"Command '{command_name}' requires parameters: {', '.join(missing_params)}"
        super().__init__(message)
        
    def display_usage(self):
        """Display usage information for the command."""
        return f"Usage: {self.command_name} " + " ".join([f"--{param} (value)" for param in self.missing_params])


class CommandHandler:

    def __init__(self):
        self.running = True
        self.commands = {}
        self.commands_desc = {}
        self.word_completer = WordCompleter([])
        self.validator = Validator.from_callable(
            self.is_exists_command,
            error_message='It is not a valid command',
            move_cursor_to_end=True
        )
        
        self.history = InMemoryHistory()



    





    def is_exists_command(self, txt):
        """
        Check if the command exists or if the input is empty.
        """
        # Return True if input is empty or just whitespace
        if not txt.strip():
            return True
        # Return True if input starts with any registered command
        if any(txt.lstrip().startswith(cmd) for cmd in self.commands.keys()):
            return True
        return False

    def add_command(self, command: str, func: any, desc: str = ''):
        """
        Add a new command and its corresponding function to the handler.
        """
        self.commands[command] = func
        
        self.commands_desc[command] = desc

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
            parts = user_input.strip().split()
            command_name = parts[0]
            args = parts[1:]

            if command_name in self.commands:
                func = self.commands[command_name]
                options = self._parse_options(args)
                
                # Check required parameters
                sig = inspect.signature(func)
                required_params = [
                    param.name for param in sig.parameters.values() 
                    if param.default == inspect.Parameter.empty 
                    and param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                ]
                
                missing_params = [param for param in required_params if param not in options]
                
                if missing_params:
                    raise MissingParameterError(command_name, missing_params)
                
                # Call the command function with options
                self.commands[command_name](**options)
            else:
                print(f"Unknown command: {command_name}")
        except MissingParameterError as e:
            print(f"Error: {e}")
            print(e.display_usage())
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

    def start_input_loop(self, callback: any):
        """
        Loop to handle user input continuously.
        """
        with patch_stdout():
            callback()
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

    def start(self, callback: any):
        """
        Main function to start the console application.
        """
        # Add default commands
        self.add_command('exit', self._command_exit)
        self.add_command('test', self._command_test)
        self.add_command('help', self._command_help)
        

        # Start input loop
        self.start_input_loop(callback)
        
    def print_formatted(self, text: str = '', style=None, bold=False, italic=False, underline=False):
        """
        Print formatted text using prompt_toolkit's HTML formatting.
        
        Args:
            text (str): The text to print
            style (str, optional): Predefined style: 'success' (green), 'error' (red), 
                                  'warning' (yellow), 'info' (blue)
            bold (bool): Make text bold
            italic (bool): Make text italic
            underline (bool): Underline the text
        
        Examples:
            print_formatted("Hello world")
            print_formatted("This is <b>bold</b> and <i>italic</i>")
            print_formatted("Operation failed", style="error")
            print_formatted("Important message", bold=True)
        """
        
        # Apply style
        if style == 'success':
            text = f"<ansigreen>{text}</ansigreen>"
        elif style == 'error':
            text = f"<ansired>{text}</ansired>"
        elif style == 'warning':
            text = f"<ansiyellow>{text}</ansiyellow>"
        elif style == 'info':
            text = f"<ansiblue>{text}</ansiblue>"
        elif style == 'magenta':
            text = f"<ansimagenta>{text}</ansimagenta>"
        elif style == 'cyan':
            text = f"<ansicyan>{text}</ansicyan>"
        elif style == 'white':
            text = f"<ansiwhite>{text}</ansiwhite>"
        elif style == 'black':
            text = f"<ansiblack>{text}</ansiblack>"
        elif style == 'important':
            text = f"<ansired><b>{text}</b></ansired>"
        elif style == 'highlight':
            text = f"<ansiyellow><b>{text}</b></ansiyellow>"
        elif style == 'special':
            text = f"<ansimagenta><i>{text}</i></ansimagenta>"
        
        # Apply formatting
        if bold:
            text = f"<b>{text}</b>"
        if italic:
            text = f"<i>{text}</i>"
        if underline:
            text = f"<u>{text}</u>"
        
        print_formatted_text(HTML(text))


    def _command_exit(self):
        """Exit this program"""
        self.running = False
        

    def _command_test(self, option_name1: str = 'empty', option_name2: str = 'empty'):
        """
        Example command that takes a command and an option.
        """
        print(f"option_name1: {option_name1} / option_name1: {option_name2}")


    def _command_help(self):
        """Display help information about available commands"""
        self.print_formatted("Available Commands:", style="info", bold=True)
        
        for cmd in sorted(self.commands.keys()):
            func = self.commands[cmd]
            
            if func.__doc__:
                desc = func.__doc__.strip().split('\n')[0]  # Get first line of docstring
            else:
                desc = self.commands_desc.get(cmd, "No description available")
                
            self.print_formatted(f"\t<ansiblue>{cmd}</ansiblue>: {desc}")