def assert_metric(value: float) -> None:
    assert 0.0 <= float(value) <= 1.0, "Metric must be normalized to [0,1]"
