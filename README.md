# vim-markdown-tool

<p align="center">
  <img width="256" height="157" src="./icon.png">
</p>

# Overview

A basic attempt to build a markdown plugin to assist writers and coders. No
native mapping, just a set of function everybody can call or map within his
own workflow.

Derived from [platicboy/vim-markdown plugin](https://github.com/plasticboy/vim-markdown)
for syntax hightlighting.

Require Python3 support

Tested only with Neovim (v0.4.4 or newer)

# Task Tracker

TODO:

- [X] add a task
- [X] change a line into a task
- [X] indicate a task status (make them configurable)
- [X] insert code block
- [X] add sub task
- [-] add a table
- [ ] manipulate tables
    - [ ] add a column into a table
    - [ ] add a row into a table
    - [ ] swap row
    - [ ] swap column
- [ ] import/export table from/to CSV & TSV
- [ ] align a table (automatic when go back to normal mode)
- [ ] insert a link (can insert the link if clipboard contains a valid one)
- [ ] insert an image
- [ ] insert html
- [ ] convert list to numbered list and inversely
- [ ] increment/decrement a title. can decrement down to text (overload ctr-x/a?)
- [ ] Create a testsuite with a vim script and diff the expected output across
      a golden file

INBOX:

- support [present](https://github.com/vinayak-mehta/present) or
  [mdp](https://github.com/visit1985/mdp)
- support text extension
- support a personal portfolio to store notes, synced in git
- export to HTML
- support floating window (for what?)
- can check links (image, file, chapters, web links)
- insert a table of content based on titles (can be automatically updated)
- create an agenda
    - indicate a due date to a task
    - task tracking: pomodoro like + reporting/review
- wrap text
- insert video
- Take a look to the best Emacs orgmode plugins

# License

This plugin is under MIT license. Do whatever you want with it, and don't
hesitate to fork it and contribute!
