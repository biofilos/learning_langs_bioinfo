from encoders import NucleotideEncoderV010, NucleotideDecoderV010
from pathlib import Path


initial_nt = "ATGGTNGAT-ACAC"
a = NucleotideEncoderV010(initial_nt)

test_binary = Path("test.bfa")

if test_binary.exists():
    test_binary.unlink()
a.save(test_binary)

fasta_bits = test_binary.open("rb").read()
decoded = NucleotideDecoderV010(fasta_bits).decode()

if initial_nt == decoded:
    print("success")
else:
    print(f"Initial sequence: {initial_nt}\nDecoded sequence: {decoded}")
