import struct
from io import BytesIO

import math

from BinaryStreams import MIN_BITS_SIZE


class InputBinaryFileStream:
    """
    Czyta z pliku wartości ze słownika lzw na ustalonej liczbie bitów
    """

    def __init__(self, file_handle: BytesIO, size):
        """

        :param file_handle: plik do czytania
        :param size: ile pełnych 32 bit intow przeczytac z pliku
        """
        self.max_buffer_size = 32
        self.remaining_bits = 0
        self.file_handle = file_handle
        self.file_handle.seek(0)
        self.buffer = 0
        self.current_buffer_size = 0
        self.reset_bit_code_size()
        self.eof = False
        self.size = size

    def increase_bit_code_size(self):
        self.current_bits_size += 1

    def reset_bit_code_size(self):
        self.current_bits_size = MIN_BITS_SIZE

    def _read_buffer(self):
        if self.size == 0:
            raise OverflowError
        byte = self.file_handle.read(1)
        self.buffer = struct.unpack("B", byte)[0]
        self.size -= 1

    def read(self):

        bits_to_read = self.current_bits_size
        value_to_return = 0
        re = bits_to_read
        if self.remaining_bits:
            value_to_return |= (self.buffer)
            self.buffer = 0
            re -= self.remaining_bits

        remaining_bits = re % 8

        num_whole_bytes = int(re / 8)
        for i in range(num_whole_bytes):
            self._read_buffer()
            value_to_return |= self.buffer << (i*8 + self.remaining_bits)
            re -= 8

        if remaining_bits:
            self._read_buffer()
            re -= remaining_bits
            assert (re == 0)
            value_to_return |= ((self.buffer & ((2**(remaining_bits) - 1) << (8 - remaining_bits))) >> (8 - remaining_bits)) << (num_whole_bytes * 8 + self.remaining_bits)
            self.buffer &= 2**(8 - remaining_bits) - 1
            self.remaining_bits = 8 - remaining_bits
        else:
            self.remaining_bits = 0

        return value_to_return







