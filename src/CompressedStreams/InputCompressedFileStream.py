from io import BytesIO

from BinaryStreams import InputBinaryFileStream
from CompressedStreams import NEW_CODE_INDEX, CLEAR_TABLE, INITIAL_DICTIONARY_SIZE


class InputCompressedFileStream:
    def __init__(self, input_binary_file_stream: InputBinaryFileStream):
        """

        :param input_binary_file_stream: wejsciowy strumen bitowy do opakowania
        """
        self.input_binary_file_stream = input_binary_file_stream

    def decompress(self, output_binary_file_object: BytesIO, validator=None):
        """
        Dekompresuje opakowany strumen wejsciowy do wskazanego pliku
        
        Dane są czytane z opakowanego strumienia
        input_binary_file_stream

        :param validator: lista elementów króre powinny być odczytane przy prawidłowym zakodowaniu strumienia.
                          Parametr jest używany w testach jednostkowych.
        :param output_binary_file_object: plik do którego zapisać wynik dekompresji 
        """

        self.clear_dictionary()
        previous_bytes_sequence = b""
        while True:
            try:
                index = self.input_binary_file_stream.read()
                if validator:
                    ov = validator.pop(0)
                    if index != ov:
                        print(index)
                        print(ov)
                        print(validator)
                        assert (False)
                if index == CLEAR_TABLE:
                    self.input_binary_file_stream.reset_bit_code_size()
                    previous_bytes_sequence = b""
                    self.clear_dictionary()
                    continue
            except EOFError:
                break
            if index in self.dictionary:
                bytes_sequence = self.dictionary[index]
            elif index == self.new_value_index:
                bytes_sequence = previous_bytes_sequence + bytes([previous_bytes_sequence[0]])
            else:
                raise ValueError('LZW Stream exception at index: %s' % index)

            output_binary_file_object.write(bytes_sequence)

            if previous_bytes_sequence:
                self.dictionary[self.new_value_index] = previous_bytes_sequence + bytes([bytes_sequence[0]])
                self.new_value_index += 1
                if self.new_value_index + 1 == 2 ** self.input_binary_file_stream.current_bits_size:
                    self.input_binary_file_stream.increase_bit_code_size()
            previous_bytes_sequence = bytes_sequence

    def clear_dictionary(self):
        num_elements = INITIAL_DICTIONARY_SIZE
        self.dictionary = {i: bytes([i]) for i in range(num_elements)}
        self.new_value_index = NEW_CODE_INDEX
