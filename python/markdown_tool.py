#!/usr/bin/env python3
# coding: utf-8

"""
Plugin:      https://github.com/dpretet/vim-markdow-tool
Description: A simple plugin to assist writing in markdown
Maintainer:  Damien Pretet https://github.com/dpretet
"""

import vim
import re

DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3


def logger(msg, logtype=INFO):
    """
    Print function to debug the flow
    TODO: Handle colors in vim messages
    """
    debug = int(vim.eval("g:mardownToolDebug"))

    if debug:
        if logtype == DEBUG:
            log = """echo "DEBUG: """
        if logtype == INFO:
            log = """echo "INFO: """
        if logtype == WARNING:
            log = """ echo "WARNING: """
        if logtype == ERROR:
            log = """echoerr "ERROR: """

        log += "MarkdownTool: "
        log += msg + """\""""
        vim.command(log)

    return


def add_task(is_sub_task=False):
    """
    Add a task into current line. If line is empty, replace it
    with the task, else append it below the curor.
    """

    # Grab task description from vim script front end
    task_desc = vim.eval("task_desc")

    (row, _) = vim.current.window.cursor
    # To index from 0 to N-1, not from 1, avoid row-1 everywhere in the script
    row = row - 1

    is_empty = False
    if vim.current.buffer[row] == "":
        logger("Line is empty", DEBUG)
        is_empty = True
        del vim.current.buffer[row]

    new_task = """- [ ]"""
    if task_desc:
        new_task += " " + task_desc

    # Append to the next line if line is not empty (so can be replaced)
    # or if is a subtask
    if not is_empty or is_sub_task:
        vim.current.buffer.append(new_task, row+1)
    else:
        vim.current.buffer.append(new_task, row)

    # Move cursor on the task line and go to the end
    if is_empty:
        vim.current.window.cursor = (row+1, 0)
    else:
        vim.current.window.cursor = (row+2, 0)
    vim.command("normal! $")
    return


def add_sub_task():
    """
    Append a subtask below an existing task
    """

    # Grab line
    (row, _) = vim.current.window.cursor
    line = vim.current.buffer[row-1]
    # Check first the line is a task
    # TODO: Change for a regex
    if """[""" not in line or """]""" not in line:
        logger("No brackets found. Assume it's not a task", WARNING)
        return

    # Get line start to compute later the indentation to apply
    first = line.find("-")
    # Add it as a sub task
    add_task(is_sub_task=True)

    # Compute indent to apply
    shiftwidth = int(vim.eval("&shiftwidth"))
    indent_level = int(first / shiftwidth + 1)
    # And indent n times
    i = 0
    while i < indent_level:
        vim.command("normal! >>")
        i = i + 1
    vim.command("normal! $")
    return


def change_to_task():
    """
    Change a line to a task. The line must not start with - [ ],
    it can only be a list item or a simple line.
    """

    (row, _) = vim.current.window.cursor
    # To index from 0 to N-1, not from 1, avoid row-1 everywhere in the script
    row = row - 1
    line = vim.current.buffer[row]

    # Check first the line is not already a task
    # TODO: Change for a regex
    if """[""" in line and """]""" in line:
        logger("Found brackets. Assume it's a task", DEBUG)
        return

    # If line is empty, turn it into a task by replacing it simply
    if vim.current.buffer[row] == "":
        del vim.current.buffer[row]
        vim.current.buffer.append("- [ ]", row)
        return

    # Search the first non null character
    first = len(re.match(r"\s*", line, re.UNICODE).group(0))

    # If is an item, just place the brackets
    if line[first] == "-":
        text = len(re.match(r"\s*", line[first+1], re.UNICODE).group(0))
        new_task = " " * first + """- [ ]""" + line[text:]
    # Else insert hypen and brackets
    else:
        new_task = " " * first + """- [ ] """ + line[first:]

    del vim.current.buffer[row]
    vim.current.buffer.append(new_task, row)

    # Move cursor on the task line and go to the end
    vim.current.window.cursor = (row+1, 0)
    vim.command("normal! $")
    return


def change_status():
    """
    When into a task line, seach for brackets and change symbol
    inbetween signifyiing the task status
    """

    # Grab task status from vim script front-end
    task_status = vim.eval("task_status")
    (row, _) = vim.current.window.cursor
    # To index from 0 to N, not from 1, avoid row-1 everywhere in the script
    row = row - 1
    line = vim.current.buffer[row]

    # Check first the line is a task, else return
    # TODO: Change for a regex
    if """[""" not in line or """]""" not in line:
        logger("No brackets found. Assume it's not a task", WARNING)
        return

    first = line.find("[")
    second = line.find("]")
    new_task = line[0:first+1] + task_status + line[second:]
    del vim.current.buffer[row]
    vim.current.buffer.append(new_task, row)

    # Move cursor into the bracket
    vim.current.window.cursor = (row+1, first+1)
    return


