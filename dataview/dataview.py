from collections import Sequence


class DataView(Sequence):
    def __init__(self, data, *args):
        self.__data = data

        slice_ = slice(*args) if args else slice(None, None, None)

        self.__start, self.__stop, self.__step = slice_.start, slice_.stop, slice_.step
        self.__calculate_indices()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data
        self.__calculate_indices()

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value
        self.__calculate_indices()

    @property
    def stop(self):
        return self.__stop

    @stop.setter
    def stop(self, value):
        self.__stop = value
        self.__calculate_indices()

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        if value == 0:
            raise ValueError("DataView step cannot be zero")

        self.__step = value
        self.__calculate_indices()

    def __calculate_indices(self):
        self.__indices = slice(self.start, self.stop, self.step).indices(len(self.data))

    def __getitem__(self, item):
        if type(item) == slice:
            if item.step == 0:
                raise ValueError("slice step cannot be zero")

            return DataView(self, item.start, item.stop, item.step)

        elif type(item) == int:
            if item in range(len(self)):
                return self.data[self.__indices[0] + item * self.__indices[2]]
            elif item in range(-len(self), 0):
                return self.data[self.__indices[0] + (item + len(self)) * self.__indices[2]]
            else:
                raise IndexError("DataView index out of range")

        else:
            raise TypeError("DataView indices should be integer")

    def __len__(self):
        return len(range(*self.__indices))

    def __repr__(self):
        return str(list(self))
