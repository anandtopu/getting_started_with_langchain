"""Exercise the realistic application with isolated runtime outputs."""

from common.config import ROOT
from common.testing import execute_script


def test_application():
    execute_script(
        ROOT / "modules/07_embeddings_retrievers/use_case/product_search.py", ["--offline"]
    )
