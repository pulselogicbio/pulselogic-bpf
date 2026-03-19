from bpf.constants import DEFAULT_CONFIG_PATH, DEFAULT_RANDOM_SEED


def test_default_seed():
    assert DEFAULT_RANDOM_SEED == 42


def test_default_config_path():
    assert DEFAULT_CONFIG_PATH == "configs/canonical_v1_0_0.yaml"