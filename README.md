# vim-markdown-tool

<p align="center">
  <img width="256" height="157" src="./icon.png">
</p>

# Overview

A basic attempt to build a markdown plugin to assist writers and coders. No
native mapping, just a set of function everybody can call or map within his
own workflow.

This plugin doesn't provide syntax hightlighting for markdown. To enable the
native one from Vim, drop the next line in your vimrc/init.vim:

```vim
" Specify markdown syntax for these extensions and the flavor
" (https://stackoverflow.com/a/30113820)
au BufRead,BufNewFile *.mkd, *.md, *.txt set filetype=markdown.pandoc
```

Many plugins provide syntax highlight for markdow (and more), follow a small list:
- [GitHub Flavored Markdown Syntax](https://github.com/rhysd/vim-gfm-syntax)
- [tpope/vim-markdown](https://github.com/tpope/vim-markdown)
- [plasticboy/vim-markdown](https://github.com/plasticboy/vim-markdown)

Please notice this plugin:
- requires Python3 support
- has been tested only with Neovim v0.4.x, but it should work with Vim

# Task Tracker

AVAILABLE:

- [X] add a task
- [X] change a line into a task
- [X] indicate a task status (make them configurable)
- [X] insert code block
- [X] add sub task
- [X] add a table
- [X] prettify a table
- [X] manipulate tables
    - [X] add a column
    - [X] add a row
    - [X] swap column
    - [X] swap row
- [X] insert a link (can insert the link if clipboard contains a valid one)
- [X] insert an image

TODO:

- [ ] import/export table from/to CSV & TSV
- [ ] Support range when possible
- [ ] convert list to numbered list and inversely
- [ ] insert a table of content, linking titles
- [ ] function to prettify all tables in the document
- [ ] create a testsuite with bash and some vim scripts and diff the expected
      output across a golden file
- [ ] links checker (image, file, chapters, web links)
- [ ] insert video
- [ ] take a look to the best Emacs orgmode plugins

# License

This plugin is under MIT license. Do whatever you want with it, and don't
hesitate to fork it and contribute!
