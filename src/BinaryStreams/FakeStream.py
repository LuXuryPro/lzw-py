from io import BytesIO

from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream


class FakeOutputStream(OutputBinaryFileStream):
    def __init__(self, file_handle: BytesIO):
        super().__init__(file_handle)
        self.c = []

    def write(self, value):
        self.c.append(value)


class FakeInputStream(InputBinaryFileStream):
    def __init__(self, file_handle: BytesIO, c: list):
        super().__init__(file_handle, 0)
        self.c = c

    def read(self):
        if not self.c:
            raise OverflowError
        return self.c.pop(0)
