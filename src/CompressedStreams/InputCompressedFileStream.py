from io import BytesIO

from BinaryStreams import InputBinaryFileStream
from CompressedStreams.LZWCompressedFileStream import LZWStream


class InputCompressedFileStream(LZWStream):
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
        self.setup_dictionary()
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}

        w = self.input_binary_file_stream.read()
        output_binary_file_object.write(bytes([w]))
        w = chr(w)
        value = self.input_binary_file_stream.read()
        while value != b"":
            if value in dictionary:
                entry = dictionary[value]
            elif value == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % value)
            output_binary_file_object.write(entry.encode("ascii"))

            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry
            value = self.input_binary_file_stream.read()
