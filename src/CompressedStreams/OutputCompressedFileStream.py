from io import BytesIO

from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams.LZWCompressedFileStream import LZWStream


class OutputCompressedFileStream(LZWStream):
    def __init__(self, output_binary_file_stream: OutputBinaryFileStream):
        """

        :param output_binary_file_stream: wyjsciowy strumen bitowy do opakowania
        """
        self.output_binary_file_stream = output_binary_file_stream
        super().__init__()

    def compress(self, input_binary_file_object: BytesIO):
        """

        Kompresuje wskazany plik

        :param input_binary_file_object: plik do którego czytać dane do skompresowania
        """
        w = ""
        input_byte = input_binary_file_object.read(1)
        while input_byte != b'':
            input_byte = input_byte.decode('utf8')
            wc = w + input_byte
            if wc in self.dictionary:
                w = wc
            else:
                self.output_binary_file_stream.write(self.dictionary[w])
                # Add wc to the dictionary.
                self.dictionary[wc] = self.dict_size
                self.dict_size += 1
                w = input_byte
            input_byte = input_binary_file_object.read(1)

        # Output the code for w.
        if w:
            self.output_binary_file_stream.write(self.dictionary[w])
