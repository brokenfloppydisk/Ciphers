from math import floor
from typing import Tuple

class CipherIO():
    fetch_input = input
    print_function = print

    @classmethod
    def print(cls, *args):
        cls.print_function(*args)
    
    @classmethod
    def input(cls, *args):
        cls.fetch_input(*args)

    @classmethod
    def section_header(cls, banner_text: str) -> None:
        """ Print a section header:
        """
        # Calculate the whitespace before the word to center it
        whitespace_length = floor((80 - len(banner_text)) / 2)
        # Print a row of dashes, the word, and a row of dashes
        cls.print(
            "-" * 80 + "\n" + 
            " " * whitespace_length + banner_text + "\n" + 
            "-" * 80
        )
    
    @classmethod
    def get_menu_input(cls, initial_text: str, prompt: str, can_exit: bool=False, *functions: Tuple, **function_dict) -> bool:
        """ Asks the user a question and performs a function depending on the answer.
        
        Returns True if a function was run, otherwise returns False

        *functions should be tuples of (str, function)

        **function_dict should be kwargs of function_name=function
        """
        # Add functions to function dictionary
        for item in functions:
            name, function = item
            function_dict[name] = function

        # Create string for list of options
        options = "\nOptions: \n" + ", ".join([option for option in function_dict]) + "\n"
        
        # Set function output to false by default to return if function fails to run
        function_output = False

        # Only print initial text if it has something in it
        if initial_text != "":
            cls.print(initial_text)

        # Loop if a function has not been executed
        while not function_output:
            # Print the question and get the lowercase form of the answer
            user_input: str = cls.print(prompt + "Type 'help' for more help. " + 
                ("Type 'exit' to exit. " if can_exit else "")).lower()

            # Exit from the loop and return False, as a function was not executed
            if user_input == "exit" and can_exit:
                break
            elif user_input == "help":
                cls.print(options)
                continue
            # Check the keyword arguments to see if the input is assigned to a function
            elif user_input in function_dict:
                # Run the corresponding function
                return function_dict[user_input]()
            
            cls.print("\nInvalid input!\n")
        
        return function_output