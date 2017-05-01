import struct
from io import BytesIO

import math


class InputBinaryFileStream:
    """
    Czyta z pliku wartości ze słownika lzw na ustalonej liczbie bitów
    """

    def __init__(self, file_handle: BytesIO):
        self.max_buffer_size = 32
        self.file_handle = file_handle
        self.buffer = 0
        self.current_buffer_size = 0
        self.reset_bit_code_size()

    def increase_bit_code_size(self):
        self.current_bits_size += 1

    def reset_bit_code_size(self):
        self.current_bits_size = 9

    def _read_buffer(self):
        bytes_int = self.file_handle.read(4)
        self.buffer = struct.unpack(">I", bytes_int)[0]
        self.current_buffer_size = 32

    def read(self):
        left_in_buffer = self.current_buffer_size - self.current_bits_size

        if left_in_buffer < 0:
            # Too much to put in buffer - must flush
            return_value = 0
            return_value |= self.buffer
            left_to_read = self.current_bits_size - self.current_buffer_size
            self._read_buffer()
            return_value <<= left_to_read
            return_value |= self.buffer & ((1 << left_to_read) - 1)
            self.buffer >>= left_to_read
            self.current_buffer_size -= left_to_read
            return return_value
        else:
            return_value = 0
            return_value |= self.buffer & ((1 << self.current_bits_size) - 1)
            self.buffer >>= self.current_bits_size
            self.current_buffer_size -= self.current_bits_size
            return return_value
