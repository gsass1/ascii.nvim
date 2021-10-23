from .command import Command
import argparse

class BoxCommand(Command):
    def __init__(self, nvim, helper):
        super().__init__(nvim, helper)

    def run(self, args, rg):
        parser = argparse.ArgumentParser()
        parser.add_argument('--padding', type=int, default=0)

        args = parser.parse_args(args)
        padding = args.padding

        start, end = self.helper.get_selection()

        #width = abs(start.col - end.col)

        width = 0
        for row in range(start.row, end.row+1):
            #width = max(width, start.col + len(self.nvim.current.buffer[row].strip()))
            width = max(width, len(self.nvim.current.buffer[row]) - start.col)

        height = abs(start.row - end.row)

        left_offset = start.col + padding
        h_width = width + padding * 2

        # Left and right bars
        for row in range(start.row, end.row+1):
            line = self.nvim.current.buffer[row]
            line = line[:left_offset] + '|' + line[left_offset:]

            required_width = (h_width + left_offset + 1)
            if len(line) < required_width:
                # Fill in the right with spaces
                line = line + ' ' * (required_width - len(line))

            line = line[:required_width] + '|' + line[required_width:]


            self.nvim.current.buffer[row] = line


        # Bottom line
        self.nvim.current.buffer.append(' ' * left_offset + '+' + '-' * h_width + '+', end.row + 1)

        # Top line
        self.nvim.current.buffer.append(' ' * left_offset + '+' + '-' * h_width + '+', start.row)

