#!/usr/bin/env python
# Simple debugger
# See instructions around lines 36 and 85

import sys
import readline

# Our buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out
    
# main program that runs the buggy program
def main():
    print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")

# globals
breakpoints = {14: True}
watchpoints = {'c': True}
stepping = False

"""
Our debug function
Improve and expand the debug function to accept 
a watchpoint command 'w <var name>'.
Add the variable name to the watchpoints dictionary
or print 'You must supply a variable name' 
if 'w' is not followed by a string.
"""
def debug(command, my_locals):
    global stepping
    global breakpoints
    
    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):     # step
        stepping = True
        return True
    elif command.startswith('c'):   # continue
        stepping = False
        return True
    elif command.startswith('p'):    # print 
        # FIRST ASSIGNMENT CODE
        pass
    elif command.startswith('b'):    # breakpoint         
        # SECOND ASSIGNMENT CODE
        pass
    elif command.startswith('w'):    # watch variable
        if arg is None:
            print('You must supply a variable name')
        else:
            watchpoints[arg] = True
        
    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)
        
    return False

commands = ["w out", "c", "c", "c", "c", "c", "c", "q"]

def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

"""
Our traceit function
Improve the traceit function to watch for variables 
in the watchpoint dictionary and print out 
event, frame.f_lineno, frame.f_code.co_name
and then the values of the variables, each in new line,
in a format:
somevar ":", repr("Initialized"), "=>", repr(somevalue)
or
somevar ":", repr(old-value), "=>", repr(new-value)
but only when the value of a variable has changed.
If the value if unchanged, do nothing.
"""
def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            while not resume:
                print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

# Using the tracer
#sys.settrace(traceit)
#main()
#sys.settrace(None)

#Simple test 
print watchpoints
debug("w s", {'s': 'xyz', 'tag': False})
print watchpoints
#>>> {'c': True}
#>>> {'c': True, 's': True}