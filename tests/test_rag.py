from rag.ingest import policy_files

def test_quantnova_policy_corpus_present():
    files = policy_files()
    assert len(files) >= 8
    assert all('policy' in p.name for p in files)
