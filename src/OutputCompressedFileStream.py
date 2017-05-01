from OutputBinaryFileStream import OutputBinaryFileStream

from src.BinaryFileObject import BinaryFileObject


class OutputCompressedFileStream:
    def __init__(self, output_binary_file_stream: OutputBinaryFileStream):
        self.output_binary_file_stream = output_binary_file_stream
        self.setup_dictionary()

    def setup_dictionary(self):
        self.dict_size = 256
        self.dictionary = dict((chr(i), i) for i in range(self.dict_size))

    def compress(self, input_binary_file_object: BinaryFileObject):
        w = ""
        for c in input_binary_file_object.get_bytes():
            wc = w + c
            if wc in self.dictionary:
                w = wc
            else:
                self.output_binary_file_stream.write(self.dictionary[w])
                # Add wc to the dictionary.
                self.dictionary[wc] = self.dict_size
                self.dict_size += 1
                w = c

        # Output the code for w.
        if w:
            self.output_binary_file_stream.write(self.dictionary[w])
