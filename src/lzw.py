import argparse
import os

from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams.InputCompressedFileStream import InputCompressedFileStream
from CompressedStreams.OutputCompressedFileStream import OutputCompressedFileStream

args = argparse.ArgumentParser()
args.add_argument("-i", help="Input file path", required=True)
args.add_argument("-o", help="Output file path", required=True)
group = args.add_mutually_exclusive_group(required=False)
group.add_argument("-d", action='store_true', help="Decompress", default=False)
group.add_argument("-c", action='store_true', help="Compress", default=True)

parsed_args = args.parse_args()
print(parsed_args)

input_file_object = open(parsed_args.i, "rb")
output_file_object = open(parsed_args.o, "wb")

if parsed_args.c and not parsed_args.d:
    output_file_stream = OutputBinaryFileStream(output_file_object)
    output_compressed_stream = OutputCompressedFileStream(output_file_stream)
    output_compressed_stream.compress(input_file_object)
    output_file_stream.flush()
    output_file_object.flush()

if parsed_args.d:
    input_file_stream = InputBinaryFileStream(input_file_object, os.path.getsize(parsed_args.i) / 4)
    input_compressed_stream = InputCompressedFileStream(input_file_stream)
    input_compressed_stream.decompress(output_file_object)
    output_file_object.flush()
