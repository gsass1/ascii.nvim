import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(SCRIPT_DIR + '/cmds'))

import pynvim
from cmds import BoxCommand

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "(row: {}, col: {})".format(self.row, self.col)

class NvimHelper:
    def __init__(self, nvim):
        self.nvim = nvim

    def get_setting(self, name):
        return self.nvim.eval("get(g:, '{}')".format(name))

    def get_visual_mode(self):
        return str(self.nvim.eval("visualmode()"))

    def get_selection(self) :
        if self.get_visual_mode() == 'V':
            # Visual Line mode
            start_pos, end_pos = self.get_selection_begin(), self.get_selection_end()
            start_pos.col = 0
            end_pos.col = len(self.nvim.current.buffer[end_pos.row - 1])
            return start_pos, end_pos
        else:
            return self.get_selection_begin(), self.get_selection_end()

    def get_selection_begin(self):
        arr = self.nvim.eval("getpos(\"'<\")")[1:3]
        return Position(arr[0] - 1, arr[1] - 1)

    def get_selection_end(self):
        arr = self.nvim.eval("getpos(\"'>\")")[1:3]
        return Position(arr[0] - 1, arr[1] - 1)

    def fill(self, row, l_offset, fill_chars, text):
        line = self.nvim.current.buffer[row]
        if len(line) < l_offset + len(text):
            line = line + fill_chars * (l_offset + len(text) - len(line))
        line = line[:l_offset] + text + line[(l_offset + len(text)):]
        self.nvim.current.buffer[row] = line

@pynvim.plugin
class AsciiPlugin(object):
    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim
    
    # @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    # def on_bufenter(self, filename):
    #     self.nvim.out_write('testplugin is in ' + filename + '\n')

    @pynvim.command('Box', nargs='*', range='')
    def box_command(self, args, rg):
        BoxCommand(self.nvim, NvimHelper(self.nvim)).run(args, rg)

        #padding = 1
        #for arg in args:
        #    if arg.startswith("padding="):
        #        padding = int(arg[8:])

        #top = rg[0]
        #bottom = rg[1]

        #max_length = 0
        #min_indent = 99999
        #for idx in range(top, bottom+1):
        #    line = self.nvim.current.buffer.range(idx, idx)[0]
        #    max_length = max(max_length, len(line.strip()))

        #    line_indent = len(line) - len(line.strip())
        #    if line_indent != 0:
        #        min_indent = min(min_indent, line_indent)

        ##for idx in range(padding):
        #    #self.nvim.current.buffer.append("", bottom+idx+1)

        ## for idx in range(padding):
        ##     self.nvim.current.buffer.append("", top-idx-1)

        #for idx in range(top - (padding-1) , bottom+padding):
        #    line = self.nvim.current.buffer.range(idx, idx)[0]
        #    own_indent = len(line) - len(line.strip()) - min_indent
        #    line = " " * (min_indent - 1) + "|" + (own_indent)*" " + (padding-1)*" " + line.strip() + " " * (max_length - len(line.strip())) + (padding-1)*" " + "|"
        #    self.nvim.current.buffer.range(idx, idx)[0] = line


        #self.nvim.current.buffer.append(" "*(min_indent-1) + "+" + "-"*(max_length+(padding-1)*2) + "+", top-padding)
        #self.nvim.current.buffer.append(" "*(min_indent-1) + "+" + "-"*(max_length+(padding-1)*2) + "+", bottom+padding)

        #self.nvim.out_write(str(rg))

        # self.nvim.current.line = ('Command with args: {}, range: {}'
        #                           .format(args, range))
