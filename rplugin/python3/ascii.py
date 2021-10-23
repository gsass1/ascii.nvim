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

    def get_buffer_max_lines(self):
        return self.nvim.eval("line(\"$\")")

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

    @pynvim.command('Box', nargs='*', range='')
    def box_command(self, args, rg):
        try:
            BoxCommand(self.nvim, NvimHelper(self.nvim)).run(args, rg)
        except Exception as e:
            self.nvim.out_write("Encountered an error: {}\n".format(e))
