from ref import REF_NT_TO_BIN
from struct import pack, unpack
import array
from pathlib import Path
from sys import exit
from errors.encoding import DecodingVersionError

class NucleotideEncoder:
    def __init__(self, nt_str:str, ref_nt_to_bin:dict) -> None:
        self.WORDSIZE = 4
        self.str_version = "0.1.0"
        # the only rule is that the ~ operator on a ACGT,
        # should give the complementary base
        self.nt_to_bin = ref_nt_to_bin
        self.nt_str = nt_str
        self.nt_len = len(self.nt_str)
        # version codes (3), the number of nucleotides, and the wordsize
        header_fields = [int(x) for x in self.str_version.split(".")] + [self.nt_len, self.WORDSIZE]
        self.header = pack("=hhhIh", *header_fields)

    def nt_pair_to_byte(self, nts):
        nibble_1 = self.nt_to_bin[nts[0]]
        nibble_2 = self.nt_to_bin[nts[1]]
        byte = (nibble_1 << self.WORDSIZE) | nibble_2
        return byte

    def encode(self):
        byte_list_len = int((self.nt_len  / 2) + self.nt_len % 2)
        byte_list = [0] * byte_list_len
        if self.nt_len % 2 == 0:
            byte_list[0] = self.nt_pair_to_byte(self.nt_str[:2])
            start_pos = 2
        else:
            byte_list[0] = self.nt_pair_to_byte("-" + self.nt_str[0])
            start_pos = 1
        byte_list_ix = 1
        for start in range(start_pos, self.nt_len, 2):
            end = start + 2
            byte_list[byte_list_ix] = self.nt_pair_to_byte(self.nt_str[start: end])
            byte_list_ix += 1
        encoded = array.array("B", byte_list)
        return self.header + encoded
    def save(self, filename: Path):
        if filename.exists():
            exit("File exists")
        with filename.open("wb") as fo:
            fo.write(self.encode())


class NucleotideDecoder:
    def __init__(self, encoded: bytes, ref_nt_to_bin:dict) -> None:
        self.version = "0.1.0"
        self.nt_to_bin = ref_nt_to_bin
        self.bin_to_nt = {v: k for k, v in self.nt_to_bin.items()}
        self.encoded = encoded
        self.header = self.encoded[:12]
        version, subversion, patch, self.nt_len, self.wordsize = unpack("=hhhIh", self.header)
        self.encoder_version = f"{version}.{subversion}.{patch}"
        self.is_odd = self.nt_len % 2 == 1
    def split_byte(self, byte):
        left = bin((byte >> self.wordsize) & 0x0F)
        right = bin(byte & 0x0F)
        nt = "".join(self.bin_to_nt[int(x, base=2)] for x in (left, right))
        return nt
    def decode(self):
        encoded_data = self.encoded[12:]
        decoded_list_len = len(encoded_data)
        first_decoded = self.split_byte(encoded_data[0])
        decoded_list = [""] * decoded_list_len
        if self.is_odd:
            decoded_list[0] = first_decoded[1]
        else:
            decoded_list[0] = first_decoded
        for ix in range(1, decoded_list_len):
            decoded_list[ix] = self.split_byte(encoded_data[ix])

        return "".join(decoded_list)


class NucleotideEncoderV010(NucleotideEncoder):
    def __init__(self, nt_str:str, ref_nt_to_bin=REF_NT_TO_BIN):
        super().__init__(nt_str=nt_str, ref_nt_to_bin=ref_nt_to_bin)
        self.WORDSIZE = 4
        self.str_version = "0.1.0"


class NucleotideDecoderV010(NucleotideDecoder):
    def __init__(self, encoded: bytes, ref_nt_to_bin=REF_NT_TO_BIN) -> None:
        super().__init__(encoded, ref_nt_to_bin)
        self.version = "0.1.0"
        if self.version != self.encoder_version:
            print("hola")
            raise  DecodingVersionError(f"Incompatible versions. Encoder version is {self.encoder_version} and decoder version is {self.version}")
