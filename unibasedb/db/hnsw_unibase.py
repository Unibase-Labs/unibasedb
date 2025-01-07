from unibasedb.db.base import Unibase
from unibasedb.db.executors.hnsw_indexer import HNSWLibIndexer


class HNSWUnibase(Unibase):
    _executor_type = HNSWLibIndexer
    reverse_score_order = False
