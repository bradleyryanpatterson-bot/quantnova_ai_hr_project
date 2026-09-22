"""Local section retrieval over the checked-in policy corpus."""
import re
from rag.ingest import policy_files

STOP = set('a an the is are am i my me can could would should do does what how for of to in on and or it be about please tell policy quantnova ai employee employees'.split())

def tokens(text):
    words = set(re.findall(r'[a-z0-9]+', text.lower())) - STOP
    aliases = {'pto': 'vacation', 'holiday': 'vacation', 'holidays': 'vacation',
               'benefit': 'benefits', 'insurance': 'benefits', 'sickness': 'sick',
               'password': 'credentials', 'harassment': 'concern', 'complaint': 'concern'}
    return words | {aliases[w] for w in words if w in aliases}

def sections():
    rows = []
    for path in policy_files():
        text = path.read_text(encoding='utf-8')
        title = text.splitlines()[0].lstrip('# ')
        policy_id = re.search(r'Policy ID: (\S+)', text).group(1)
        version = re.search(r'Version: (\S+)', text).group(1)
        for part in re.split(r'^## ', text, flags=re.M)[1:]:
            heading, _, body = part.partition('\n')
            rows.append(dict(policy_id=policy_id, title=title, section=heading.strip(),
                             version=version, snippet=body.strip(), filename=path.name))
    return rows

def search(query, top_k=5):
    terms = tokens(query)
    ranked = []
    for row in sections():
        body = tokens(row['snippet'])
        heading = tokens(row['section'])
        title = tokens(row['title'])
        score = len(terms & body) + 3 * len(terms & heading) + 2 * len(terms & title)
        if score:
            ranked.append((score, row))
    return [row for _, row in sorted(ranked, key=lambda item: -item[0])[:max(1, min(top_k, 10))]]

def build_citation(row: dict) -> dict:
    return {
        "policy_id": row.get("policy_id"),
        "title": row.get("title"),
        "section": row.get("section"),
        "version": row.get("version"),
        "snippet": row.get("snippet"),
    }
