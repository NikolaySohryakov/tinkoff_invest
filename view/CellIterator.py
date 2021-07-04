import re

cell_index_parts = re.compile(r'(\$?)([A-Z]{1,3})(\$?)(\d+)')


class CellIterator:
    def __init__(self, *args, **kwargs):
        try:
            # First arg is an int, default to row/col notation.
            if len(kwargs) == 2:
                self.row = kwargs['row']
                self.col = kwargs['col']
            else:
                raise ValueError
        except ValueError:
            match = cell_index_parts.match(args[0])
            col_str = match.group(2)
            row = int(match.group(4))

            self.col = col_str
            self.row = row

    def next_row(self):
        self.row += 1

    def next_col(self):
        if self.col[-1:].upper() == 'Z':
            self.col = 'A' + self.col[:-1] + 'A'
        else:
            next_char = chr(ord(self.col[-1:]) + 1)

            self.col = self.col[:-1] + next_char

    def col_index(self) -> int:
        """Zero-based index or a column."""
        result = 0

        for index, char in enumerate(self.col):
            result += ord(char.upper()) - ord('A') + (ord('Z') - ord('A') + 1) * index

        return result

    def row_index(self) -> int:
        """Zero-based index of a row."""
        return self.row - 1

    def __str__(self):
        return self.col.upper() + str(self.row)