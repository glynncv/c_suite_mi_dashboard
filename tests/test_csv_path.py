import os

import pandas as pd
import pytest

from src.transforms import to_dataframe


@pytest.mark.skipif(not os.path.exists("tests/data/test_incidents.csv"), reason="CSV test file missing")
def test_csv_file_priority_and_mi_scope():
    raw = pd.read_csv("tests/data/test_incidents.csv", encoding="utf-8")
    df = to_dataframe(raw)
    assert "priority" in df.columns
    assert df["priority"].dropna().isin([1, 2, 3, 4, 5]).all()
    # Check MI rule: P1/P2 only
    assert df[df["is_major"]]["priority"].isin([1, 2]).all()
