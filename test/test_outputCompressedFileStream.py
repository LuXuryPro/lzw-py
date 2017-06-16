import random
from io import BytesIO
from unittest import TestCase

from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream


class TestOutputCompressedFileStream(TestCase):
    def test_can_create(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)

    def test_can_write_bits_to_stream(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)
        output_binary_file_stream.write((1 << 9) - 1)

    def test_write_read(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)
        for i in range(512):
            output_binary_file_stream.write(i)
        output_binary_file_stream.increase_bit_code_size()
        for i in range(512, 1024):
            output_binary_file_stream.write(i)
        output_binary_file_stream.increase_bit_code_size()
        for i in range(1024, 2048):
            output_binary_file_stream.write(i)
        output_binary_file_stream.reset_bit_code_size()
        for i in range(512):
            output_binary_file_stream.write(i)
        output_binary_file_stream.increase_bit_code_size()
        for i in range(512, 1000):
            output_binary_file_stream.write(i)
        output_binary_file_stream.increase_bit_code_size()
        for i in range(1024, 2000):
            output_binary_file_stream.write(i)
        output_binary_file_stream.increase_bit_code_size()
        for i in range(2000, 4000):
            output_binary_file_stream.write(i)
        output_binary_file_stream.flush()

        file_handle.seek(0)

        input_binary_file_stream = InputBinaryFileStream(file_handle, output_binary_file_stream.counter)
        for i in range(512):
            self.assertEquals(input_binary_file_stream.read(),i)
        input_binary_file_stream.increase_bit_code_size()
        for i in range(512, 1024):
            self.assertEquals(input_binary_file_stream.read(),i)
        input_binary_file_stream.increase_bit_code_size()
        for i in range(1024, 2048):
            self.assertEquals(input_binary_file_stream.read(),i)
        input_binary_file_stream.reset_bit_code_size()
        for i in range(512):
            self.assertEquals(input_binary_file_stream.read(),i)
        input_binary_file_stream.increase_bit_code_size()
        for i in range(512, 1000):
            self.assertEquals(input_binary_file_stream.read(),i)
        input_binary_file_stream.increase_bit_code_size()
        for i in range(1024, 2000):
            self.assertEquals(input_binary_file_stream.read(),i)
        input_binary_file_stream.increase_bit_code_size()
        for i in range(2000, 4000):
            self.assertEquals(input_binary_file_stream.read(),i)

    def test_write_read_inc(self):
        file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(file_handle)
        for i in range(500):
            output_binary_file_stream.write(i)

        output_binary_file_stream.increase_bit_code_size()

        for i in range(1000):
            output_binary_file_stream.write(i)

        output_binary_file_stream.flush()
        file_handle.seek(0)

        input_binary_file_stream = InputBinaryFileStream(file_handle, output_binary_file_stream.counter)
        for i in range(500):
            self.assertEquals(input_binary_file_stream.read(), i)

        input_binary_file_stream.increase_bit_code_size()

        for i in range(1000):
            self.assertEquals(input_binary_file_stream.read(), i)
