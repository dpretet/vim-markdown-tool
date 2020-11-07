#!/usr/bin/env python3
# coding: utf-8

"""
Plugin:      https://github.com/dpretet/vim-markdow-tool
Description: A simple plugin to assist writing in markdown
Maintainer:  Damien Pretet https://github.com/dpretet
"""

import vim
import re


def add_task():
    """
    Add a task into current line. If line is empty, replace it
    with the task, else append it below the curor.
    """
    task_desc = vim.eval("task_desc")

    (row, _) = vim.current.window.cursor
    # To index from 0 to N, not from 1, avoid row-1 everywhere in the script
    row = row - 1

    if vim.current.buffer[row] == "":
        del vim.current.buffer[row]

    new_task = """- [ ]"""
    if task_desc:
        new_task += " " + task_desc

    vim.current.buffer.append(new_task, row)


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



