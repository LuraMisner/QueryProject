# Team 4 (Ryan J., Lura M. Maude P.): CS205 Warmup Project

A simple query tool for data on States and Colleges

## Running

This program uses [Python's Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) for a better command line experience. It is available via `pip install prompt_toolkit`. The program will run without it, but the prompt is far less interactive- there are no readline keybindings, history via C-n/p, or autocompletion. 

To run, git clone, cd into the directory, and enter `python main.py` 

This program should run on any system with Python (preferably >=3, as it was not compatibility tested for Python 2, which is EOL) and SQLITE installed. 

## Special Note on Running on Windows 

On Windows, use CMD.EXE or configure your IDE (we tested with PyCharm) to have its output to emulate a terminal. In Pycharm, this in Run/Debug configuration, under Execute, a checkbox that says "emulate terminal on output". If run in Git Bash, or another noncompatible terminal, the program will provide an error message informing you your terminal is noncompliant, and run the standard prompt. 

## Commands

  | Command                                          | Use                                                         |
  |--------------------------------------------------|-------------------------------------------------------------|
  | load data                                        | Load data from file format                                  | 
  | help                                             | Help text/list query grammar                                |  
  | states                                           | List of all states                                          |     
  | State "\<state name\>"                           | All information for a given state                           |     
  | state "\<state name\>" capital                   | State's capital                                             |     
  | state "\<state name\>" population                | State's population                                          | 
  | state "\<state name\>" colleges                  | All colleges in a state                                     |     
  | state "\<state name\>" total colleges            | Number of colleges in a given state                         | 
  | state "\<state name\>" total enrollment          | Total number of college students in a state                 |     
  | college "\<college name\>" enrollment            | Enrollment for a college                                    |     
  | college "\<college name\>" president             | President of a college                                      | 
  | college "\<college name\>" state                 | State of a college                                          |   
  | college "\<college name\>" population percentage | Return enrollment as a percentage of total state population | 


## Examples

\> state "Vermont" capital

\>\> Montpelier

\> college "Champlain College" state

\>\> Vermont

\> state "Vermont" total colleges

\>\> 17