def add_code():
    """
    Add a code block
    """

    # Grab language from vim script front-end
    lang = vim.eval("lang")

    (row, _) = vim.current.window.cursor
    # To index from 0 to N, not from 1, avoid row-1 everywhere in the script
    row = row - 1

    if vim.current.buffer[row] == "":
        del vim.current.buffer[row]

    start_block = """```"""
    if lang:
        start_block += lang
    end_block = "```"

    # Append code block into the buffer
    vim.current.buffer.append(end_block, row)
    vim.current.buffer.append("", row)
    vim.current.buffer.append(start_block, row)

    # Move cursor inside the code block
    vim.current.window.cursor = (row+2, 0)
    return


def add_table():
    """
    Insert a markdown table at the current line.

    Table dimensions can be specified in different ways:

        - can be a list of two integers like [2 3], creating a table
          with 2 columns and 3 rows.

        - can be a list of string like [Name, Address, Phone], creating
          a table with 3 columns named with the strings and 5 rows
          (default value when row number is not specified)

    By default tables are left justified
    """

    (row, _) = vim.current.window.cursor
    # To index from 0 to N-1, not from 1, avoid row-1 everywhere in the script
    row = row - 1
    # Grab table dimension from vim script front end
    desc = vim.eval("description")
    # Put in shape the descriptions
    desc = table_clean_args(desc)
    # Construct a first table, with only strings in to a list
    table_list = table_init(desc)
    # Format the table to drop
    table_text = table_prettifier(table_list)
    # Append the new shiny table in the buffer, at current line if empty
    # else on the line below
    vim.current.buffer.append(table_text, row+1)

    return


def table_clean_args(desc):
    """
    Handle the arguments passed to AddTable() and prepare
    them for processing
    """

    # Handle as well comma and space to separate descriptions
    if "," in desc[0]:
        desc = desc[0].split(",")
    else:
        desc = desc[0].split(" ")

    logger("Nb Args: " + str(len(desc)), DEBUG)

    # Clean up the arguments
    for i in range(len(desc)):
        desc[i] = desc[i].strip()

    return desc


def table_init(dims):
    """
    From description passed by the user, draft a first table
    based on list of string. Headers remain blank if was not specified,
    and add separation with rows
    """

    # Default dimension of the table, will be adjusted by the user arguments
    column_num = 3
    row_num = 5
    row_width = 5
    # The output list to return
    table_list = []
    # A flag indicating we need to create a table only from dimension,
    # no header description has been passed
    init_with_dim = 0

    # Check first if the arguments could be the table dimensions
    # In this case, handle a dimension passed by the user, like 2 x 3
    # He didn't provide the columns' header
    if len(dims) == 2 and\
       dims[0].isnumeric() and dims[1].isnumeric():

        init_with_dim = 1
        dim = dims[0] + "x" + dims[1]
        msg = "Two numeric args passed. Will create a " + dim + " table"
        logger(msg, DEBUG)

        column_num = int(dims[0])
        row_num = int(dims[1])
    # Here assume the arguments are the headers description if arguments passed
    elif len(dims) > 0:
        column_num = len(dims)
    # Else if nothing passed, assume it's init with default dimensions
    else:
        logger("Init the table with default dimension (3x5)", DEBUG)
        init_with_dim = 1

    # Init the table content
    for i in range(column_num):
        rows = []
        # +1 for the headers
        for j in range(row_num+1):
            # Append the header description
            if j == 0 and not init_with_dim:
                rows.append(dims[i])
            # Or simply a blank one
            else:
                rows.append(" " * row_width)

        table_list.append(rows)

    return table_list


def table_prettifier(table, justify="left"):
    """
    Prettify the table to drop into the document. Adapt the
    column width
    """

    default_width = 5
    column_num = len(table)
    table_text = []

    column_width = []

    # First parse the table to store the maximum width of
    # each column stored
    for i in range(column_num):
        column_width.append(0)
        for j in range(len(table[0])):
            if len(table[i][j]) > column_width[i] and\
                    not table[i][j].isspace():
                column_width[i] = len(table[i][j])
        # If table is only plenty of space, init width
        if column_width[i] == 0:
            column_width[i] = default_width

    # Then append the data and align them to have clean
    # aligment to ease visualization
    for i in range(len(table[0])):
        row_md = "| "
        for j in range(column_num):
            # Case it's only whitespace, adapt with correct width
            if table[j][i].isspace():
                row_md += " " * column_width[j] + " | "
            # Else append the content and add missing whitespace
            # for alignment
            else:
                missing_ws = column_width[j] - len(table[j][i])
                row_md += table[j][i] + (" " * (missing_ws-1)) + " | "
        # Add our brand new row
        table_text.append(row_md)
        # If was parsing the columns' header, add a new line
        # (|----|----|) to separate the data
        if i == 0:
            row_md = "|"
            for j in range(column_num):
                # +2 because we add space before and after '|'
                # in headers and data
                row_md += "-" * (column_width[j] + 2) + "|"
            table_text.append(row_md)

    return table_text
