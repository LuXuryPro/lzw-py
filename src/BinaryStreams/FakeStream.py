from io import BytesIO

from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream


class FakeOutputStream(OutputBinaryFileStream):
    def __init__(self, file_handle: BytesIO):
        super().__init__(file_handle)
        self.c = []
        self.b = []

    def write(self, value):
        self.c.append(value)
        self.b.append(self.current_bits_size)


class FakeInputStream(InputBinaryFileStream):
    def __init__(self, file_handle: BytesIO, c: list, b: list):
        super().__init__(file_handle, 0)
        self.c = c
        self.b = b

    def read(self):
        if not self.c:
            raise OverflowError
        req = self.b.pop(0)
        if req != self.current_bits_size:
            print(req)
            print(self.current_bits_size)
            print(self.c.pop(0))
            raise AssertionError
        return self.c.pop(0)
