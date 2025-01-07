from unibasedb.db.base import Unibase
from unibasedb.db.executors.inmemory_exact_indexer import InMemoryExactNNIndexer


class InMemoryExactNNUnibase(Unibase):
    _executor_type = InMemoryExactNNIndexer
    reverse_score_order = True
