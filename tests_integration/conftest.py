"""The integration suite reuses the unit suite's fixtures.

It lives apart because its rows need infrastructure this repository cannot
provision: the Quoin CLI and a writable module catalog. `make test` does not run
it; `make test-integrations` does.
"""

from __future__ import annotations

from tests.conftest import *  # noqa: F401,F403
from tests.conftest import (  # noqa: F401
    manifest,
    quire_engine,
    semantic_block,
    semantic_module,
    skeletons,
)
