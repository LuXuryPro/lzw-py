from io import BytesIO

from BinaryStreams import InputBinaryFileStream
from CompressedStreams import NEW_CODE_INDEX, CLEAR_TABLE, INITIAL_DICTIONARY_SIZE


class InputCompressedFileStream:
    def __init__(self, input_binary_file_stream: InputBinaryFileStream):
        """

        :param input_binary_file_stream: wejsciowy strumen bitowy do opakowania
        """
        self.input_binary_file_stream = input_binary_file_stream

    def decompress(self, output_binary_file_object: BytesIO, validator):
        """
        Dekompresuje opakowany strumen wejsciowy do wskazanego pliku
        
        Dane są czytane z opakowanego strumienia
        input_binary_file_stream

        :param output_binary_file_object: plik do którego zapisać wynik dekompresji 
        """

        self.clear_dictionary()
        w = b""
        while True:
            try:
                value = self.input_binary_file_stream.read()
                ov = validator.pop(0)
                if value != ov:
                    print(value)
                    print(ov)
                    print(validator)
                    assert (False)
                if value == CLEAR_TABLE:
                    print("CLEAR")
                    self.input_binary_file_stream.reset_bit_code_size()
                    w = b""
                    self.clear_dictionary()
                    continue
            except OverflowError:
                break
            if value in self.dictionary:
                entry = self.dictionary[value]
            elif value == self.new_value_index:
                entry = w + bytes([w[0]])
            else:
                raise ValueError('LZW Stream exception at value: %s %s' % (value, self.new_value_index))

            output_binary_file_object.write(entry)

            if w:
                self.dictionary[self.new_value_index] = w + bytes([entry[0]])
                self.new_value_index += 1
            w = entry
            if self.new_value_index + (w != b"") == 2 ** self.input_binary_file_stream.current_bits_size:
                print("UP")
                self.input_binary_file_stream.increase_bit_code_size()

    def clear_dictionary(self):
        num_elements = INITIAL_DICTIONARY_SIZE
        self.dictionary = {i: bytes([i]) for i in range(num_elements)}
        self.new_value_index = NEW_CODE_INDEX


