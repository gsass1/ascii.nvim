from .command import Command
import argparse

class BoxCommand(Command):
    def __init__(self, nvim, helper):
        super().__init__(nvim, helper)

    def run(self, args, rg):
        parser = argparse.ArgumentParser()
        parser.add_argument('--padding', type=int, default=1)

        args = parser.parse_args(args)

        self.insert_box(None, None, args.padding)

    def insert_box(self, begin, end, padding):
        #width = abs(begin.col - end.col)
        #height = abs(begin.row - end.row)

        #self.nvim.current.buffer.append(str(begin.col))
        #self.nvim.current.buffer.append(str(end.col))
        start, end = self.helper.get_selection()
        self.nvim.current.buffer.append(str(start))
        self.nvim.current.buffer.append(str(end))
