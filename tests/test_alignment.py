import pandas as pd
import pytest

from bpf.qc.alignment import validate_sample_alignment


def test_validate_sample_alignment_passes_with_overlap():
    expression_df = pd.DataFrame({"sample_id": ["S1", "S2"], "BMK1": [1.0, 2.0]})
    labels_df = pd.DataFrame({"sample_id": ["S1", "S2"], "label": [1, 0]})
    validate_sample_alignment(expression_df, labels_df)


def test_validate_sample_alignment_raises_on_no_overlap():
    expression_df = pd.DataFrame({"sample_id": ["S1", "S2"], "BMK1": [1.0, 2.0]})
    labels_df = pd.DataFrame({"sample_id": ["S3", "S4"], "label": [1, 0]})

    with pytest.raises(ValueError, match="No overlapping sample IDs"):
        validate_sample_alignment(expression_df, labels_df)