class LZWStream:
    def __init__(self):
        self.setup_dictionary()

    def setup_dictionary(self):
        self.dict_size = 256
        self.dictionary = {chr(i): i for i in range(self.dict_size)}
