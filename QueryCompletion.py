from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import re 

top_level_commands = ['load data','help','quit','states','state','college']
state_commands = ['capital','population','total','colleges']
state_total_commands = ['colleges','enrollment']
college_commands = ['enrollment','president','state','population percentage']

class QueryCompleter(Completer):
    def get_completions(self, document, complete_event):
        """ Generator that yields a completion according to the program's query grammar """ 

        # Figure out if we're currently inside quotation marks 
        text = document.text[::-1]
        in_quote = False
        for ch in text: 
            if ch == '\"':
                in_quote = not in_quote 

        if in_quote: #If we're inside quotes, we want to offer no completion, or a blank completion
            yield Completion("",start_position=0)
        else:  
            # For contextual completions, we need to figure out what has already been written
            # This method is not as foolproof as say, an LL parser (our command language is context free), but it is also substantially less complicated than that for 90% of the return
            word = document.get_word_before_cursor() 
            first_word = document.text.split()[0]

            # State command completions
            if (first_word.lower() == "state"):
                if "total" in document.text.lower(): 
                    for command in state_total_commands: 
                        if command.startswith(word):
                            yield Completion(command,start_position=-len(word))
                else:
                    for command in state_commands: 
                        if command.startswith(word):
                            yield Completion(command,start_position=-len(word))

            # College subcommand completions
            elif (first_word.lower() == "college"): 
                for command in college_commands:
                    if command.startswith(word):
                        yield Completion(command,start_position=-len(word))
            
            # Top level command completions
            else: 
                for command in top_level_commands:
                    if command.startswith(word):
                        yield Completion(command,start_position=-len(word))
