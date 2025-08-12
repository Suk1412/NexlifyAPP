from collections.abc import ByteString
from funcy import compose


class Bytes:
    """Primitive that fuzzes a binary byte string with arbitrary length.

    :type name: str, optional
    :param name: Name, for referencing later. Names should always be provided, but if not, a default name will be given,
        defaults to None
    :type default_value: bytes, optional
    :param default_value: Value used when the element is not being fuzzed - should typically represent a valid value,
        defaults to b""
    :type size: int, optional
    :param size: Static size of this field, leave None for dynamic, defaults to None
    :type padding: chr, optional
    :param padding: Value to use as padding to fill static field size, defaults to b"\\x00"
    :type max_len: int, optional
    :param max_len: Maximum string length, defaults to None
    :type fuzzable: bool, optional
    :param fuzzable: Enable/disable fuzzing of this primitive, defaults to true
    """

    # This binary strings will always included as testcases.
    _fuzz_library = [
        b"",
        b"\x00",
        b"\xFF",
        b"A" * 10,
        b"A" * 100,
        b"A" * 1000,
        b"A" * 5000,
        b"A" * 10000,
        b"A" * 100000,
    ]
    payload = [0x0000,
               0x0001,
               0x0002,
               0x0003,
               0x0004,
               0x0005,
               0x0006,
               0x0007,
               0x0008,
               0x0009,
               0x000a,
               0x000b,
               0x000c,
               0x000d,
               0x000e,
               0x000f,
               0x0010,
               0x0011,
               0x0012,
               0x0013,
               0x0014,
               0x001e,
               0x001f,
               0x0020,
               0x0021,
               0x003f,
               0x0040,
               0x0041,
               0x007f,
               0x0080,
               0x0081,
               0x00ff,
               0x0100,
               0x0101,
               0x0180,
               0x01ff,
               0x0200,
               0x0201,
               0x0303,
               0x03c0,
               0x03ff,
               0x0400,
               0x0401,
               0x0606,
               0x07e0,
               0x07ff,
               0x0800,
               0x0801,
               0x0c0c,
               0x0f0f,
               0x0ff0,
               0x0fff,
               0x1000,
               0x1001,
               0x1818,
               0x1e1e,
               0x1ff8,
               0x1fff,
               0x1111,
               0x2000,
               0x2001,
               0x2222,
               0x3000,
               0x3030,
               0x3333,
               0x3c3c,
               0x3ffc,
               0x3fff,
               0x4000,
               0x4001,
               0x4444,
               0x5000,
               0x5555,
               0x6000,
               0x6060,
               0x6666,
               0x7000,
               0x7878,
               0x7e7e,
               0x7f7f,
               0x7ffe,
               0x7fff,
               0x8000,
               0x8001,
               0x8002,
               0x8003,
               0x8004,
               0x8008,
               0x8010,
               0x8020,
               0x8040,
               0x8080,
               0x8100,
               0x8200,
               0x8400,
               0x8800,
               0x8888,
               0x9000,
               0xa000,
               0xaaaa,
               0xb000,
               0xbfbf,
               0xbfff,
               0xc000,
               0xc001,
               0xc0c0,
               0xcccc,
               0xd000,
               0xdfdf,
               0xdfff,
               0xe000,
               0xefef,
               0xefff,
               0xf000,
               0xf00f,
               0xf0f0,
               0xf7f7,
               0xf7ff,
               0xf800,
               0xfbfb,
               0xfbff,
               0xfc00,
               0xfc3f,
               0xfdfd,
               0xfe00,
               0xfe7f,
               0xfefe,
               0xfeff,
               0xff00,
               0xff7f,
               0xff80,
               0xffbf,
               0xffdf,
               0xffe0,
               0xffef,
               0xfff7,
               0xfff8,
               0xfffb,
               0xfffc,
               0xfffd,
               0xfff0,
               0xfffe,
               0xffff,
               ]
    _fuzz_library.extend([b"A" * i for i in payload])
    _fuzz_library.extend([b"\xFF" * i for i in payload])
    _fuzz_library.extend([b"\x00" * i for i in payload])

    # from https://en.wikipedia.org/wiki/Magic_number_(programming)#Magic_debug_values
    _magic_debug_values = [
        b"\x00\x00\x81#",
        b"\x00\xfa\xca\xde",
        b"\x1b\xad\xb0\x02",
        b"\x8b\xad\xf0\r",
        b"\xa5\xa5\xa5\xa5",
        b"\xa5",
        b"\xab\xab\xab\xab",
        b"\xab\xad\xba\xbe",
        b"\xab\xba\xba\xbe",
        b"\xab\xad\xca\xfe",
        b"\xb1k\x00\xb5",
        b"\xba\xad\xf0\r",
        b"\xba\xaa\xaa\xad",
        b'\xba\xd2""',
        b"\xba\xdb\xad\xba\xdb\xad",
        b"\xba\xdc\x0f\xfe\xe0\xdd\xf0\r",
        b"\xba\xdd\xca\xfe",
        b"\xbb\xad\xbe\xef",
        b"\xbe\xef\xca\xce",
        b"\xc0\x00\x10\xff",
        b"\xca\xfe\xba\xbe",
        b"\xca\xfe\xd0\r",
        b"\xca\xfe\xfe\xed",
        b"\xcc\xcc\xcc\xcc",
        b"\xcd\xcd\xcd\xcd",
        b"\r\x15\xea^",
        b"\xdd\xdd\xdd\xdd",
        b"\xde\xad\x10\xcc",
        b"\xde\xad\xba\xbe",
        b"\xde\xad\xbe\xef",
        b"\xde\xad\xca\xfe",
        b"\xde\xad\xc0\xde",
        b"\xde\xad\xfa\x11",
        b"\xde\xad\xf0\r",
        b"\xde\xfe\xc8\xed",
        b"\xde\xad\xde\xad",
        b"\xeb\xeb\xeb\xeb",
        b"\xfa\xde\xde\xad",
        b"\xfd\xfd\xfd\xfd",
        b"\xfe\xe1\xde\xad",
        b"\xfe\xed\xfa\xce",
        b"\xfe\xee\xfe\xee",
    ]

    # This is a list of "interesting" 1,2 and 4 byte binary strings.
    # The lists are used to replace each block of 1, 2 or 4 byte in the original
    # value with each of those "interesting" values.
    _fuzz_strings_1byte = [b"\x00", b"\x01", b"\x7F", b"\x80", b"\xFF"] + [
        i for i in _magic_debug_values if len(i) == 1
    ]

    _fuzz_strings_2byte = [
                              b"\x00\x00",
                              b"\x01\x00",
                              b"\x00\x01",
                              b"\x7F\xFF",
                              b"\xFF\x7F",
                              b"\xFE\xFF",
                              b"\xFF\xFE",
                              b"\xFF\xFF",
                          ] + [i for i in _magic_debug_values if len(i) == 2]

    _fuzz_strings_4byte = [
                              b"\x00\x00\x00\x00",
                              b"\x00\x00\x00\x01",
                              b"\x01\x00\x00\x00",
                              b"\x7F\xFF\xFF\xFF",
                              b"\xFF\xFF\xFF\x7F",
                              b"\xFE\xFF\xFF\xFF",
                              b"\xFF\xFF\xFF\xFE",
                              b"\xFF\xFF\xFF\xFF",
                          ] + [i for i in _magic_debug_values if len(i) == 4]

    def __init__(
            self,
            default_value: bytes = b"",
            size: int = None,
            padding: bytes = b"\x00",
            max_len: int = None,
    ):
        if not isinstance(default_value, ByteString):
            raise TypeError("default_value of Bytes must be of ByteString type")
        if not isinstance(padding, ByteString):
            raise TypeError("padding of Bytes must be of ByteString type")

        self.size = size
        self.max_len = max_len
        if self.size is not None:
            self.max_len = self.size
        self.padding = padding

    def mutations(self, default_value):
        for fuzz_value in self._iterate_fuzz_cases(default_value):
            if callable(fuzz_value):
                yield compose(self._adjust_mutation_for_size, fuzz_value)(b'A')
            else:
                yield self._adjust_mutation_for_size(fuzz_value=fuzz_value)

    def _adjust_mutation_for_size(self, fuzz_value):
        if self.size is not None:
            if len(fuzz_value) > self.size:
                return fuzz_value[: self.max_len]
            else:
                return fuzz_value + self.padding * (self.size - len(fuzz_value))
        elif self.max_len is not None and len(fuzz_value) > self.max_len:
            return fuzz_value[: self.max_len]
        else:
            return fuzz_value

    def _iterate_fuzz_cases(self, default_value):
        for fuzz_value in self._fuzz_library:
            yield fuzz_value
        for fuzz_value in self._magic_debug_values:
            yield fuzz_value
        for i in range(0, len(default_value)):
            for fuzz_bytes in self._fuzz_strings_1byte:

                def f(value):
                    if i < len(value):
                        return value[:i] + fuzz_bytes + value[i + 1:]
                    else:
                        return value

                yield f
        for i in range(0, len(default_value) - 1):
            for fuzz_bytes in self._fuzz_strings_2byte:

                def f(value):
                    if i < len(value) - 1:
                        return value[:i] + fuzz_bytes + value[i + 2:]
                    else:
                        return value

                yield f

        for i in range(0, len(default_value) - 3):
            for fuzz_bytes in self._fuzz_strings_4byte:

                def f(value):
                    if i < len(value) - 3:
                        return value[:i] + fuzz_bytes + value[i + 4:]
                    else:
                        return value

                yield f

    def num_mutations(self, default_value):
        """
        Calculate and return the total number of mutations for this individual primitive.

        @rtype:  int
        @return: Number of mutated forms this primitive can take
        :param default_value:
        """
        return sum(
            (
                len(self._fuzz_library),
                len(self._magic_debug_values),
                len(self._fuzz_strings_1byte) * max(0, len(default_value) - 0),
                len(self._fuzz_strings_2byte) * max(0, len(default_value) - 1),
                len(self._fuzz_strings_4byte) * max(0, len(default_value) - 3),
            )
        )

    def encode(self, value, mutation_context):
        if value is None:
            value = b""
        return value


if __name__ == '__main__':
    b = Bytes()
    # c = functools.partial(operator.mul, 2)
    # print(c(5))
    print(b.num_mutations(b'RESPMOD'))
    n=0
    for i in b.mutations(b'RESPMOD'):
        n+=1
        # print(i)
    print(n)
