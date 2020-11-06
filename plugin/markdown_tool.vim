"---------------------------------------------------------------
" Plugin:      https://github.com/dpretet/vim-markdow-plugin
" Description: A simple plugin to assist writing in markdown
" Maintainer:  Damien Pretet https://github.com/dpretet
"---------------------------------------------------------------

" Require Python3
if !has("python3")
    echo "vim has to be compiled with +python3 to run Vim-SVTB plugin"
    finish
endif

if exists('loaded_markdown_toolbox_vim') || &cp
    finish
endif

let loaded_markdown_toolbox_vim = 1

" Save compatible mode
let s:save_cpo = &cpo
" Reset compatible mode to default value
set cpo&vim

"--------------------------------------------------------
" Load here the python part of the plugin
"--------------------------------------------------------

" Get current plugin directory
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import markdown_tool
EOF

"--------------------------------------------------------
" Bind the python function to call them from command mode
"--------------------------------------------------------

function! AddTask(...)
    let buf = @"
    python3 markdown_tool.add_task()
endfunction

command! -nargs=* MdAddTask call AddTask()


" Restore compatible mode
let &cpo = s:save_cpo
unlet s:save_cpo
