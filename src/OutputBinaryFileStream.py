import struct
from io import BytesIO

import math


class OutputBinaryFileStream:
    """
    Zapisuje wartości ze słownika lzw na ustalonej liczbie bitów
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

    def check_if_value_fits_bit_code_size(self, value, size):
        if math.log2(value) > size:
            raise OverflowError(
                "Attempt to write {value} using {size} bits".format(value=value, size=self.current_bits_size))

    def _write_current_buffer(self):
        bytes_int = struct.pack(">I", self.buffer)
        print(bytes_int)
        print(self.file_handle.write(bytes_int))
        self.buffer = 0
        self.current_buffer_size = 0

    def _write_to_buffer(self, value, size):
        self.check_if_value_fits_bit_code_size(value, size)
        self.buffer <<= size
        self.buffer |= value
        self.current_buffer_size += size

    def write(self, value):
        new_buffer_size = self.current_buffer_size + self.current_bits_size
        overflow = self.max_buffer_size - new_buffer_size

        if overflow < 0:
            # Too much to put in buffer - must flush
            bits_that_fits_in_buffer = self.current_bits_size + overflow
            to_be_writen_to_buffer_now = value & ((1 << bits_that_fits_in_buffer) - 1)
            self._write_to_buffer(to_be_writen_to_buffer_now, bits_that_fits_in_buffer)
            self._write_current_buffer()
            to_be_writen_to_buffer_later = value >> bits_that_fits_in_buffer
            self._write_to_buffer(to_be_writen_to_buffer_later, -overflow)
        else:
            self._write_to_buffer(value, self.current_bits_size)

    def flush(self):
        self._write_current_buffer()

