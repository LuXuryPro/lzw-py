import os
import random
from unittest import TestCase

from io import BytesIO

from BinaryStreams.FakeStream import FakeOutputStream, FakeInputStream
from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams.InputCompressedFileStream import InputCompressedFileStream
from CompressedStreams.OutputCompressedFileStream import OutputCompressedFileStream


class TestOutputCompressedFileStream(TestCase):
    def test_compression(self):
        byte = b"\x01\x02\x03"
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        print(len(byte))
        file_handle = BytesIO(byte)
        output_file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(output_file_handle)
        max_bits_size = 10
        ff = FakeOutputStream(output_file_handle)
        compressed_stream = OutputCompressedFileStream(ff, max_bits_size)
        compressed_stream.compress(file_handle)

        output_binary_file_stream.flush()
        print(output_file_handle.getvalue().__sizeof__())
        output_file_handle.seek(0)

        input_binary_file_stream = InputBinaryFileStream(output_file_handle, output_binary_file_stream.counter)
        fi = FakeInputStream(output_file_handle, ff.c, ff.b)
        decompresed_file_stream = InputCompressedFileStream(fi)
        decompresed_file_handle = BytesIO()
        decompresed_file_stream.decompress(decompresed_file_handle, compressed_stream.validator)
        self.assertEquals(decompresed_file_handle.getvalue(), byte)
        print(decompresed_file_handle.getvalue().__sizeof__())
        print(byte.__sizeof__())

    def test_compression_real(self):
        byte = b"\x01\x02\x03"
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        byte = byte + byte + byte + byte
        file_handle = BytesIO(byte)
        output_file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(output_file_handle)
        max_bits_size = 10
        compressed_stream = OutputCompressedFileStream(output_binary_file_stream, max_bits_size)
        compressed_stream.compress(file_handle)

        output_binary_file_stream.flush()
        print(output_file_handle.getvalue().__sizeof__())
        output_file_handle.seek(0)

        input_binary_file_stream = InputBinaryFileStream(output_file_handle, output_binary_file_stream.counter)
        decompresed_file_stream = InputCompressedFileStream(input_binary_file_stream)
        decompresed_file_handle = BytesIO()
        decompresed_file_stream.decompress(decompresed_file_handle, compressed_stream.validator)
        self.assertEquals(decompresed_file_handle.getvalue(), byte)
        print(decompresed_file_handle.getvalue().__sizeof__())
        print(byte.__sizeof__())

    def test_random_data(self):
        for i in range(100):
            bytes = bytearray(os.urandom(10000))
            file_handle = BytesIO(bytes)
            output_file_handle = BytesIO()
            output_binary_file_stream = OutputBinaryFileStream(output_file_handle)
            max_bits_size = random.randint(9, 32)
            compressed_stream = OutputCompressedFileStream(output_binary_file_stream, max_bits_size)
            compressed_stream.compress(file_handle)

            output_binary_file_stream.flush()
            print(output_file_handle.getvalue().__sizeof__())
            output_file_handle.seek(0)

            input_binary_file_stream = InputBinaryFileStream(output_file_handle, output_binary_file_stream.counter)
            decompresed_file_stream = InputCompressedFileStream(input_binary_file_stream)
            decompresed_file_handle = BytesIO()
            decompresed_file_stream.decompress(decompresed_file_handle, compressed_stream.validator)
            self.assertEquals(decompresed_file_handle.getvalue(), bytes)
            print(decompresed_file_handle.getvalue().__sizeof__())
            print(bytes.__sizeof__())

    def test_random_data2(self):
        for i in range(100):
            byte= bytes(bytearray(os.urandom(10000)))
            print(len(byte))
            file_handle = BytesIO(byte)
            output_file_handle = BytesIO()
            output_binary_file_stream = OutputBinaryFileStream(output_file_handle)
            max_bits_size = random.randint(9, 32)
            ff = FakeOutputStream(output_file_handle)
            compressed_stream = OutputCompressedFileStream(ff, max_bits_size)
            compressed_stream.compress(file_handle)

            output_binary_file_stream.flush()
            print(output_file_handle.getvalue().__sizeof__())
            output_file_handle.seek(0)

            input_binary_file_stream = InputBinaryFileStream(output_file_handle, output_binary_file_stream.counter)
            fi = FakeInputStream(output_file_handle, ff.c, ff.b)
            decompresed_file_stream = InputCompressedFileStream(fi)
            decompresed_file_handle = BytesIO()
            decompresed_file_stream.decompress(decompresed_file_handle, compressed_stream.validator)
            self.assertEquals(decompresed_file_handle.getvalue(), byte)
            print(decompresed_file_handle.getvalue().__sizeof__())
            print(byte.__sizeof__())
