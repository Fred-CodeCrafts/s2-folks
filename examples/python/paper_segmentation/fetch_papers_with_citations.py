#!/usr/bin/env python3
import json
import os
from requests import Session
from typing import Generator, TypeVar

S2_API_KEY = os.environ.get('S2_API_KEY', '')

T = TypeVar('T')

def batched(items: list[T], batch_size: int) -> list[T]:
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

def get_paper_batch(session: Session, ids: list[str], fields: str = 'paperId,title', **kwargs) -> list[dict]:
    params = {
        'fields': fields,
        **kwargs,
    }
    headers = {
        'X-API-KEY': S2_API_KEY,
    }
    body = {
        'ids': ids,
    }

    # https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers
    with session.post('https://api.semanticscholar.org/graph/v1/paper/batch',
                       params=params,
                       headers=headers,
                       json=body) as response:
        response.raise_for_status()
        return response.json()

def get_papers(ids: list[str], batch_size: int = 100, **kwargs) -> Generator[dict, None, None]:
    # use a session to reuse the same TCP connection
    with Session() as session:
        # take advantage of S2 batch paper endpoint
        for ids_batch in batched(ids, batch_size=batch_size):
            yield from get_paper_batch(session, ids_batch, **kwargs)

def main():
    # Read PMID IDs
    pmid_file = 'bulk_get_papers_by_pmid/pmid-p53-set.txt'
    with open(pmid_file, 'r') as f:
        pmids = [line.strip() for line in f.readlines()]

    print(f'Fetching data for {len(pmids)} papers...')
    
    papers_data = []
    ids = [f'PMID:{pmid}' for pmid in pmids]
    fields = 'externalIds,title,authors,year,abstract,citationCount,fieldsOfStudy,publicationDate'

    for paper in get_papers(ids, fields=fields):
        # If an ID is not found, the corresponding entry in the response will be null.
        if not paper:
            continue

        paper_authors = paper.get('authors', [])
        papers_data.append({
            'pmid': paper.get('externalIds', {}).get('PubMed', 'N/A'),
            'title': paper.get('title', 'N/A'),
            'first_author': paper_authors[0]['name'] if paper_authors else 'N/A',
            'year': paper.get('year'),
            'citations': paper.get('citationCount', 0),
            'fields': paper.get('fieldsOfStudy', []),
            'publication_date': paper.get('publicationDate', 'N/A')
        })

    # Save to JSON
    output_file = 'papers_data.json'
    with open(output_file, 'w') as f:
        json.dump(papers_data, f, indent=2)
    
    print(f'Wrote {len(papers_data)} papers to {output_file}')
    print(f'Citation range: {min(p["citations"] for p in papers_data)} - {max(p["citations"] for p in papers_data)}')

if __name__ == '__main__':
    main()
