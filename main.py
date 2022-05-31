import parser_
import Database
from Database import query_type 
from prompt_toolkit import PromptSession
import QueryCompletion
import os, sys

def prompt_user():
    """ Prompt the user for input with standard, send to parser, return if valid, loop on bad input """ 
    user_input = input("> ")
    return_type = parser_.parser(user_input)
    while return_type == None:
        print("Your command was invalid. Type `help` for a list of commands")
        user_input = input("> ")
        return_type = parser_.parser(user_input)
    return return_type

def send_to_database(args_parser,conn):
    """ Make database query and output results """ 
    output = Database.do_query(args_parser[0], args_parser[1], conn)
    if len(output) == 0:
        print("Sorry we either do not have it in the data base")
        print("or the name was inserted wrong")
    else:
        print_data(output)

def print_data(output):
    """ Print formatted query output """
    index = len(output)
    for i in range(index):
        new_output = ''
        bad_character = [')', '(', "'", ',', '"', '/']
        fix_output = str(output[i])
        for char in fix_output:
            if char not in bad_character:
                new_output = new_output + char
        print(new_output)

def get_path_State():
    path_state = os.path.abspath('State.csv')
    return path_state

def get_path_College():
    path_college = os.path.abspath('College.csv')
    return path_college

def run_program_standard():
    """ Program REPL with standard, no-dependency prompt """ 
    conn = Database.standup_database("college_state.db") # Open or create database
    args_parser = prompt_user() #Prompt the user for command 

    while (args_parser[0] != query_type.QUIT): 
        print(args_parser[0])
        if (not args_parser[0] == query_type.QUIT and not args_parser[0] == query_type.HELP): 
            if (args_parser[0] == query_type.LOAD_DATA): 
                Database.empty_database(conn) # We always want to overwrite existing data, per the spec 
                Database.load_data(get_path_State(),"State", conn)
                Database.load_data(get_path_College(),"College", conn)
            elif (Database.table_empty("College",conn) or Database.table_empty("State",conn)): 
                print("you have not loaded the data yet")
                print("load the data with the `load data` command")
            else:
                send_to_database(args_parser,conn)
        args_parser = prompt_user()

def prompt_user_fancy(session):
    """ Prompt user using Prompt Toolkit, send input to parser, return if valid, and loop on bad input """ 
    user_input = session.prompt("> ",completer=QueryCompletion.QueryCompleter())
    return_type = parser_.parser(user_input)
    while return_type == None:
        print("Your command was invalid. Type `help` for a list of commands")
        user_input = session.prompt("> ",completer=QueryCompletion.QueryCompleter()) 
        return_type = parser_.parser(user_input)
    return return_type

def run_program_with_fancy_prompt():
    """ Program REPL with Prompt Toolkit fancy prompt and completion""" 
    conn = Database.standup_database("college_state.db") # Open or create database
    session = PromptSession()

    parser_results = prompt_user_fancy(session)
    while parser_results[0] != query_type.QUIT: 
        if (not parser_results[0] == query_type.HELP): 
            if (parser_results[0] == query_type.LOAD_DATA): 
                Database.empty_database(conn) # We always want to overwrite existing data, per the spec 
                Database.load_data(get_path_State(),"State", conn)
                Database.load_data(get_path_College(),"College", conn)
            elif (Database.table_empty("College",conn) or Database.table_empty("State",conn)): 
                print("you have not loaded the data yet")
                print("load the data with the `load data` command")
            else:
                send_to_database(parser_results,conn)

        parser_results = prompt_user_fancy(session)


def main(argv):
    if ("--without-readline" in argv):
        use_prompt_toolkit = False 
    else: 
        use_prompt_toolkit = True

    try: 
        from prompt_toolkit import prompt
    except ModuleNotFoundError: 
        if use_prompt_toolkit: 
            print("Your system does not have Prompt Toolkit installed")
            print("This program uses Python\'s Prompt Toolkit, available via `pip install prompt_toolkit` for the best experience, and readline emulation. Without it, the prompt will be less interactive.")
            print("To not have this message display, start this program with --without-readline")
        use_prompt_toolkit = False 
    except: 
        print("This program uses Python\'s Prompt Toolkit, available via `pip install prompt_toolkit` for the best experience, and readline emulation.")
        print("Your current terminal is NOT COMPATIBLE with Prompt Toolkit. On Windows, try using PyCharm with Terminal Emulation On Output in your Run/Debug configuration enabled, or use CMD.EXE. Prompt Toolkit does not work with Git Bash")
        print("The program will now run a less responsive prompt, without Prompt Toolkit")
        use_prompt_toolkit = False 

    if use_prompt_toolkit: 
        run_program_with_fancy_prompt()
    else: 
        run_program_standard()


main(sys.argv)
