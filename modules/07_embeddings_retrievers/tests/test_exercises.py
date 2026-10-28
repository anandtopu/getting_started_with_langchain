"""Learner targets; default runs solutions, --exercise-target exercises checks edited baselines."""

import runpy

import pytest

from common.config import ROOT


def test_01_practice(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/07_embeddings_retrievers" / target / "01_practice.py"))[
        "cosine"
    ]
    import numpy as np

    assert fn(np.array([2.0, 0.0]), np.array([3.0, 0.0])) == pytest.approx(1)
    assert fn(np.array([1.0, 0.0]), np.array([0.0, 1.0])) == pytest.approx(0)
    with pytest.raises(ValueError):
        fn(np.zeros(2), np.ones(2))


def test_02_apply(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/07_embeddings_retrievers" / target / "02_apply.py"))[
        "eligible"
    ]
    base = {"category": "tents", "capacity": 4, "waterproof_mm": 3000, "price": 299.99}
    assert fn(base)
    for change in [{"price": 300}, {"capacity": 2}, {"category": "boots"}, {"waterproof_mm": 0}]:
        assert not fn({**base, **change})


def test_03_stretch(request):
    target = request.config.getoption("--exercise-target")
    fn = runpy.run_path(str(ROOT / "modules/07_embeddings_retrievers" / target / "03_stretch.py"))[
        "cache_key"
    ]
    base = ["provider", "model", 64, "query", "tent"]
    original = fn(*base)
    assert original == fn(*base)
    for index, value in [(0, "other"), (1, "new-model"), (2, 32), (3, "document"), (4, " tent")]:
        changed = base.copy()
        changed[index] = value
        assert fn(*changed) != original
