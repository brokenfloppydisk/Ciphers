from time import sleep
from cipher_io import CipherIO
from ciphers.aristocrat_io import AristocratIO

def main_menu() -> None:
    """ Run the main menu
    """
    CipherIO.print_function = print
    CipherIO.fetch_input = input

    exit_status = True
    returning = False

    while exit_status != False: 
        # Print banner if launching the program, otherwise print returning to main menu
        if not returning: 
            CipherIO.section_header("Cipher toolkit")
        else:
            CipherIO.section_header("Returning to the main menu...")
            sleep(0.5)
        
        # Get user input and either go to cipher generation or solving.
        exit_status = CipherIO.get_menu_input(
            "Welcome to cipher toolkit! This program allows you to "
            + "generate monoalphabetic ciphers, \npractice solving a cipher, "
            + "attempt to solve a cipher, and decrypt a cipher with the key.\n"
            + "made to practice codebusters for Science Olympiad.", 
            "Please enter a command. ", 
            False,
            ("generate cipher" , AristocratIO.generate_user_cipher),
            ("practice cipher" , AristocratIO.practice_cipher),
            ("solve unknown cipher", AristocratIO.solve_unknown_cipher),
            ("decrypt known cipher", AristocratIO.decrypt_known_cipher),
            ("exit", lambda : CipherIO.section_header("Exiting program...")))
        
        returning = True

if __name__ == "__main__":
    main_menu()