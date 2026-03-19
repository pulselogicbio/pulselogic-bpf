from pathlib import Path

from bpf.io.hashing import sha256_file


def test_sha256_file_returns_same_hash_for_same_file():
    path = Path("examples/toy_labels.csv")
    h1 = sha256_file(path)
    h2 = sha256_file(path)
    assert h1 == h2