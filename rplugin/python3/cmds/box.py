from .command import Command
import argparse

class BoxCommand(Command):
    def __init__(self, nvim, helper):
        super().__init__(nvim, helper)

    def run(self, args, rg):
        parser = argparse.ArgumentParser()
        parser.add_argument('--hpadding', type=int, default=self.helper.get_setting("ascii_default_hpadding"))
        parser.add_argument('--vpadding', type=int, default=self.helper.get_setting("ascii_default_vpadding"))

        args = parser.parse_args(args)

        hpadding = args.hpadding
        vpadding = args.vpadding

        start, end = self.helper.get_selection()

        width = abs(start.col - end.col) + 1

#        width = 0
#        for row in range(start.row, end.row+1):
#            #width = max(width, start.col + len(self.nvim.current.buffer[row].strip()))
#            width = max(width, len(self.nvim.current.buffer[row]) - start.col)

        height = abs(start.row - end.row)

        left_offset = start.col + hpadding
        w = start.col
        h_width = width + hpadding * 2

        # If vpadding > 0, insert blank lines on bottom if the buffer is too small
        # Bottom
        if self.helper.get_buffer_max_lines() < end.row + vpadding + 1:
            #self.nvim.current.buffer.append(str(end.row + vpadding + 1))

            for _ in range(end.row + vpadding - self.helper.get_buffer_max_lines() + 3):
                self.nvim.current.buffer.append('', end.row + 1)

        # Adjust position
        start.row -= vpadding
        end.row += vpadding

        hline_char = self.helper.get_setting("ascii_hline_char")[0]
        vline_char = self.helper.get_setting("ascii_vline_char")[0]
        corner_char = self.helper.get_setting("ascii_corner_char")[0]

        # Left and right bars
        for row in range(start.row, end.row+1):
            line = self.nvim.current.buffer[row]

            required_left_width = (w + hpadding + 1)
            if len(line) < required_left_width:
                line = line + ' ' * (required_left_width - len(line))

            line = line[:w] + vline_char + hpadding * ' ' + line[w:]

            required_width = (w + h_width + 1)
            if len(line) < required_width:
                # Fill in the right with spaces
                line = line + ' ' * (required_width - len(line))

            line = line[:required_width] + vline_char + line[required_width+(hpadding+2):]

            self.nvim.current.buffer[row] = line


        # Bottom line
        self.helper.fill(end.row+1, w, ' ', corner_char + hline_char * h_width + corner_char)

        # Top Line
        self.helper.fill(start.row-1, w, ' ', corner_char + hline_char * h_width + corner_char)


