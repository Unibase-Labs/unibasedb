import pytest
import random
import string
from docarray import DocList, BaseDoc
from docarray.typing import NdArray
from unibasedb import HNSWUnibase
import numpy as np


class MyDoc(BaseDoc):
    text: str
    embedding: NdArray[128]


@pytest.fixture()
def docs_to_index():
    return DocList[MyDoc](
        [MyDoc(text="".join(random.choice(string.ascii_lowercase) for _ in range(5)), embedding=np.random.rand(128))
         for _ in range(2000)])


@pytest.mark.parametrize('call_method', ['docs', 'inputs', 'positional'])
def test_hnswlib_unibase_batch(docs_to_index, call_method, tmpdir):
    query = docs_to_index[:10]
    indexer = HNSWUnibase[MyDoc](workspace=str(tmpdir), ef=5000)
    if call_method == 'docs':
        indexer.index(docs=docs_to_index)
        resp = indexer.search(docs=query)
    elif call_method == 'inputs':
        indexer.index(inputs=docs_to_index)
        resp = indexer.search(inputs=query)
    elif call_method == 'positional':
        indexer.index(docs_to_index)
        resp = indexer.search(query)
    assert len(resp) == len(query)
    for res in resp:
        assert len(res.matches) == 10
        assert res.id == res.matches[0].id
        assert res.text == res.matches[0].text
        assert res.scores[0] < 0.001  # some precision issues, should be 0.0


@pytest.mark.parametrize('limit', [1, 10, 2000, 2500])
@pytest.mark.parametrize('call_method', ['docs', 'inputs', 'positional'])
def test_hnswlib_unibase_single_query(docs_to_index, limit, call_method, tmpdir):
    query = docs_to_index[100]
    indexer = HNSWUnibase[MyDoc](workspace=str(tmpdir), ef=5000)
    if call_method == 'docs':
        indexer.index(docs=docs_to_index)
        resp = indexer.search(docs=query, limit=limit)
    elif call_method == 'inputs':
        indexer.index(inputs=docs_to_index)
        resp = indexer.search(inputs=query, limit=limit)
    elif call_method == 'positional':
        indexer.index(docs_to_index)
        resp = indexer.search(query, limit=limit)
    assert len(resp.matches) == min(limit, len(docs_to_index))
    assert resp.id == resp.matches[0].id
    assert resp.text == resp.matches[0].text
    assert resp.scores[0] < 0.001  # some precision issues, should be 0.0


def test_hnswlib_unibase_search_field(tmpdir):
    class MyDocTens(BaseDoc):
        text: str
        tens: NdArray[128]

    docs_to_index = DocList[MyDocTens](
        [MyDocTens(text="".join(random.choice(string.ascii_lowercase) for _ in range(5)), tens=np.random.rand(128))
         for _ in range(2000)])

    query = docs_to_index[100]
    indexer = HNSWUnibase[MyDocTens](workspace=str(tmpdir), ef=5000)
    indexer.index(docs=docs_to_index)
    resp = indexer.search(docs=query, search_field='tens')
    assert len(resp.matches) == 10
    assert resp.id == resp.matches[0].id
    assert resp.text == resp.matches[0].text
    assert resp.scores[0] < 0.001  # some precision issues, should be 0.0


@pytest.mark.parametrize('call_method', ['docs', 'inputs', 'positional'])
def test_hnswlib_unibase_delete(docs_to_index, call_method, tmpdir):
    query = docs_to_index[0]
    delete = MyDoc(id=query.id, text='', embedding=np.random.rand(128))
    indexer = HNSWUnibase[MyDoc](workspace=str(tmpdir), ef=5000)
    if call_method == 'docs':
        indexer.index(docs=docs_to_index)
        resp = indexer.search(docs=query)
    elif call_method == 'inputs':
        indexer.index(inputs=docs_to_index)
        resp = indexer.search(inputs=query)
    elif call_method == 'positional':
        indexer.index(docs_to_index)
        resp = indexer.search(query)

    assert len(resp.matches) == 10
    assert resp.id == resp.matches[0].id
    assert resp.text == resp.matches[0].text
    assert resp.scores[0] < 0.001  # some precision issues, should be 0.0

    if call_method == 'docs':
        indexer.delete(docs=delete)
        resp = indexer.search(docs=query)
    elif call_method == 'inputs':
        indexer.delete(docs=delete)
        resp = indexer.search(inputs=query)
    elif call_method == 'positional':
        indexer.delete(docs=delete)
        resp = indexer.search(query)

    assert len(resp.matches) == 10
    assert resp.id != resp.matches[0].id
    assert resp.text != resp.matches[0].text


