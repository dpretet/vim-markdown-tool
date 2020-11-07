#!/usr/bin/env python3
# coding: utf-8

"""
Plugin:      https://github.com/dpretet/vim-markdow-tool
Description: A simple plugin to assist writing in markdown
Maintainer:  Damien Pretet https://github.com/dpretet
"""

import vim
import re


def add_task(is_sub_task=False):
    """
    Add a task into current line. If line is empty, replace it
    with the task, else append it below the curor.
    """
    task_desc = vim.eval("task_desc")

    (row, _) = vim.current.window.cursor
    # To index from 0 to N, not from 1, avoid row-1 everywhere in the script
    row = row - 1

    is_empty = False
    if vim.current.buffer[row] == "":
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
    vim.command("normal $")
    return


def add_sub_task():
    """
    Append a subtask below an existing task
    """

    # Grab line
    (row, _) = vim.current.window.cursor
    line = vim.current.buffer[row-1]
    # Check first the line is a task
    if """[ ]""" not in line and """[]""" not in line:
        print("Line is not a task")
        return

    # Get line start to compute later the indentation to apply
    first = line.find("-")
    # First add it as a task
    add_task(is_sub_task=True)

    # Compute indent to apply
    shiftwidth = int(vim.eval("&shiftwidth"))
    indent_level = int(first / shiftwidth + 1)
    # And indent n times
    i = 0
    while i < indent_level:
        vim.command("normal >>")
        i = i + 1
    vim.command("normal $")
    return


def change_to_task():
    """
    Change a line to a task. The line must not start with - [ ],
    it can only be a list item or a simple line.
    """

    (row, _) = vim.current.window.cursor
    # To index from 0 to N, not from 1, avoid row-1 everywhere in the script
    row = row - 1
    line = vim.current.buffer[row]

    # Check first the line is not already a task
    if """[ ]""" in line or """[]""" in line:
        print("Found brackets into the line")
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
    vim.command("normal $")
    return


def change_status():
    """
    When into a task line, seach for brackets and change symbol
    inbetween signifyiing the task status
    """

    task_status = vim.eval("task_status")
    (row, _) = vim.current.window.cursor
    # To index from 0 to N, not from 1, avoid row-1 everywhere in the script
    row = row - 1
    line = vim.current.buffer[row]

    # Check first the line is a task
    if """[ ]""" not in line and """[]""" not in line:
        print("Line is not a task")
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

    vim.current.buffer.append(end_block, row)
    vim.current.buffer.append("", row)
    vim.current.buffer.append(start_block, row)

    # Move cursor into the code block
    vim.current.window.cursor = (row+2, 0)
    return


def add_table():
    """
    Insert a markdown table after the current line
    Table dimension can be specified. By default tables are
    left justified
    """

    dims = vim.eval("argus")
    dims = dims[0].split(" ")

    for el in dims:
        print(el)
        print(type(el))
