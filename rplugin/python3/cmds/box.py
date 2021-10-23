from .command import Command
import argparse

class BoxCommand(Command):
    def __init__(self, nvim, helper):
        super().__init__(nvim, helper)

    def run(self, args, rg):
        parser = argparse.ArgumentParser()
        parser.add_argument('--padding', type=int, default=self.helper.get_setting("ascii_default_padding"))

        args = parser.parse_args(args)
        padding = args.padding

        start, end = self.helper.get_selection()

        width = abs(start.col - end.col) + 1

#        width = 0
#        for row in range(start.row, end.row+1):
#            #width = max(width, start.col + len(self.nvim.current.buffer[row].strip()))
#            width = max(width, len(self.nvim.current.buffer[row]) - start.col)

        height = abs(start.row - end.row)

        left_offset = start.col + padding
        w = start.col
        h_width = width + padding * 2

        # If padding > 0, insert blank lines on top and bottom
        # Bottom
        # for p in range(padding):
        #     self.nvim.current.buffer.append('', end.row + 1)

        # # Top
        # for p in range(padding):
        #     self.nvim.current.buffer.append('', start.row)

        # Adjust position
        start.row -= padding
        end.row += padding

        hline_char = self.helper.get_setting("ascii_hline_char")[0]
        vline_char = self.helper.get_setting("ascii_vline_char")[0]
        corner_char = self.helper.get_setting("ascii_corner_char")[0]

        # Left and right bars
        for row in range(start.row, end.row+1):
            line = self.nvim.current.buffer[row]

            required_left_width = (w + padding + 1)
            if len(line) < required_left_width:
                line = line + ' ' * (required_left_width - len(line))

            line = line[:w] + vline_char + padding * ' ' + line[w:]

            required_width = (w + h_width + 1)
            if len(line) < required_width:
                # Fill in the right with spaces
                line = line + ' ' * (required_width - len(line))

            line = line[:required_width] + vline_char + line[required_width+(padding+2):]

            self.nvim.current.buffer[row] = line


        # Bottom line
        #self.nvim.current.buffer.append(' ' * w + '+' + '-' * h_width + '+', end.row + 1)
        self.helper.fill(end.row+1, w, ' ', corner_char + hline_char * h_width + corner_char)

        # Top Line
        #self.nvim.current.buffer.append(' ' * w + '+' + '-' * h_width + '+', start.row)
        self.helper.fill(start.row-1, w, ' ', corner_char + hline_char * h_width + corner_char)


