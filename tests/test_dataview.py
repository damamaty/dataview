import unittest
import itertools
from dataview import DataView


class TestDataView(unittest.TestCase):
    def setUp(self):
        self.sources = [list(range(x)) for x in range(10)]

    def test_key_is_not_int(self):
        view = DataView(self.sources[0])
        self.assertRaises(TypeError, lambda: view[1.5])
        self.assertRaises(TypeError, lambda: view["1.5"])

    def test_view_slice_equal_source_slice(self):
        for source in self.sources:
            view = DataView(source)

            products = self.__slice_products(len(source))
            for product in products:
                slice_ = slice(*product)
                self.assertEqual(source[slice_], list(view[slice_]))

    def test_view_equal_source_slice(self):
        for source in self.sources:
            products = self.__slice_products(len(source))

            for product in products:
                expected = source[slice(*product)]
                result = list(DataView(source, *product))

                self.assertEqual(expected, result)

    def test_view_view_equal_source_view(self):
        for source in self.sources:
            products = self.__slice_products(len(source))

            for product1 in products:
                for product2 in products:
                    excepted = source[slice(*product1)][slice(*product2)]

                    results = [
                        DataView(source, *product1)[slice(*product2)],
                        DataView(source)[slice(*product1)][slice(*product2)],
                        DataView(source[slice(*product1)], *product2)
                    ]

                    for result in results:
                        self.assertEqual(excepted, list(result))

    @staticmethod
    def __slice_products(length):
        values = itertools.chain(range(-2 * length, 2 * length), [None])

        return list(itertools.product(values))