@pytest.mark.parametrize('call_method', ['docs', 'inputs', 'positional'])
def test_hnswlib_unibase_udpate_text(docs_to_index, call_method, tmpdir):
    query = docs_to_index[0]
    update = MyDoc(id=query.id, text=query.text + '_changed', embedding=query.embedding)
    indexer = HNSWUnibase[MyDoc](workspace=str(tmpdir), ef=5000)
    if call_method == 'docs':
        indexer.index(docs=docs_to_index)
        resp = indexer.search(docs=query)
    elif call_method == 'inputs':
        indexer.index(inputs=docs_to_index)
        resp = indexer.search(inputs=query)
    elif call_method == 'positional':
        indexer.index(docs_to_index)
        resp = indexer.search(query)

    assert len(resp.matches) == 10
    assert resp.id == resp.matches[0].id
    assert resp.text == resp.matches[0].text
    assert resp.scores[0] < 0.001  # some precision issues, should be 0.0

    if call_method == 'docs':
        indexer.update(docs=update)
        resp = indexer.search(docs=query)
    elif call_method == 'inputs':
        indexer.update(inputs=update)
        resp = indexer.search(inputs=query)
    elif call_method == 'positional':
        indexer.update(update)
        resp = indexer.search(inputs=query)

    assert len(resp.matches) == 10
    assert resp.scores[0] < 0.001
    assert resp.id == resp.matches[0].id
    assert resp.matches[0].text == resp.text + '_changed'


def test_hnswlib_unibase_restore(docs_to_index, tmpdir):
    query = docs_to_index[:100]
    indexer = HNSWUnibase[MyDoc](workspace=str(tmpdir), ef=5000)
    indexer.index(docs=docs_to_index)
    resp = indexer.search(docs=query)
    assert len(resp) == len(query)
    for res in resp:
        assert len(res.matches) == 10
        # assert res.id == res.matches[0].id
        # assert res.text == res.matches[0].text
        # assert res.scores[0] < 0.001 # some precision issues, should be 0
    indexer.persist()
    new_indexer = HNSWUnibase[MyDoc](workspace=str(tmpdir), ef=5000)
    resp = new_indexer.search(docs=query)
    assert len(resp) == len(query)
    for res in resp:
        assert len(res.matches) == 10
        # assert res.id == res.matches[0].id
        # assert res.text == res.matches[0].text
        # assert res.scores[0] < 0.001 # some precision issues, should be 0

def test_hnswlib_num_dos(tmpdir):
    db = HNSWUnibase[MyDoc](workspace=str(tmpdir))
    doc_list = [MyDoc(text=f'toy doc {i}', embedding=np.random.rand(128)) for i in range(1000)]
    db.index(inputs=DocList[MyDoc](doc_list))
    x = db.num_docs()
    assert x['num_docs'] == 1000

def test_hnswlib_query_id(tmpdir):
    db = HNSWUnibase[MyDoc](workspace=str(tmpdir))
    doc_list = [MyDoc(id='test_1',text=f'test', embedding=np.random.rand(128)) ]
    db.index(inputs=DocList[MyDoc](doc_list))
    queryobjtest1 = db.get_by_id('test_1')
    queryobjtest2 = db.get_by_id('test_2')
    assert queryobjtest2 is None
    assert queryobjtest1.id == 'test_1'
