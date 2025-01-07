def _ignore_warnings():
    import logging
    import warnings

    logging.captureWarnings(True)
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="Deprecated call to `pkg_resources.declare_namespace('google')`.",
    )


_ignore_warnings()

__version__ = '0.0.1'

from unibasedb.client import Client
from unibasedb.db.hnsw_unibase import HNSWUnibase
from unibasedb.db.inmemory_exact_unibase import InMemoryExactNNUnibase
