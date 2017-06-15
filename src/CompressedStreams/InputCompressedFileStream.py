from io import BytesIO

from BinaryStreams import InputBinaryFileStream


class InputCompressedFileStream:
    def __init__(self, input_binary_file_stream: InputBinaryFileStream, max_bits_size: int):
        """

        :param input_binary_file_stream: wejsciowy strumen bitowy do opakowania
        """
        self.max_bits_size = max_bits_size
        self.input_binary_file_stream = input_binary_file_stream
        self.clear_dictionary()

    def decompress(self, output_binary_file_object: BytesIO):
        """
        Dekompresuje opakowany strumen wejsciowy do wskazanego pliku
        
        Dane są czytane z opakowanego strumienia
        input_binary_file_stream

        :param output_binary_file_object: plik do którego zapisać wynik dekompresji 
        """

        w = self.input_binary_file_stream.read()
        output_binary_file_object.write(bytes([w]))
        w = bytes([w])
        while True:
            try:
                self.maintain_dictionary_capacity()
                value = self.input_binary_file_stream.read()

                if value in self.dictionary:
                    entry = self.dictionary[value]
                elif value == self.dict_size:
                    entry = w + bytes([w[0]])
                else:
                    raise ValueError('LZW Stream exception at value: %s' % value)
                output_binary_file_object.write(entry)

                self.dictionary[self.dict_size] = w + bytes([entry[0]])
                self.dict_size += 1

                w = entry
            except OverflowError:
                break

    def clear_dictionary(self):
        self.dict_size = 256
        self.dictionary = {i: bytes([i]) for i in range(self.dict_size)}

    def maintain_dictionary_capacity(self):
        if self.dict_size + 1 == 2 ** self.input_binary_file_stream.current_bits_size + 1:
            self.input_binary_file_stream.increase_bit_code_size()
        if self.input_binary_file_stream.current_bits_size == self.max_bits_size:
            self.input_binary_file_stream.reset_bit_code_size()
            self.clear_dictionary()

