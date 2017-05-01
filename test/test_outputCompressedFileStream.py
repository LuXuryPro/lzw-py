import struct
from unittest import TestCase
from io import BytesIO

from InputBinaryFileStream import InputBinaryFileStream
from OutputBinaryFileStream import OutputBinaryFileStream


class TestOutputCompressedFileStream(TestCase):
    def test_can_create(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)

    def test_can_write_bits_to_stream(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"\xff\xff\xff\xff")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"\xff\xff\xff\xff")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"\xff\xff\xff\xff")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"\xff\xff\xff\xff")
        output_binary_file_stream.write((1 << 9) - 1)
        self.assertEquals(file_handle.getvalue(), b"\xff\xff\xff\xff\xff\xff\xff\xff")

    def test_write_read(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)
        input_binary_file_stream = InputBinaryFileStream(file_handle)
        for i in range(20):
            output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.flush()
        file_handle.seek(0)

        for i in range(20):
            print(i)
            self.assertEquals(input_binary_file_stream.read(), ((1 << 9) - 1))
