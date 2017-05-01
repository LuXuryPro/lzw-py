from unittest import TestCase

from io import BytesIO

from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams.InputCompressedFileStream import InputCompressedFileStream
from CompressedStreams.OutputCompressedFileStream import OutputCompressedFileStream


class TestOutputCompressedFileStream(TestCase):
    def test_compression(self):
        bytes = b"12345123451234512345asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd"
        file_handle = BytesIO(bytes)
        output_file_handle = BytesIO()
        output_binary_file_stream = OutputBinaryFileStream(output_file_handle)
        compressed_stream = OutputCompressedFileStream(output_binary_file_stream)
        compressed_stream.compress(file_handle)

        output_binary_file_stream.flush()
        print(output_file_handle.getvalue().__sizeof__())
        output_file_handle.seek(0)

        input_binary_file_stream = InputBinaryFileStream(output_file_handle, output_binary_file_stream.counter)
        decompresed_file_stream = InputCompressedFileStream(input_binary_file_stream)
        decompresed_file_handle = BytesIO()
        decompresed_file_stream.decompress(decompresed_file_handle)
        self.assertEquals(decompresed_file_handle.getvalue(), bytes)
        print(decompresed_file_handle.getvalue().__sizeof__())
        print(bytes.__sizeof__())
