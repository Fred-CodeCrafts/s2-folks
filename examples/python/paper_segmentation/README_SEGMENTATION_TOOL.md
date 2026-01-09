# Paper Segmentation Tool - Usage Guide

## Overview

The **Paper Segmentation Tool** is a modular, configurable Python script that segments research papers into three influence-based layers based on citation counts:
- **Foundational**: Highly cited, classic papers (top ~20%)
- **Intermediate**: Moderately cited, important extensions (middle ~20%)
- **Frontier**: Recent, innovative papers with lower citations (bottom ~60%)

## Features

✅ **User-configurable citation thresholds**  
✅ **Flexible input** - Read from any JSON file or auto-generate examples  
✅ **Multiple output formats** - JSON and formatted tables  
✅ **Optional field grouping** - Organize papers by discipline  
✅ **Automatic sorting** - By citation count within layers  
✅ **Modular design** - Easy to extend and customize  
✅ **No hardcoded dependencies** - Works standalone  

## Installation

No external dependencies required! Works with standard Python 3.6+

```bash
# Just copy the script and run
python paper_segmentation_tool.py
```

## Quick Start

### 1. Run with Example Data
```bash
python paper_segmentation_tool.py
```
This creates an example dataset and outputs both JSON and table formats.

### 2. Use Your Own Data
```bash
python paper_segmentation_tool.py --input papers_data.json
```

### 3. Custom Thresholds
```bash
python paper_segmentation_tool.py --input papers_data.json \
    --foundational-threshold 100 \
    --intermediate-threshold 50
```

### 4. Table Output Only
```bash
python paper_segmentation_tool.py --output-format table
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input JSON file path | None (creates example) |
| `-o, --output` | Output JSON file path | `segmented_papers_output.json` |
| `--foundational-threshold` | Min citations for foundational layer | Auto (80th percentile) |
| `--intermediate-threshold` | Min citations for intermediate layer | Auto (60th percentile) |
| `--no-group-by-field` | Disable field grouping | False |
| `--no-sort` | Disable citation sorting | False |
| `--output-format` | Output format: `json`, `table`, or `both` | `both` |

## Input Format

Your input JSON should be an array of paper objects:

```json
[
  {
    "title": "Paper Title",
    "citations": 123,
    "year": 2020,
    "fields": ["AI", "ML"],
    "first_author": "Author Name"
  }
]
```

**Required fields:**
- `title` (string)
- `citations` (integer)

**Optional fields:**
- `year` (integer)
- `fields` (array of strings or single string)
- `first_author` (string)
- Any other metadata you want to preserve

## Output Format

### JSON Output Structure

```json
{
  "metadata": {
    "total_papers": 100,
    "citation_range": {"min": 0, "max": 500},
    "thresholds": {
      "foundational": 75,
      "intermediate": 40
    },
    "layer_counts": {
      "foundational": 20,
      "intermediate": 20,
      "frontier": 60
    }
  },
  "foundational": {
    "AI": [
      {
        "title": "...",
        "citations": 500,
        "year": 2017
      }
    ],
    "ML": [...]
  },
  "intermediate": {...},
  "frontier": {...}
}
```

### Table Output

The table format shows:
- Summary statistics
- Papers grouped by layer and field
- Top papers in each category
- Citation counts and years

## Usage Examples

### Example 1: Basic Usage with Real Data
```bash
# Use the p53 dataset from the repository
python paper_segmentation_tool.py \
    --input papers_data.json \
    --output p53_segmented.json
```

### Example 2: Custom Thresholds
```bash
# Set specific citation cutoffs
python paper_segmentation_tool.py \
    --input papers_data.json \
    --foundational-threshold 200 \
    --intermediate-threshold 80 \
    --output custom_segmented.json
```

### Example 3: Flat List (No Field Grouping)
```bash
# Disable field grouping for simple lists
python paper_segmentation_tool.py \
    --input papers_data.json \
    --no-group-by-field \
    --output flat_segmented.json
```

### Example 4: Table View Only
```bash
# Quick visualization without saving JSON
python paper_segmentation_tool.py \
    --input papers_data.json \
    --output-format table
```

### Example 5: Combine with Existing Data
```bash
# Process the existing segmented data
python paper_segmentation_tool.py \
    --input papers_data.json \
    --output new_segmentation.json \
    --foundational-threshold 100 \
    --intermediate-threshold 50 \
    --output-format both
```

## Customization & Extension

The tool is designed to be modular. Here's how to extend it:

### Add New Output Formats

```python
def export_to_csv(self, output: Dict[str, Any], filename: str):
    """Add CSV export capability"""
    # Your implementation here
    pass
```

### Modify Segmentation Logic

```python
def segment_papers(self, papers: List[Dict[str, Any]]):
    # Change to quartiles instead of percentiles
    # Or use machine learning clustering
    pass
```

### Add New Metadata Fields

The tool preserves any extra fields in your input JSON, so just add them:

```json
{
  "title": "...",
  "citations": 100,
  "doi": "10.xxx/xxx",
  "abstract": "...",
  "custom_score": 4.5
}
```

### Custom Sorting

```python
# Sort by year instead of citations
tool = PaperSegmentationTool(sort_by_citations=False)
# Then modify the sorting in group_by_fields() method
```

## Files Created

After running the tool, you'll have:

1. **`paper_segmentation_tool.py`** - Main executable script
2. **`example_output.json`** - Sample output with demo data
3. **`segmented_papers_output.json`** - Your actual output (customizable name)
4. **`README_SEGMENTATION_TOOL.md`** - This documentation

## Troubleshooting

**Problem**: `FileNotFoundError`  
**Solution**: Check the input file path. Use absolute paths if needed.

**Problem**: `JSONDecodeError`  
**Solution**: Validate your input JSON format. Each paper must be in an array.

**Problem**: Empty output  
**Solution**: Check if papers have the `citations` field. Default is 0 if missing.

**Problem**: All papers in one layer  
**Solution**: Adjust thresholds manually or check citation distribution.

## Advanced: Programmatic Usage

You can also use the tool as a Python module:

```python
from paper_segmentation_tool import PaperSegmentationTool

# Create tool instance
tool = PaperSegmentationTool(
    foundational_threshold=100,
    intermediate_threshold=50,
    group_by_field=True,
    sort_by_citations=True
)

# Load papers
papers = tool.load_papers('my_papers.json')

# Generate output
output = tool.create_output(papers)

# Save
tool.save_json(output, 'result.json')
tool.print_table(output)
```

## Contributing

The tool is designed to be easily extensible. Future enhancements could include:

- [ ] Support for multiple citation metrics (h-index, impact factor, etc.)
- [ ] Automatic percentile calculation with different algorithms
- [ ] Export to CSV, Excel, HTML
- [ ] Visualization (charts, graphs)
- [ ] Multi-tier segmentation (more than 3 layers)
- [ ] Machine learning-based clustering

## License

This tool is part of the s2-folks examples repository.

---

**Questions or Issues?**  
Check the inline documentation in `paper_segmentation_tool.py` or run:
```bash
python paper_segmentation_tool.py --help
```
