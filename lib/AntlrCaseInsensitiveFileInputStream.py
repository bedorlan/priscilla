import antlr4

class AntlrCaseInsensitiveFileInputStream(antlr4.FileStream):

    def __init__(self, filename):
        super().__init__(filename)
        input_lower = self.strdata.upper()
        self._lookaheadData = [ord(c) for c in input_lower]

    def LA(self, offset: int):
        if offset == 0:
            return 0 # undefined
        if offset < 0:
            offset += 1 # e.g., translate LA(-1) to use offset=0
        pos = self._index + offset - 1
        if pos < 0 or pos >= self._size: # invalid
            return antlr4.Token.EOF
        return self._lookaheadData[pos]
