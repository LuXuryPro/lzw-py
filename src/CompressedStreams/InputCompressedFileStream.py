from io import BytesIO

from BinaryStreams import InputBinaryFileStream


class InputCompressedFileStream:
    def __init__(self, input_binary_file_stream: InputBinaryFileStream):
        """

        :param input_binary_file_stream: wejsciowy strumen bitowy do opakowania
        """
        self.input_binary_file_stream = input_binary_file_stream
        super().__init__()

    def decompress(self, output_binary_file_object: BytesIO):
        """
        Dekompresuje opakowany strumen wejsciowy do wskazanego pliku

        :param output_binary_file_object: plik do którego zapisać wynik dekompresji 
        """
        dict_size = 256
        dictionary = {i: bytes([i]) for i in range(dict_size)}

        w = self.input_binary_file_stream.read()
        output_binary_file_object.write(bytes([w]))
        w = bytes([w])
        while True:
            if dict_size + 1 == 2 ** self.input_binary_file_stream.current_bits_size + 1:
                self.input_binary_file_stream.increase_bit_code_size()

            value = self.input_binary_file_stream.read()
            if value == b"":
                break

            if value in dictionary:
                entry = dictionary[value]
            elif value == dict_size:
                entry = w + bytes([w[0]])
            else:
                raise ValueError('Bad compressed k: %s' % value)
            output_binary_file_object.write(entry)

            dictionary[dict_size] = w + bytes([entry[0]])
            dict_size += 1

            w = entry
