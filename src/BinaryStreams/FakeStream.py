from io import BytesIO

from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams import CLEAR_TABLE


class FakeOutputStream(OutputBinaryFileStream):
    def __init__(self, file_handle: BytesIO):
        super().__init__(file_handle)
        self.c = []
        self.b = []
        self.last_current_bits_size = self.current_bits_size

    def write(self, value):
        if value == CLEAR_TABLE:
            assert self.last_current_bits_size == self.current_bits_size

        self.c.append(value)
        self.b.append(self.current_bits_size)
        self.last_current_bits_size = self.current_bits_size


class FakeInputStream(InputBinaryFileStream):
    def __init__(self, file_handle: BytesIO, c: list, b: list):
        super().__init__(file_handle, 0)
        self.c = c
        self.b = b
        self.last_current_bits_size = self.current_bits_size

    def read(self):
        if not self.c:
            raise EOFError
        req = self.b.pop(0)
        if req != self.current_bits_size:
            print(req)
            print(self.current_bits_size)
            print(self.c.pop(0))
            raise AssertionError
        val = self.c.pop(0)
        if val == CLEAR_TABLE:
            assert self.last_current_bits_size == self.current_bits_size
        self.last_current_bits_size = self.current_bits_size
        return val
