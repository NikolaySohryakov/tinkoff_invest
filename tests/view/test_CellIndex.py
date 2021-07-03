import unittest
from view.XlsXRenderer import CellIterator


class CellIteratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cell_index = CellIterator(col='A', row=1)

    def test_string_representation(self):
        cell_index = CellIterator(col='B', row=5)

        self.assertEqual(cell_index.__str__(), 'B5')

    def test_does_not_accept_none_col(self):
        with self.assertRaises(BaseException):
            CellIterator(col=None, row=5)

    def test_does_not_accept_none_row(self):
        with self.assertRaises(BaseException):
            CellIterator(col='B', row=None)

    def test_next_row(self):
        self.cell_index.next_row()

        self.assertEqual(self.cell_index.__str__(), 'A2')

    def test_next_col(self):
        self.cell_index.next_col()

        self.assertEqual(self.cell_index.__str__(), 'B1')

    def test_next_col_last(self):
        self.cell_index.col = 'Z'
        self.cell_index.next_col()

        self.assertEqual(self.cell_index.__str__(), 'AA1')

    def test_next_col_double(self):
        self.cell_index.col = 'AA'
        self.cell_index.next_col()

        self.assertEqual(self.cell_index.__str__(), 'AB1')

    def test_init_with_index(self):
        index = CellIterator('A33')

        self.assertEqual(index.col, 'A')
        self.assertEqual(index.row, 33)


if __name__ == '__main__':
    unittest.main()
