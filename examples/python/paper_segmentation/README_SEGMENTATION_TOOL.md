# Research Paper Segmentation Tool

This script is a local research paper segmentation tool that works on a JSON dataset of papers (like the one produced by your Semantic Scholar fetcher). Here's what it does step by step:

## 1. Purpose

Segments research papers into three influence-based layers based on citation counts:

- **Foundational** – top ~20% most cited
- **Intermediate** – middle ~20%
- **Frontier** – bottom ~60%

Groups papers by primary field of study for easier analysis.

Saves a structured JSON file with segmentation, counts, and metadata.

## 2. Input

A JSON file called `papers_data.json` with this format:

```json
[
  {
    "title": "Paper Title",
    "citations": 123,
    "year": 2020,
    "fields": ["AI", "ML"],
    "first_author": "Author Name"
  },
  ...
]
```

Usually this JSON comes from the Semantic Scholar fetcher.

## 3. Processing Steps

1. Load papers from `papers_data.json`.
2. Calculate citation percentiles:
   - 80th percentile → Foundational threshold
   - 60th percentile → Intermediate threshold
3. Segment papers into three layers using these thresholds.
4. Group papers by field:
   - Uses the first field as "primary field"
   - Sorts papers in each field by citation count descending.
5. Generate output structure with metadata and grouped papers.

## 4. Output

Saves a JSON file: `segmented_papers.json` with this structure:

```json
{
  "metadata": {
    "total_papers": 100,
    "citation_range": {"min": 5, "max": 50000},
    "percentiles": {"80th": 40000, "60th": 150},
    "layer_counts": {"foundational": 20, "intermediate": 20, "frontier": 60}
  },
  "foundational": {
    "AI": [{"title": "...", "citations": 50000, "year": 2017, "field": ["AI", "ML"]}],
    "ML": [...]
  },
  "intermediate": {...},
  "frontier": {...}
}
```

Prints summary tables to the console:

- Citation statistics
- Number of papers in each layer
- Number of papers per field in each layer

### Example console output:

```
Loaded 100 papers

Citation Statistics:
  Range: 5 - 50000
  80th percentile (Foundational threshold): 40000
  60th percentile (Intermediate threshold): 150

Segmentation Results:
  Foundational (top ~20%): 20 papers
  Intermediate (middle ~20%): 20 papers
  Frontier (bottom ~60%): 60 papers

Field Distribution by Layer:
Foundational:
  AI: 10 papers
  ML: 5 papers
  NLP: 5 papers
Intermediate:
  ML: 12 papers
  NLP: 8 papers
Frontier:
  AI: 20 papers
  ML: 15 papers
  Quantum Computing: 25 papers
```

## 5. Key Features

✅ Automatic percentile-based thresholds – no need to manually pick citation cutoffs

✅ Three-layer segmentation – foundational, intermediate, frontier

✅ Field grouping – groups papers by primary research field

✅ Citation sorting – papers in each field are sorted by citations

✅ JSON output – easy to use in other tools or portfolio projects

✅ Console summary – shows overall counts and field distribution
