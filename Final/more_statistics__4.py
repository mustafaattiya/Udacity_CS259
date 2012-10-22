#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# The provided code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the provided code
# to work also on function calls (you can use your code from problem set 5 here)
# Use the mystery function that can be found at line 170 and the
# test cases at line 165 for this exercise.
# Remember that for functions the phi values have to be calculated as
# described in the problem set 5 video -
# you should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
#
# Then combine both approaches to find out the function call and its return
# value that is the most correlated with failure, and then - the line in the
# function. Calculate phi values for the function and the line and put them
# in the variables below.
# Do NOT set these values dynamically.

answer_function = "f2"   # One of f1, f2, f3
answer_bin = -1          # One of 1, 0, -1
answer_function_phi = 0.6547    # precision to 4 decimal places.
answer_line_phi = 1 # precision to 4 decimal places.
# if there are several lines with the same phi value, put them in a list,
# no leading whitespace is required
answer_line = ["elif other < 1:", "grade -= 1"]  # lines of code


# The buggy program
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


# global variable to keep the coverage data in
coverage = {}
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "call"', and in
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    global coverage

    if event == "line":
    # if event == "line" and frame.f_code.co_name == 'f2':
        lineno   = frame.f_lineno
        coverage[lineno] = True

    return traceit

# Calculate phi coefficient from given values
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) /
             math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each covered line
def print_tables(tables):
    for line, stats in tables.iteritems():
        (n11, n10, n01, n00) = stats
        try:
            factor = phi(n11, n10, n01, n00)
            prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
        except:
            prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)

        print prefix, line

# Run the program with each test case and record
# input, outcome and coverage of lines
def run_tests(inputs):
    runs   = []
    global coverage

    for input in inputs:
        coverage = {}
        sys.settrace(traceit)
        result = mystery(input)
        sys.settrace(None)

        runs.append((input, result, coverage))

    return runs

# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for line in coverage:
            if not tables.has_key(line):
                tables[line] = (0, 0, 0, 0)

    return tables

# Compute n11, n10, etc. for each line
def compute_n(tables, runs):
    for line in tables:
        (n11, n10, n01, n00) = tables[line]
        for (input, outcome, coverage) in runs:
            if coverage.has_key(line):
                # Covered in this run
                if outcome == "FAIL":
                    n11 += 1  # covered and fails
                else:
                    n10 += 1  # covered and passes
            else:
                # Not covered in this run
                if outcome == "FAIL":
                    n01 += 1  # uncovered and fails
                else:
                    n00 += 1  # uncovered and passes
        tables[line] = (n11, n10, n01, n00)
    return tables

# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

# These are the test cases for the remove_html_input function
# inputs_line = ['foo',
#           '<b>foo</b>',
#           '"<b>foo</b>"',
#           '"foo"',
#           "'foo'",
#           '<em>foo</em>',
#           '<a href="foo">foo</a>',
#           '""',
#           "<p>"]
# runs = run_tests(inputs_line)

# tables = init_tables(runs)

# tables = compute_n(tables)

# print_tables(tables)

# These are the input values you should test the mystery function with
inputs = ["aaaaa223%", "aaaaaaaatt41@#", "asdfgh123!", "007001007", "143zxc@#$ab", "3214&*#&!(", "qqq1dfjsns", "12345%@afafsaf"]

###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == str
    assert len(magic) > 0

    r1 = f1(magic)

    r2 = f2(magic)

    r3 = f3(magic)

    # print magic, r1, r2, r3

    if r1 < 0 or r3 < 0:
        return "FAIL"
    elif (r1 + r2 + r3) < 0:
        return "FAIL"
    elif r1 == 0 and r2 == 0:
        return "FAIL"
    else:
        return "PASS"


def f1(ml):
    if len(ml) <6:
        return -1
    elif len(ml) > 12 :
        return 1
    else:
        return 0

def f2(ms):
    digits = 0
    letters = 0
    for c in ms:
        if c in "1234567890":
            digits += 1
        elif c.isalpha():
            letters += 1
    other = len(ms) - digits - letters
    grade = 0

    if (other + digits) > 3:
        grade += 1
    elif other < 1:
        grade -= 1

    return grade

def f3(mn):
    forbidden = ["pass", "123", "qwe", "111"]
    grade = 0
    for word in forbidden:
        if mn.find(word) > -1:
            grade -= 1
    if mn.find("%") > -1:
        grade += 1
    return grade




'''
Outline.

    Find the function most correlated with failure.
        Run all functions on all inputs, and build up the runs list.
        Init tables.
        Conpute n for tables.
        Print tables to find the right function.

    Find the line within the function most correlated with failure.
        For the right function f, run all inputs on f, and build runs for lines.
        Build tables for runs.
        Compute n for tables.
        Print tables to find the right line.
'''



coverage_functions = {}

def trace_functions(frame, event, arg):
    if event == 'return':
        coverage_functions[frame.f_code.co_name] = arg

    return trace_functions


def run_test_on_functions(input_sequence):
    global coverage_functions
    runs = []

    for input in input_sequence:
        coverage_functions = {}
        sys.settrace(trace_functions)
        result = mystery(input)
        sys.settrace(None)

        runs.append((input, result, coverage_functions))

    return runs


def init_tables_for_functions(runs):
    tables = {}

    for _, _, coverage in runs:
        for func in coverage:
            tables[func] = tables.get(func, {'pos': (0, 0, 0, 0),
                'zero': (0, 0, 0, 0), 'neg': (0, 0, 0, 0)})

    return tables


def compute_n_for_functions(tables, runs):
    for _, outcome, coverage in runs:
        for func, value in coverage.iteritems():

            if isinstance(value, (int, float)):
                category = 'neg' if value < 0 else 'zero' if value == 0 else 'pos'

            elif hasattr(value, '__len__'):
                length = len(value)
                category = 'neg' if length < 0 else 'zero' if length == 0 else 'pos'

            elif value is False:
                category = 'neg'

            elif value is True:
                category = 'pos'

            elif value is None:
                category = 'neg'

            else:
                raise ValueError(
                    'Invalid value returned from a function: {0}'.format(value))

            for tables_category in tables[func]:
                n11, n10, n01, n00 = tables[func][tables_category]

                if tables_category == category:
                    if outcome == 'FAIL':
                        n11 += 1

                    else:
                        n10 += 1

                else:
                    if outcome == 'FAIL':
                        n01 += 1

                    else:
                        n00 += 1

                tables[func][tables_category] = (n11, n10, n01, n00)

    return tables


def print_tables_for_functions(tables):
    for func in tables:
        for category, ns in tables[func].iteritems():
            n11, n10, n01, n00 = ns

            try:
                factor = phi(n11, n10, n01, n00)
                prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
            except Exception as e:
                prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)

            print prefix, func, category



from pprint import pprint

def run_functions():
    runs = run_test_on_functions(inputs)
    print('Runs:')
    pprint(runs)
    print

    tables = init_tables_for_functions(runs)
    print 'Tables:'
    pprint(tables)
    print

    tables = compute_n_for_functions(tables, runs)
    print 'Tables:'
    pprint(tables)
    print

    print 'Tables:'
    print_tables_for_functions(tables)

def run_lines():
    print 'Lines:'; print

    runs = run_tests(inputs)
    print 'Runs:'
    pprint(runs)

    tables = init_tables(runs)
    print 'Tables:'
    pprint(tables)

    tables = compute_n(tables, runs)
    print 'Tables:'
    pprint(tables)

    print 'Tables:'
    print_tables(tables)


run_functions()
run_lines()
