from Database import query_type

def help():
    '''
    Prints out the commands and their uses for our valid query language
    Takes no parameters
    Returns nothing
    '''
    print("""  
  |----------------------------------------------|-------------------------------------------------------|
  | Command                                      | Use                                                   |
  |----------------------------------------------|-------------------------------------------------------|
  | load data                                    | Load data from file format                            | 
  | help                                         | Help text/list query grammar                          | 
  | quit                                         | Terminate the program                                 |   
  | states                                       | List of all states                                    |     
  | state "state name"                           | All information for a given state                     |     
  | state "state name" capital                   | State's capital                                       |     
  | state "state name" population                | State's population                                    | 
  | state "state name" colleges                  | All colleges in a state                               |     
  | state "state name" total colleges            | Number of colleges in a given state                   | 
  | state "state name" total enrollment          | Total number of college students in a state           |     
  | college "college name" enrollment            | Enrollment for a college                              |     
  | college "college name" president             | President of a college                                | 
  | college "college name" state                 | State of a college                                    |
  | college "college name" population percentage | Display enrollment as percentage of state population  |
  |----------------------------------------------|-------------------------------------------------------|
  """)


def parser(user_input: str) -> (query_type, [str, str]):
    look_extra_space = user_input.strip(' ')
    '''
    Breaks up user input into a question format
    Takes a string of user input
    Returns a tuple of query type and dictionary
    '''
    # Help
    if look_extra_space.lower() == "help":
        if user_input.lower() == "help":
            help()
            return (query_type.HELP,{})
        else:
            print("You might have had extra white space when calling command help")
            print("Please try again and be careful for the extra white space")
            return None
    # Load data
    if look_extra_space.lower() == "load data":
        if user_input.lower() == "load data":
            return (query_type.LOAD_DATA, {})
        else:
            print("You might have had extra white space when calling command load data")
            print("Please try again and be careful for the extra white space")
            return None

    # Quit
    if look_extra_space.lower() == "quit":
        if user_input.lower() == "quit":
            return (query_type.QUIT, {})
        else:
            print("You might have had extra white space when calling command quit")
            print("Please try again and be careful for the extra white space")
            return None

    # Breaks user input into pieces
    words = user_input.split()
    length_words = len(words)

    # Case One: One word
    if length_words == 1:
        if user_input.lower() == "states":
            # List states
            dict = {}
            dict['property'] = "*"
            return (query_type.STATES, dict)
        elif user_input.lower() == "colleges":
            # List colleges
            dict = {}
            dict['property'] = "*"
            return (query_type.COLLEGE, dict)
        else:
            # Invalid search
            return None

    table = ""  # Refers to which table the question refers to
    location = ""  # Refers to the state or college they are asking about
    information = ""  # Refers to the information searched for

    quote = False
    info = False

    # Organizes the words into their category
    for word in words:
        if word == words[0]:
            table = word

        if info:
            information += word + " "

        # Location is the item between the quotes
        elif word.count('"') != 0:
            if not quote:
                #one word
                if word.count('"') == 2:
                    location = word
                    info = True
                else:
                    quote = True
            else:
                quote = False
                location += word
                info = True

        if quote:
            location += word + " "

    # Remove the space at the end of information
    information = information[0:len(information)-1]

    # Verify that there are quotation marks
    if user_input.count('"') < 2:
        print("please put quotation mark where indicated in the command")
        return None

    location = location.strip('"')

    # Case Two: Two items
    if len(information) == 0:
        dict = {}
        dict['property'] = "*"

        if table.lower() == "state":
            dict['state_name'] = location
            return (query_type.STATE, dict)
        elif table.lower() == "college":
            dict['college_name'] = location
            return (query_type.COLLEGE, dict)

    # Case Three: all three items
    # Verify that table is state or college
    if table.lower() != "state" and table.lower() != "college":
        return None

    # Verify that information is for data we have
    if table.lower() == "state":
        dict = {}
        dict['state_name'] = location
        dict['property'] = information
        if information.lower() == "capital" or information.lower() == "population":
            return query_type.STATE, dict

        elif information.lower() == "colleges":
            return query_type.STATE_COLLEGES, dict

        elif information.lower() == "total colleges":
            return query_type.STATES_TOTAL_COLLEGES, dict

        elif information.lower() == "total enrollment":
            return query_type.STATES_TOTAL_ENROLLMENT, dict

    elif table.lower() == "college":
        dict = {}
        dict['college_name'] = location
        if information.lower() == "enrollment" or information.lower() == "president" or information.lower() == "state":
            dict['property'] = information
            return query_type.COLLEGE, dict
        elif information.lower() == "population percentage":
            dict['property'] = information
            return query_type.COLLEGE_POPULATION_PERCENTAGE, dict
    # Not a valid case if it gets to here
    return None