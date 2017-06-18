import struct
from io import BytesIO

import math

from BinaryStreams import MIN_BITS_SIZE


class OutputBinaryFileStream:
    """
    Zapisuje wartości ze słownika lzw na ustalonej liczbie bitów
    """

    def __init__(self, file_handle: BytesIO):
        self.max_buffer_size = 32
        self.remaining_bits = 0
        self.file_handle = file_handle
        self.buffer = 0
        self.current_buffer_size = 0
        self.reset_bit_code_size()
        self.counter = 0
        self.num_writen_symbols = 0
        self.sum_written_bits = 0

    def increase_bit_code_size(self):
        self.current_bits_size += 1

    def reset_bit_code_size(self):
        self.current_bits_size = MIN_BITS_SIZE

    def check_if_value_fits_bit_code_size(self, value, size):
        if value == 0:
            return
        if math.floor(math.log2(value)) + 1 > size:
            raise OverflowError(
                "Attempt to write {value} using {size} bits".format(value=value, size=self.current_bits_size))

    def _write_current_buffer(self):
        byte = struct.pack("B", self.buffer)
        self.file_handle.write(byte)
        self.buffer = 0
        self.counter += 1

    def write(self, value):
        self.check_if_value_fits_bit_code_size(value, self.current_bits_size)
        bits_to_write = self.current_bits_size

        # write remaining bits to fill previous byte
        bits_writen = 0

        if self.remaining_bits:
            bits_writen = 8 - self.remaining_bits
            rem = value & (2**bits_writen - 1)
            value >>= bits_writen
            bits_to_write -= bits_writen

            self.buffer <<= bits_writen
            self.buffer |= rem
            self._write_current_buffer()
            self.remaining_bits = 0

        num_whole_bytes = int(bits_to_write / 8)
        for i in range(num_whole_bytes):
            v = value & 0xFF
            value >>= 8
            self.buffer = v
            self._write_current_buffer()
        self.remaining_bits = bits_to_write % 8
        self.buffer = value
        self.num_writen_symbols += 1
        self.sum_written_bits += self.current_bits_size

    def flush(self):
        if self.remaining_bits:
            self.buffer <<= 8 - self.remaining_bits
            self._write_current_buffer()

