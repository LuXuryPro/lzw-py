import struct
from io import BytesIO

from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream


class OutputCompressedFileStream:
    def __init__(self, output_binary_file_stream: OutputBinaryFileStream, max_bits_size):
        """

        :param output_binary_file_stream: wyjsciowy strumen bitowy do opakowania
        """
        self.max_bits_size = max_bits_size
        self.output_binary_file_stream = output_binary_file_stream
        self.clear_dictionary()

    def compress(self, input_binary_file_object: BytesIO):
        """

        Kompresuje wskazany plik
        
        Wynik kompresji jest zapisywany w opakowanym strumieniu
        output_binary_file_stream

        :param input_binary_file_object: plik z którego czytać dane do skompresowania
        """
        w = ""
        input_byte = input_binary_file_object.read(1)
        while input_byte != b'':
            self.maintain_dictionary_capacity()
            input_byte = chr(struct.unpack("B", input_byte)[0])
            wc = w + input_byte
            if wc in self.dictionary:
                w = wc
            else:
                self.output_binary_file_stream.write(self.dictionary[w])
                # Add wc to the dictionary.
                self.dictionary[wc] = self.dict_size
                self.dict_size += 1
                w = input_byte

                if self.dict_size == 2 ** self.output_binary_file_stream.current_bits_size + 1:
                    self.output_binary_file_stream.increase_bit_code_size()

            input_byte = input_binary_file_object.read(1)

        # Output the code for w.
        if w:
            self.output_binary_file_stream.write(self.dictionary[w])

    def clear_dictionary(self):
        self.dict_size = 256
        self.dictionary = {chr(i): i for i in range(self.dict_size)}

    def maintain_dictionary_capacity(self):
        if self.dict_size + 1 == 2 ** self.output_binary_file_stream.current_bits_size + 1:
            self.output_binary_file_stream.increase_bit_code_size()
        if self.output_binary_file_stream.current_bits_size == self.max_bits_size:
            self.output_binary_file_stream.reset_bit_code_size()
            self.clear_dictionary()
