from bpf.constants import DEFAULT_RANDOM_SEED

def test_default_seed():
    assert DEFAULT_RANDOM_SEED == 42