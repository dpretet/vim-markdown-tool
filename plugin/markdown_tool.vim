"---------------------------------------------------------------
" Plugin:      https://github.com/dpretet/vim-markdow-tool
" Description: A simple plugin to assist writing in markdown
" Maintainer:  Damien Pretet https://github.com/dpretet
"---------------------------------------------------------------

" Require Python3
if !has("python3")
    echo "vim has to be compiled with +python3 to run markdown-tool plugin"
    finish
endif

" Check plugin has been loaded before
if exists('loaded_markdown_tool') || &cp
    finish
endif

let loaded_markdown_tool= 1

" Save compatible mode
let s:save_cpo = &cpo
" Reset compatible mode to default value
set cpo&vim

"--------------------------------------------------------
" Plugin variable
"--------------------------------------------------------
if !has('g:mardownToolNewStatus')
    let g:mardownToolNewStatus = " "
endif

if !has('g:mardownToolOngoingStatus')
    let g:mardownToolOngoingStatus = "-"
endif

if !has('g:mardownToolDoneStatus')
    let g:mardownToolDoneStatus = "X"
endif

if !has('g:mardownToolCancelStatus')
    let g:mardownToolCancelStatus = "C"
endif

if !has('g:mardownToolDebug')
    let g:mardownToolDebug = 0
endif
"--------------------------------------------------------
" Load here the python part of the plugin
"--------------------------------------------------------

" Get current plugin directory
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" Load python module
python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import markdown_tool
EOF

"---------------------------------------------------------
" Bind the python functions to call them from command mode
"---------------------------------------------------------

" Bind python functions into Vim functions

function! MdAddTask(...)
    let task_desc = ""
    if a:0 > 0
        let task_desc = a:1
    endif
    python3 markdown_tool.add_task()
    unlet task_desc
endfunction

function! MdAddSubTask(...)
    let task_desc = ""
    if a:0 > 0
        let task_desc = a:1
    endif
    python3 markdown_tool.add_sub_task()
    unlet task_desc
endfunction

function! MdChangeToTask()
    python3 markdown_tool.change_to_task()
endfunction


function! MdStatusNew()
    let task_status = g:mardownToolNewStatus
    python3 markdown_tool.change_status()
    unlet task_status
endfunction


function! MdStatusOngoing()
    let task_status = g:mardownToolOngoingStatus
    python3 markdown_tool.change_status()
    unlet task_status
endfunction


function! MdStatusDone()
    let task_status = g:mardownToolDoneStatus
    python3 markdown_tool.change_status()
    unlet task_status
endfunction


function! MdStatusCancel()
    let task_status = g:mardownToolCancelStatus
    python3 markdown_tool.change_status()
    unlet task_status
endfunction

function! MdAddTable(...)
    let description = a:000
    python3 markdown_tool.add_table()
    let description = a:000
endfunction

function! MdAddCode(...)
    let lang = ""
    if a:0 > 0
        let lang = a:1
    endif
    python3 markdown_tool.add_code()
    unlet lang
endfunction

function! MdPrettify()
    python3 markdown_tool.table_transformation()
endfunction

function! MdAddColumn()
    let description = a:000
    python3 markdown_tool.table_transformation('add_column')
    unlet description
endfunction

function! MdAddRow()
    let description = a:000
    python3 markdown_tool.table_transformation('add_row')
endfunction

function! MdSwapColumn()
    python3 markdown_tool.table_transformation('swap_column')
endfunction

function! MdSwapRow()
    python3 markdown_tool.table_transformation('swap_row')
endfunction

function! MdAddLink(...)
    let link = a:000
    let clip = @+
    python3 markdown_tool.add_link()
    unlet link
    unlet clip
endfunction

function! MdAddImage(...)
    let link = a:000
    python3 markdown_tool.add_image()
    unlet link
endfunction

function! MdToHtml()
    " TODO: %!markdown + simple CSS
endfunction

" Register the function as a command callable from command mode

command! -nargs=? MdAddTask call MdAddTask(<q-args>)

command! -nargs=? MdAddSubTask call MdAddSubTask(<q-args>)

command! -nargs=0 MdChangeToTask call MdChangeToTask()

command! -nargs=0 MdStatusNew call MdStatusNew()

command! -nargs=0 MdStatusOngoing call MdStatusOngoing()

command! -nargs=0 MdStatusDone call MdStatusDone()

command! -nargs=0 MdStatusCancel call MdStatusCancel()

command! -nargs=* MdAddTable call MdAddTable(<q-args>)

command! -nargs=? MdAddCode call MdAddCode(<q-args>)

command! -nargs=0 MdPrettify call MdPrettify()

command! -nargs=* MdAddColumn call MdAddColumn()

command! -nargs=* MdAddRow call MdAddRow()

command! -nargs=0 MdSwapColumn call MdSwapColumn()

command! -nargs=0 MdSwapRow call MdSwapRow()

command! -nargs=* MdAddLink call MdAddLink(<q-args>)

command! -nargs=* MdAddImage call MdAddImage(<q-args>)

command! -nargs=0 MdToHtml call MdToHtml()

" Restore compatible mode
let &cpo = s:save_cpo
unlet s:save_cpo
