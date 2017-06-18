import argparse
import os

from os.path import isfile, join, split

from BinaryStreams.InputBinaryFileStream import InputBinaryFileStream
from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams.InputCompressedFileStream import InputCompressedFileStream
from CompressedStreams.OutputCompressedFileStream import OutputCompressedFileStream


def lzw(parsed_args):

    if parsed_args.a and parsed_args.c and not parsed_args.d:
        compress_all(parsed_args)
        return

    if parsed_args.a and parsed_args.d:
        decompress_all(parsed_args)
        return

    input_file_object = open(parsed_args.i, "rb")
    output_file_object = open(parsed_args.o, "wb")

    if parsed_args.c and not parsed_args.d:
        compress(input_file_object, output_file_object, parsed_args)

    if parsed_args.d:
        decompress(input_file_object, output_file_object, parsed_args)


def compress(input_file_object, output_file_object, parsed_args):
    input_file_size = os.path.getsize(parsed_args.i)
    output_file_stream = OutputBinaryFileStream(output_file_object)
    output_compressed_stream = OutputCompressedFileStream(output_file_stream, parsed_args.b)
    output_compressed_stream.compress(input_file_object)
    output_file_stream.flush()
    print("Bits per output symbol = {bits:.6f}".format(bits=output_file_stream.sum_written_bits/output_file_stream.num_writen_symbols))
    print("Bits per input symbol = {bits:.6f}".format(bits=output_file_stream.sum_written_bits/input_file_size))
    print("Compression Ratio = {ratio:.6f}".format(ratio=input_file_size/output_file_stream.counter))
    output_file_object.flush()


def decompress(input_file_object, output_file_object, parsed_args):
    input_file_stream = InputBinaryFileStream(input_file_object, os.path.getsize(parsed_args.i))
    input_compressed_stream = InputCompressedFileStream(input_file_stream)
    input_compressed_stream.decompress(output_file_object)
    output_file_object.flush()


def compress_all(parsed_args):
    files = get_all_files_names_from_directory(parsed_args.i)
    for file in files:
        file_in = open(file, "rb")
        file_out = split(file)[-1] + "_c"
        file_out = open(join(parsed_args.o, file_out), "wb")
        compress(file_in, file_out, parsed_args)


def decompress_all(parsed_args):
    files = get_all_files_names_from_directory(parsed_args.i)
    for file in files:
        file_in = open(file, "rb")
        file_out = split(file)[-1]
        file_out = file_out[:-2]
        file_out = open(join(parsed_args.o, file_out), "wb")
        decompress(file_in, file_out, parsed_args)

def bit_size(x):
    i = int(x)
    if i < 9:
         raise argparse.ArgumentTypeError("Minimum dictionary bitsize is 9 bits")
    return i

def parse_script_arguments():
    args = argparse.ArgumentParser()
    args.add_argument("i", help="Input file path")
    args.add_argument("o", help="Output file path")
    args.add_argument("-a", help="Proceed all files in input directory", action="store_true")
    args.add_argument("-b", help="Max bit size of dictionary entry", default=12, type=bit_size)
    group = args.add_mutually_exclusive_group(required=False)
    group.add_argument("-d", action='store_true', help="Decompress", default=False)
    group.add_argument("-c", action='store_true', help="Compress", default=True)

    parsed_args = args.parse_args()
    return parsed_args


def get_all_files_names_from_directory(path):
    return [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]

if __name__ == '__main__':
    program_args = parse_script_arguments()
    lzw(program_args)
