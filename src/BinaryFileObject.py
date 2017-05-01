class BinaryFileObject:
    def __init__(self, file_handle):
        self.file_handle = file_handle

    def get_bytes(self):
        byte = self.file_handle.read(1)
        while byte != b"":
            yield int(byte)
            byte = self.file_handle.read(1)
